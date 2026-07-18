print("WELCOME HERO")

# --- Create your character as a dictionary ---
name = input("Enter your name: ")

player = {
    "name": name,
    "health": 100,
    "attack": 15,
    "defense": 5,
    "gold": 0
}

print(f"\nWelcome to the Vampire Republic, {player['name']}!")
print(f"HP: {player['health']} | ATK: {player['attack']} | DEF: {player['defense']}")

# --- Enemies are characters too ---
def create_enemy(name, health, attack, gold):
    return {"name": name, "health": health, "attack": attack, "gold": gold}

# --- Combat function ---
def combat(player, enemy):
    print(f"\n⚔️  {enemy['name']} appears! HP: {enemy['health']}")

    while player["health"] > 0 and enemy["health"] > 0:
        print(f"\nYour HP: {player['health']} | {enemy['name']} HP: {enemy['health']}")
        action = input("Attack, Defend, or Flee? ").strip().capitalize()

        if action == "Attack":
            damage = player["attack"]
            enemy["health"] -= damage
            print(f"You deal {damage} damage!")

            if enemy["health"] <= 0:
                print(f"✅ {enemy['name']} defeated! You earn {enemy['gold']} gold.")
                player["gold"] += enemy["gold"]
                return "win"

            # Enemy hits back
            taken = max(0, enemy["attack"] - player["defense"])
            player["health"] -= taken
            print(f"{enemy['name']} hits you for {taken} damage!")

        elif action == "Defend":
            taken = max(0, enemy["attack"] - player["defense"] - 5)  # defense bonus
            player["health"] -= taken
            print(f"You brace! {enemy['name']} hits for only {taken} damage.")

        elif action == "Flee":
            print("You flee! You lose 10 HP escaping.")
            player["health"] -= 10
            return "fled"

        else:
            print("Invalid action!")

    print("💀 You have been defeated. Game Over!")
    return "lose"

# --- The adventure ---
direction = input("\nGo left or right? ").strip().lower()

if direction == "left":
    print("\nYou enter the town square...")
    enemy = create_enemy("Goblin", health=30, attack=8, gold=10)
else:
    print("\nYou approach the castle...")
    enemy = create_enemy("Skeleton", health=40, attack=12, gold=20)

result = combat(player, enemy)

if result == "win":
    print(f"\n🏆 You won! Final stats — HP: {player['health']} | Gold: {player['gold']}")
elif result == "fled":
    print(f"\nYou escaped... HP: {player['health']}")
