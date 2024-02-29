import pymysql
from tcmb_rate import TRY_EURO, TRY_USD
from alanchand import USD_IRR
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#calculation
TRY_IRT = USD_IRR / TRY_USD


# Replace these variables with your database connection info and the product ID you're updating
db_host = 'localhost'
db_port = '3306'
db_user = 'WHMCS_DB_User'
db_password = 'WHMCS_DB_Password'
db_name = 'WHMCS_DB_Name'


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
response = requests.post("https://whmcsdomain/includes/api.php", data=data, verify=False)

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
            if 'ViTR' in name:
                #print(name)
                    product_id = product.get('pid', '')
                    prices=product.get('pricing','')
                    price_try=prices['TRY']
                    price_try_monthly=float(price_try['monthly'])
                    price_usd_monthly=price_try_monthly / TRY_USD
                    price_euro_monthly=price_try_monthly / TRY_EURO
                    price_irt_monthly=price_try_monthly * TRY_IRT

                    with connection.cursor() as cursor:
                        # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing 
                        SET monthly = %s 
                        WHERE relid = %s AND currency = 7
                        """
                        cursor.execute(sql, (price_usd_monthly, product_id))
        
                        # Commit the changes to the database
                        connection.commit()

                                           # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing
                        SET monthly = %s
                        WHERE relid = %s AND currency = 5
                        """
                        cursor.execute(sql, (price_irt_monthly, product_id))

                        # Commit the changes to the database
                        connection.commit()

                                               # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing
                        SET monthly = %s
                        WHERE relid = %s AND currency = 6
                        """
                        cursor.execute(sql, (price_euro_monthly, product_id))

                        # Commit the changes to the database
                        connection.commit()

    except ValueError:
        # Handle JSON decode error
        print("Error decoding JSON response")
else:
    # Handle possible HTTP errors
    print("HTTP Error:", response.status_code)

