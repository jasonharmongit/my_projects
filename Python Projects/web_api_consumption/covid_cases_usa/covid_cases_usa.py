"""
Feb, 2023
A project built for one of the Python courses I took at USU. This program calls a Web API containing historical COVID-19
data about the United States in JSON format, parses it, then calculates a variety of metrics regarding certain States.
"""

import requests
import json
import numpy as np
from datetime import datetime

#introduction line
print("COVID CONFIRMED CASES STATISTICS:")
print("--------------------------")

states = ['ca', 'ut', 'il', 'tx', 'nj']
results = {} #start a dictionary to track relevant results

for state in states: #repeat calculations for each state in the list
    
    #grab data from URL and put it in a list
    url = 'https://api.covidtracking.com/v1/states/' + state + '/daily.json'
    request = requests.get(url)
    lst = json.loads(request.text)
    filepath = ''
    json.dump(lst, open(filepath + '/covid/' + state + '.json', "w"), indent=1) #create json files
    
    #print state name
    name_key = "state"
    print("State name:", lst[0][name_key])
    
    #create corresponding day and case increase number lists
    days = []
    pos_cases = []
    date_key = "date"
    pos_key = "positiveIncrease"
    for day in lst:
        days.append(day[date_key])
        pos_cases.append(day[pos_key])
    
    #find average number of cases for the state dataset (stored in the pos_cases list)
    avg_cases = np.mean(pos_cases)
    avg_cases = round(avg_cases,2)
    print("Average number of new daily confirmed cases for the entire state dataset:", avg_cases)
    results[state + "_avg_new_cases"] = avg_cases
    
    #find max number of cases in data set
    max_cases = max(pos_cases)
    high_date = days[pos_cases.index(max_cases)]
    high_date_transformed = datetime.strptime(str(high_date), '%Y%m%d') #convert to datetime object
    high_date_transformed = high_date_transformed.strftime('%m/%d/%Y')
    print("Date with the highest new number of confirmed cases: ", high_date_transformed, " (", max_cases, " cases)", sep="") #report corresponding date of max cases
    results[state + "_highest_cases_day"] = high_date_transformed
    
    #find most recent date with no new cases
    rec_date = days[pos_cases.index(0)] #because list is in reverse chronological order, simply find first occurance of 0 new cases
    rec_date_transformed = datetime.strptime(str(rec_date), '%Y%m%d') #convert to datetime object
    rec_date_transformed = rec_date_transformed.strftime('%m/%d/%Y')
    print("Most recent date with no new confirmed cases:", rec_date_transformed) #report
    results[state + "_rec_date_no_cases"] = high_date_transformed
    
    # initialize variables
    max_new_cases = 0
    max_month = 0
    current_month = 0
    current_new_cases = 0
    month_new_cases = 0
    max_year = 0
    min_new_cases = 0
    min_month = 0
    min_year = 0
    month_count = 0
    
    #iterate through all the days of the list, adding them up for each month and comparing them to a max month variable
    for day in lst:
        current_year = day[date_key] // 10000 #truncate to just the year to store year variable
        no_year = day[date_key] % 10000 #remove the year in first step to isolate month
        month = no_year // 100 #remove day to leave just the month of the current day
        day_new_cases = day[pos_key]
        
        if month != current_month: #if it changed months, compare to maximums and minimums and change if necessary
            month_count += 1
            if month_new_cases > max_new_cases:
                max_new_cases = month_new_cases
                max_month = current_month
                max_year = current_year
                
            if month_count == 1: #first month change
                if month_new_cases == 0: #if there are no cases, reset
                    month_count = 0
                else: #otherwise, make this first month the minimum
                    min_new_cases = month_new_cases 
                    min_month = current_month
                    min_year = current_year
                
            elif month_new_cases < min_new_cases: #check every other month against the minimum month
                min_new_cases = month_new_cases
                min_month = current_month
                min_year = current_year
                
            #reset monthly new cases counter, change month
            month_new_cases = day_new_cases
            current_month = month
            
        else: #while the month doesn't change, add each day's new cases to the monthly total
            month_new_cases += day_new_cases
     
    #check on last month in set, becuase it won't trigger the change month statement
    if month_new_cases > max_new_cases:
        max_new_cases = month_new_cases
        max_month = current_month
        max_year = current_year
    elif month_new_cases < min_new_cases and month_new_cases != 0:
        min_new_cases = month_new_cases
        min_month = current_month
        min_year = current_year
                
    #print max and min months, along with cases
    print("Month with the highest new number of confirmed cases: ", max_month, "/", max_year, " (", max_new_cases, " cases)", sep="")
    results[state + "_max_month"] = max_month
    print("Month with the lowest new number of confirmed cases: ", min_month, "/", min_year, " (", min_new_cases, " cases)", sep="")
    results[state + "_min_month"] = min_month
    print("--------------------------")
    
    json.dump(results, open(filepath + "/results.json", "w"), indent=1) #dump results