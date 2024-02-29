import pymysql
from tcmb_rate import TRY_EURO, TRY_USD
from alanchand import USD_IRR
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#calculation
TRY_IRT = USD_IRR / TRY_USD
IRT_TRY = 1 / TRY_IRT
IRR_USD = 1 / USD_IRR
EURO_IRR = TRY_EURO * TRY_IRT
IRR_EURO = 1 / EURO_IRR


# Replace these variables with your database connection info and the product ID you're updating
db_host = 'localhost'
db_port = '3306'
db_user = 'WHMCS_DB_USERNAME'
db_password = 'WHMCS_DB_PASSWORD'
db_name = 'WHMCS_DB_NAME'


#DB connection
connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
# Initialize the data for POST request
data = {
    'action': 'GetProducts',
    'identifier': 'WHMCS_API_Identifier',
    'secret': 'WHMCS_API_Secret',
    'responsetype': 'json'
}

# Make the POST request
response = requests.post("https://armanhost.com/includes/api.php", data=data, verify=False)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Parse the JSON response
        responseData = response.json()
        
        # Assuming 'products' is a dictionary containing a list under 'product',
        # Iterate through products, looking for '3CX' in the name
        for product in responseData['products']['product']:
            name = product.get('name', '')
            product_id = product.get('pid', '')
            if '3CX' in name:
                #print(name)
                    product_id = product.get('pid', '')
                    prices=product.get('pricing','')
                    price_usd=prices['USD']
                    price_usd_annually=float(price_usd['annually'])
                    price_try_annually=price_usd_annually * TRY_USD
                    price_euro_annually=price_try_annually / TRY_EURO
                    price_irt_annually= (price_usd_annually * USD_IRR ) / 10

                    with connection.cursor() as cursor:
                        # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing 
                        SET annually = %s 
                        WHERE relid = %s AND currency = 1
                        """
                        cursor.execute(sql, (price_try_annually, product_id))
        
                        # Commit the changes to the database
                        connection.commit()

                                           # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing
                        SET annually = %s
                        WHERE relid = %s AND currency = 5
                        """
                        cursor.execute(sql, (price_irt_annually, product_id))

                        # Commit the changes to the database
                        connection.commit()

                                               # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing
                        SET annually = %s
                        WHERE relid = %s AND currency = 6
                        """
                        cursor.execute(sql, (price_euro_annually, product_id))

                        # Commit the changes to the database
                        connection.commit()

    except ValueError:
        # Handle JSON decode error
        print("Error decoding JSON response")
else:
    # Handle possible HTTP errors
    print("HTTP Error:", response.status_code)

