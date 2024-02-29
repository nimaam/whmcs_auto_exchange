
import requests
import xml.etree.ElementTree as ET

# URL containing the XML data
url = "http://www.tcmb.gov.tr/kurlar/today.xml"

# Fetch the XML data from the URL
response = requests.get(url)
# Ensure the request was successful
response.raise_for_status()

# Parse the XML from the response text
root = ET.fromstring(response.text)

# Define the currency codes we are interested in
currency_codes = ["USD", "EUR", "IRR"]

# Initialize a dictionary to hold our results
rates = {}

# Iterate over each 'Currency' element in the XML
for currency in root.findall('.//Currency'):
    # Get the currency code
    code = currency.get('Kod')
    # Check if this is one of the currencies we're interested in
    if code in currency_codes:
        # Try to find the 'BanknoteSelling' element and get its text
        # If not found, use None
        banknote_selling = currency.find('BanknoteSelling').text if currency.find('BanknoteSelling') is not None else None
        # Store the rate in our dictionary
        rates[code] = banknote_selling
        
# Print out the rates we found
#for code, rate in rates.items():
#    print(f"{code}: {rate}")
TRY_EURO=float(rates["EUR"])
TRY_USD=float(rates["USD"])
#print(TRY_EURO)
#print(TRY_USD)
