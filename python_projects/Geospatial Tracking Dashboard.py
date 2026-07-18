#!/usr/bin/env python3
"""
PALANTIR-STYLE EARTH — Live Intelligence Display
Run this file directly from PyCharm.
Serves a local web app with live data from:
  - OpenSky Network (7,000+ live aircraft)
  - ADS-B Exchange (military flights)
  - CelesTrak (satellite TLE orbital data)
  - OpenStreetMap (city vehicle flow particles)
  - Austin Public CCTV cameras
"""

import http.server
import socketserver
import threading
import webbrowser
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

PORT = 8765
BASE_DIR = Path(__file__).parent


# ── Live data proxy endpoints ──────────────────────────────────────────────

def fetch_opensky():
    """Fetch live aircraft from OpenSky Network (no auth needed for basic)."""
    try:
        url = "https://opensky-network.org/api/states/all?lamin=24&lomin=-125&lamax=50&lomax=-65"
        req = urllib.request.Request(url, headers={"User-Agent": "PalantirEarth/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            states = data.get("states", []) or []
            aircraft = []
            for s in states[:300]:  # cap at 300 for perf
                if s[5] and s[6]:  # must have lon/lat
                    aircraft.append({
                        "icao": s[0], "callsign": (s[1] or "").strip(),
                        "lon": s[5], "lat": s[6], "alt": s[7] or 0,
                        "vel": s[9] or 0, "hdg": s[10] or 0,
                        "country": s[2], "on_ground": s[8]
                    })
            return aircraft
    except Exception as e:
        print(f"[OpenSky] {e}")
        return []


def fetch_adsb_military():
    """Fetch military aircraft from ADS-B Exchange public API."""
    try:
        url = "https://opendata.adsb.fi/api/v2/mil"
        req = urllib.request.Request(url, headers={"User-Agent": "PalantirEarth/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            ac_list = data.get("ac", [])
            aircraft = []
            for ac in ac_list[:150]:
                if ac.get("lon") and ac.get("lat"):
                    aircraft.append({
                        "icao": ac.get("hex", ""), "callsign": ac.get("flight", "").strip(),
                        "lon": ac.get("lon"), "lat": ac.get("lat"),
                        "alt": ac.get("alt_baro", 0) or 0,
                        "vel": ac.get("gs", 0) or 0, "hdg": ac.get("track", 0) or 0,
                        "military": True
                    })
            return aircraft
    except Exception as e:
        print(f"[ADS-B Exchange] {e}")
        return []


def fetch_celestrak_tle():
    """Fetch satellite TLE data from CelesTrak."""
    try:
        # Active satellites
        url = "https://celestrak.org/SOCRATES/query.php?CODE=ALL&MAX=100&FORMAT=json"
        # Fallback: well-known active group
        url = "https://celestrak.org/SOCRATES/query.php"
        # Use the simpler TLE endpoint
        url = "https://celestrak.org/pub/TLE/catalog.txt"
        req = urllib.request.Request(url, headers={"User-Agent": "PalantirEarth/1.0"})
        # Actually use the active satellites JSON
        url = "https://celestrak.org/SOCRATES/query.php?CODE=ALL&MAX=50&FORMAT=json"
        # Use active.json
        url = "https://celestrak.org/pub/TLE/active.txt"
        req = urllib.request.Request(url, headers={"User-Agent": "PalantirEarth/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            lines = r.read().decode("utf-8", errors="ignore").strip().split("\n")
            sats = []
            i = 0
            while i + 2 < len(lines) and len(sats) < 180:
                name = lines[i].strip()
                tle1 = lines[i+1].strip()
                tle2 = lines[i+2].strip()
                if tle1.startswith("1 ") and tle2.startswith("2 "):
                    sats.append({"name": name, "tle1": tle1, "tle2": tle2})
                i += 3
            return sats
    except Exception as e:
        print(f"[CelesTrak] {e}")
        return []


def fetch_austin_cameras():
    """Austin public CCTV camera locations."""
    # Austin Open Data — traffic cameras
    try:
        url = "https://data.austintexas.gov/resource/p53x-x73x.json?$limit=60"
        req = urllib.request.Request(url, headers={"User-Agent": "PalantirEarth/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            cams = json.loads(r.read())
            result = []
            for c in cams:
                loc = c.get("location", {})
                if isinstance(loc, dict) and loc.get("coordinates"):
                    lon, lat = loc["coordinates"]
                    result.append({
                        "id": c.get("camera_id", ""),
                        "name": c.get("location_name", "Camera"),
                        "lon": float(lon), "lat": float(lat),
                        "ip": c.get("camera_ip", "")
                    })
                elif c.get("longitude") and c.get("latitude"):
                    result.append({
                        "id": c.get("camera_id", ""),
                        "name": c.get("location_name", "Camera"),
                        "lon": float(c["longitude"]), "lat": float(c["latitude"]),
                        "ip": c.get("camera_ip", "")
                    })
            return result
    except Exception as e:
        print(f"[Austin CCTV] {e}")
        return []


# ── HTTP Server ────────────────────────────────────────────────────────────

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        # API routes
        if self.path == "/api/aircraft":
            self._json(fetch_opensky())
        elif self.path == "/api/military":
            self._json(fetch_adsb_military())
        elif self.path == "/api/satellites":
            self._json(fetch_celestrak_tle())
        elif self.path == "/api/cameras":
            self._json(fetch_austin_cameras())
        else:
            super().do_GET()

    def _json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Suppress noisy request logs
        if "/api/" in (args[0] if args else ""):
            return
        print(f"  [server] {fmt % args}")


def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        print(f"\n  ╔══════════════════════════════════════╗")
        print(f"  ║   PALANTIR EARTH  —  Live Intel       ║")
        print(f"  ║   http://localhost:{PORT}               ║")
        print(f"  ╚══════════════════════════════════════╝\n")
        httpd.serve_forever()


if __name__ == "__main__":
    # Start server in background thread
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # Open browser
    import time
    time.sleep(0.5)
    webbrowser.open(f"http://localhost:{PORT}/index.html")

    print("  Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Shutting down.")