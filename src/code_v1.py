#!/usr/bin/python
from __future__ import division
import pandas as pd
import datetime
import os
import json


def Ingest(e, D=[]):
    data = pd.read_json(e)
    #except:
    #    print ("Invalid File Name or File is Missing")    
    # Creating Subsets of the Main Data_store as follows:
    customer = data[data['type'] == 'CUSTOMER']
    site_visit = data[data['type'] == 'SITE_VISIT']
    image = data[data['type'] == 'IMAGE']
    order = data[data['type'] == 'ORDER']
    print(order[['verb','key']])
        
        
    #Update the table order [Implementing Type 1 SCD: Keeping the updated order]
    order = order.sort_values(by=["key", "event_time"],ascending=False)
    order = order.drop_duplicates(subset=["key"], keep='first')
    
    
    # Size of Datastore
    print("current size of datastore :",len(data))
   
    # Removing 'USD' from total amount for calculations
    for k, v in order['total_amount'].iteritems():
        order.set_value(k, 'total_amount', float(str(v).split(' ')[0]))    

    # Total Revenue by each customer
    revenue = pd.DataFrame(order.groupby(['customer_id'])[['total_amount']].sum())
    
    #Total Visits by each customer
    visits = site_visit['customer_id'].value_counts()
    
    #List of customer_ids
    customer_list = list(set(customer['key']))
    
    #Creating LTV table for customers
    LTV_table = pd.DataFrame(columns=['customer_id','customer_last_name','total_revenue','total_visits','LTV_Value'])
    
    #Update the LTV table
    for i in customer_list:
            idx = len(LTV_table)
            visit_list = site_visit.loc[site_visit['customer_id']==i, 'event_time'].tolist()

            if len(visit_list) == 0:
                continue

            elif len(visit_list) >= 1:
                nweeks = cal_weeks(visit_list)
                if nweeks == 0:
                    nweeks = 1

            rev_per_wk = (revenue.loc[i, 'total_amount'] / visits.loc[i])
            
            vist_per_wk= (visits.loc[i] / nweeks)
            
            a= rev_per_wk * vist_per_wk
            
            ltv_value = 52 * a * 10

            #Update the LTV values for customers in LTV_table
            LTV_table.loc[idx, 'customer_id'] = i
            LTV_table.loc[idx, 'customer_last_name'] = customer.loc[customer['key'][customer['key'] == i].index[0], 'last_name']
            LTV_table.loc[idx, 'total_revenue'] = float(revenue.loc[i, 'total_amount'])
            LTV_table.loc[idx, 'total_visits'] = visits.loc[i]
            LTV_table.loc[idx, 'LTV_Value'] = int(ltv_value)
    return(LTV_table)

# Function to calculate the weeks between first and last visit in the timeframe
def cal_weeks(visit_list):
    dt1=list(map(int,(max(visit_list).strftime("%Y-%m-%d").split("-"))))
    dt2=list(map(int,(min(visit_list).strftime("%Y-%m-%d").split("-"))))
    dt1 = datetime.date(dt1[0], dt1[1], dt1[2])
    dt2 = datetime.date(dt2[0], dt2[1], dt2[2])
    return(((dt1 - dt2)/7).days)   

def TopXSimpleLTVCustomers(x, LTV):
    LTV_Table=LTV.sort_values(by="LTV_Value",ascending=False)
    top_x = LTV_Table.head(x)
    print(top_x)

LTV = Ingest('../sample_input/events.txt', D)

TopXSimpleLTVCustomers(10, LTV)
