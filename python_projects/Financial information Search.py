import yfinance as yf


def get_financial_info(NVDA):
    """
    Takes a ticker symbol and returns key financial information.
    """
    # Create the Ticker object
    ticker = yf.Ticker(NVDA)

    # Retrieve info dictionary
    info = ticker.info

    # Extract specific data points
    data = {
        'Company Name': info.get('shortName'),
        'Current Price': info.get('currentPrice'),
        'Market Cap': info.get('marketCap'),
        'P/E Ratio': info.get('forwardPE'),
        '52 Week High': info.get('fiftyTwoWeekHigh'),
        '52 Week Low': info.get('fiftyTwoWeekLow')
    }

    return data

stats = get_financial_info("NVDA")
print(stats)

