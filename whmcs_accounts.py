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
db_user = 'armanhost_wuhsmecrsdb'
db_password = ']u%4G1~2JqPW'
db_name = 'armanhost_wdhamtcasbase'


#DB connection
connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
# Initialize the data for POST request
data = {
    'action': 'GetProducts',
    'identifier': 'sPzsDkph38rGQ5LrlGaWZVNeoDeNhtrI',
    'secret': 'FtYLemzPtt0f75qZFCQLt2o4aUMdkKBv',
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
            if 'Account' in name:
                #print(name)
                    product_id = product.get('pid', '')
                    prices=product.get('pricing','')
                    price_try=prices['TRY']
                    price_try_monthly=float(price_try['monthly'])
                    price_usd_monthly=price_try_monthly / TRY_USD
                    price_euro_monthly=price_try_monthly / TRY_EURO
                    price_irt_monthly=price_try_monthly * TRY_IRT


                    price_try_quarterly=float(price_try['quarterly'])
                    price_usd_quarterly=price_try_quarterly / TRY_USD
                    price_euro_quarterly=price_try_quarterly / TRY_EURO
                    price_irt_quarterly=price_try_quarterly * TRY_IRT


                    price_try_annually=float(price_try['annually'])
                    price_usd_annually=price_try_annually / TRY_USD
                    price_euro_annually=price_try_annually / TRY_EURO
                    price_irt_annually=price_try_annually * TRY_IRT

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

                        # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing 
                        SET quarterly = %s 
                        WHERE relid = %s AND currency = 7
                        """
                        cursor.execute(sql, (price_usd_quarterly, product_id))

                        # Commit the changes to the database
                        connection.commit()

                                           # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing
                        SET quarterly = %s
                        WHERE relid = %s AND currency = 5
                        """
                        cursor.execute(sql, (price_irt_quarterly, product_id))

                        # Commit the changes to the database
                        connection.commit()

                                               # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing
                        SET quarterly = %s
                        WHERE relid = %s AND currency = 6
                        """
                        cursor.execute(sql, (price_euro_quarterly, product_id))

                        # Commit the changes to the database
                        connection.commit()


                        # SQL query to update the annully field
                        sql = """
                        UPDATE tblpricing 
                        SET annually = %s 
                        WHERE relid = %s AND currency = 7
                        """
                        cursor.execute(sql, (price_usd_annually, product_id))

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

