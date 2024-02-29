import pymysql
from alanchand import USD_IRR
from tcmb_rate import TRY_EURO, TRY_USD
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Replace these variables with your database connection info and the product ID you're updating
db_host = 'localhost'
db_port = '3306'
db_user = 'WHMCS_DB_User'
db_password = 'WHMCS_DB_Password'
db_name = 'WHMCS_DB_Name'

#Calculation
TRY_IRT = USD_IRR / TRY_USD 
IRT_TRY = 1 / TRY_IRT
IRR_USD = 1 / USD_IRR
EURO_IRR = TRY_EURO * TRY_IRT
IRR_EURO = 1 / EURO_IRR

print("TRY To EURO")
print(TRY_EURO)
print("TRY To USD")
print(TRY_USD)
print("TRY To IRT")
print(TRY_IRT)
print("IRT To TRY")
print(IRT_TRY)
print("IRR To USD:")
print(IRR_USD)
print("IRR To Euro:")
print(IRR_EURO)

#DB connection
connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
                        

with connection.cursor() as cursor:            
    # SQL query to update the annully field
    sql = """
    UPDATE tblcurrencies
    SET rate = %s
    WHERE code = "IRT" 
    """
    cursor.execute(sql, (TRY_IRT,))

    # Commit the changes to the database
    connection.commit()

    sql = """
    UPDATE tblcurrencies
    SET rate = %s
    WHERE code = "USD"
    """
    cursor.execute(sql, (TRY_USD,))

    # Commit the changes to the
    connection.commit()

    # SQL query to update the annully field
    sql = """
    UPDATE tblcurrencies
    SET rate = %s
    WHERE code = "EURO" 
    """
    cursor.execute(sql, (TRY_EURO,))

    # Commit the changes to the
    connection.commit()
