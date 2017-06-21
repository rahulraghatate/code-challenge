#!/usr/bin/python
import random
import fileinput
import os

'''
* Test Data Generation : Currently it generates all events properly and randomly. 

* As sequence of generation is random, if site_visit or order events are generated for customer absent in customer_table, resulting in
failure in code.py at point where site_visits/orders for particular customer are not found for calculations or vice versa.

* Also Order with "UPDATE" verb are unable to generate as it requires existing_customer_id list and if order event is picked first, its unable to find existing customer 

** These cases will be taken care of in future updates to code
''' 

class Data_Generator:
    types = ["CUSTOMER", "SITE_VISIT", "IMAGE", "ORDER"]
    last_names = ["Shah", "Miller", "Charlie", "Stanley", "Eden", "Franklin", "Smith"]
    cities = ["Atlanta", "Boston", "Chicago", "New York", "Detroit", "Seattle","Palo Alto"]
    states = ["GA", "MA", "IL", "NY", "MI", "WA", "CA"]
    
    def __init__(self):
        self.customer_list = set()
        self.order_list= set()

    def events(self):
        key = str('')
        customer_id = str(random.randrange(1,20))

        #event_time : there can be issue about the "UPDATE" records for event_type=="ORDER" as randomly generated event_time can be earlier than "NEW" order
        yy = random.randrange(2013, 2016)
        MM = "%02d" % random.randrange(1,13)
        dd = "%02d" % random.randrange(1,29)
        hh = "%02d" % random.randrange(0,24)
        mm = "%02d" % random.randrange(0,60)
        ss = "%02d" % random.randrange(0,60)
        SSS = "%02d" % random.randrange(0,1000)
        
        #key is 12 characters long
        for i in range(0, 12):
            key = str(key + random.choice('abcdef0123456789'))

        #Initialize the verb as "NEW"
        verb = "NEW"
        
        #Randomly select the Event_type
        event_type = self.types[random.randrange(0, 4)]
        
        if event_type == "CUSTOMER":
            key = str(random.randrange(1,20))
            
            #Update the customer_list
            self.customer_list.add(key)
            
            #Customer properties
            last_name = self.last_names[random.randrange(0, 7)]
            random_index = random.randrange(0, 7)
            adr_city = self.cities[random_index]
            adr_state = self.states[random_index]

            if customer_id in self.customer_list:
                verb = "UPDATE"
            record = '{{"type": "{}", "verb": "{}", "key": "{}", "event_time": "{}-{}-{}T{}:{}:{}.{}Z", "last_name": "{}", "adr_city": "{}", "adr_state": "{}"}}'.format(
                        event_type, verb, customer_id, yy, MM, dd, hh, mm, ss, SSS, last_name, adr_city, adr_state)
            return record

        elif event_type == "SITE_VISIT":
            record = '{{"type": "{}", "verb": "{}", "key": "{}", "event_time": "{}-{}-{}T{}:{}:{}.{}Z", "customer_id": "{}", "tags": {{"some key": "some value"}}}}'.format(
                        event_type, verb, key, yy, MM, dd, hh, mm, ss, SSS, customer_id)
            return record
        
        elif event_type == "IMAGE":
            verb = "UPLOAD"
            record = '{{"type": "{}", "verb": "{}", "key": "{}", "event_time": "{}-{}-{}T{}:{}:{}.{}Z", "customer_id": "{}", "camera_make": "Canon", "camera_model": "EOS 80D"}}'.format(
                        event_type, verb, key, yy, MM, dd, hh, mm, ss, SSS, customer_id)
            return record
       
        elif event_type == "ORDER":
            #Update the order_list
            self.order_list.add(key)  
            amount = "%.2f" % random.uniform(1, 43.96)
            
            #if key in self.order_list:
            #    verb = "UPDATE"
            record = '{{"type": "{}", "verb": "{}", "key": "{}", "event_time": "{}-{}-{}T{}:{}:{}.{}Z", "customer_id": "{}", "total_amount": "{} USD"}}'.format(
                        event_type, verb, key, yy, MM, dd, hh, mm, ss, SSS, customer_id, amount)
            return record

def generate(num):
    g = Data_Generator()
    path = "../input/"
    temp= open("../sample_input/events.txt","r")
    with open(path + 'events_{}.txt'.format(num), 'w') as f:
        f.write(temp.read())
        f.seek(0,2)
        size=f.tell()
        f.truncate(size-1)
        events = ','
        for i in range(0, num):
            events = events + g.events() + ','
        events=events[:-1]+']'
        f.write(events)
    f.close()
    temp.close()
if __name__ == "__main__":
    generate(30)
    generate(100)       
