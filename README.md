# WHMCS Auto Exchange Updater!

Hi! I'm ytry to make a code to update the exchange rates in  **WHMCS**.  As I am living in Turkey, one of the currency is Turkish Lira (TRY) and I want to have the rates to EURO, USD and Iranian rials always with the last rate, as you maybe know the WHMCS has default currency, so my default here is TRY , this code get he TRY To USD and Euro from the **Turkish Central Bank (TCMB)** and for the Iranian rial form **AlanChand**.


# Configurations

To run the code properly we should have these items
 **WHMCS API Credential**
 **WHMCS API URL**
  **WHMCS Database Access**
Then edit the files and replace them in.

## Schedule to run

Due to situation I run the code with Cron in cPanel 2 times a day

## What this code do?

We have some python files here is important like whmcs_3cx.py, in this file we search the products has a name of "3CX" in "Licenses" group and then update the price in Euro, TL and IRT in this code as you will se the main currency is USD, because the 3CX company base currency is US Dollar, but in whmcs_account,py the main price is TL and we want to have updated in Euro, USD and IRT, so for each product or category of product you can extend the code and use it.
This code remove the WHMCS limitation for the multi currency prices.
