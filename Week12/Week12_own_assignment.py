import pymysql
import re
import pandas as pd
from sqlalchemy import create_engine 
from datetime import datetime, date, timedelta

# Assignment link:
# http://samplecsvs.s3.amazonaws.com/SacramentocrimeJanuary2006.csv

# -------------------------------------------
# -------------------- 1 --------------------
# -------------------------------------------
# Download data fra linket og gem det i en dataframe 
# og gem det i en mysql database

def get_crime_data():
    URL = "http://samplecsvs.s3.amazonaws.com/SacramentocrimeJanuary2006.csv"
    dataframe = pd.read_csv(URL)

    con_str = 'mysql+pymysql://dev:ax2@localhost:3307/python'
    engine = create_engine(con_str)

    dataframe.to_sql('crimes',con=engine, if_exists='append', index = False)
    print(dataframe.dtypes)
    print("Check your database...")

# get_crime_data()


# -------------------------------------------
# -------------------- 2 --------------------
# -------------------------------------------
# Lav en funktion der returnerer en dict med minimum følgende data:
# - Find antallet af crimes mellem to givne datoer i 2006 (givet som parameter til funktionen)
# - Find den totale mængde af "burglary" i januar

# Part 1
def get_amount_of_crimes_in_period(start_date=None, end_date=None):
    if not (isinstance(start_date, date)) :
        return "Please provide a start date"
    if not (isinstance(end_date, date)) :
        return "Please provide an end date"
    # In python strings when formatting dates (as far as i know): 
    # %m = month 
    # %d = day 
    # %y = year
    # %H = hour 
    # %M = minute
    
    # To match the format the dates in the database are saved with I use 
    # date.strftime("%m/%d/%y %H:%M") to convert a python date into a string 
    # that can be used in a SQL query
    # Initially I did this:
    # date1 = start_date.strftime("%m/%d/%y %H:%M")
    # date2 = end_date.strftime("%m/%d/%y %H:%M")
    # which would convert the dates to dates with the correct format and added timestamp.
    # But the timestamp would always be 00:00 which means the end date didn't count as 
    # the entire date - only the first minute of the day which is not optimal, so I 
    # added the timestamp manually instead:
    date1 = start_date.strftime("%m/%d/%y")
    date2 = end_date.strftime("%m/%d/%y")
    # Making sure the first date begins at the first minute of the day
    date1 += " 00:00"
    # Making sure the second date ends at the very last minute of the day
    date2 += " 23:59"

    # In the SQL query we have to use STR_TO_DATE since all the dates are saved 
    # as TEXT and not as dates. In order to make the format of the date-strings match,
    # we have to use the following string as format in the query: '%m/%d/%y %H:%i'
    # %m = month 
    # %d = day 
    # %y = year as a numeric, 2-digit value
    # %H = hour (00 to 23)
    # %i = minutes (00 to 59)

    sqlquery = (
    "SELECT count(*) FROM crimes "
    "WHERE STR_TO_DATE(cdatetime, '%m/%d/%y %H:%i') "
    "BETWEEN STR_TO_DATE('{}', '%m/%d/%y %H:%i') "
    "AND STR_TO_DATE('{}', '%m/%d/%y %H:%i')"
    ).format(date1, date2)
    cnx = pymysql.connect(user='dev', password='ax2',host='127.0.0.1',port=3307,db='python') 
    cursor = cnx.cursor() 

    cursor.execute(sqlquery)

    amount_of_crimes = cursor.fetchall()
    cursor.close()
    cnx.close()
    # Extract the number from the result using regex
    only_numbers = re.compile(r'\d+')
    mo = only_numbers.search(str(amount_of_crimes))
    result = mo.group()
    return result

# Part 2
def get_total_amount_of_burglaries():
    sqlquery = "SELECT count(*) FROM crimes WHERE `crimedescr` LIKE '%BURGLARY%'"
    
    cnx = pymysql.connect(user='dev', password='ax2',host='127.0.0.1',port=3307,db='python') 
    cursor = cnx.cursor() 

    cursor.execute(sqlquery)

    amount_of_crimes = cursor.fetchall()
    cursor.close()
    cnx.close()
    # Extract the number from the result using regex
    only_numbers = re.compile(r'\d+')
    mo = only_numbers.search(str(amount_of_crimes))
    result = mo.group()
    return result

def get_specific_crime_data_as_dict(start_date, end_date):
    result = {}
    result["Amount_of_crimes_in_period"] = get_amount_of_crimes_in_period(start_date, end_date)
    result["Total_amount_of_burglaries"] = get_total_amount_of_burglaries()
    return result


# start_date = date(2006, 1, 1)
# end_date = date(2006, 1, 2)
# print(get_amount_of_crimes_in_period(None))
# res = get_specific_crime_data_as_dict(start_date, end_date)
# print(res)

# -------------------------------------------
# -------------------- 3 --------------------
# -------------------------------------------
# Lav en flask server, hvor du åbner minimum 2 endpoints:
# - GET : returner data omkring antallet af crimes i en given periode 
# (giv to datoer med som query-param i URL'en)
# - POST : returner den totale mængde af "burglaries" i januar, men returner kun data, 
# hvis request.body indeholder et json objekt med key-value "key":"secret"

# Will create the server in a separate file
# Week12_own_assignment_server.py