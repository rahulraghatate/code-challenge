#ShutterFly Code Challenge.
##Problem Statement: Program to Ingest and Process Shutterfly Events data and to find top X customers by life time value

####Python version: Python 3.6

###Implementation(Current):
  1. Events are received from a input source as a set of files and processed one after the other and placed into database record by record.
     Input Files('../input/'):
     a. events.txt
     b. events1.txt
  2. If the records in any file are repeating, they are taken care while updating the database by dropping the duplicates.
  3. Tables as dataframes implemented: CUSTOMER,ORDER,SITE_VISIT,IMAGE
  4. After the Ingestion of events,Customer life time value(LTV_value) is calculated and maintained in LTV_Table table.
  5. LTV_Table is used for querying the top X customers by LTV_value.
     Output_File('../output/'):
     a. output.txt
     Data Format:
     customer_id	customer_last_name	total_revenue	total_visits	LTV_Value
     
  6. Any number of 
     Ingest(e,D) function call can be performed to update the datastore and  
     TopXSimpleLTVCustomers(x, D) to request top x customer by LTV_Value
                        
                        
###In Progress/Future Work:   
   1. Implementation of Referential Integrity in database management, by implementing DQ_check function to check for valid records before ingesting and create Log_files for every ingest activity.
   2. Also, Events can be processed in parallel by different threads, therefore multi connections can be establish for multiple sources.
   3. Implemetation of Slowly changing Dimension (SCD) - Type 3 for better database management and analytics results
   4. LTV table is created every_single time by processing all the records. Instead, delta update can be done only to update records for which customer activity happened recently.
                        

##Code_structure

Ingest(e,D)--> Ingest(file_path, exising Database)
        D <-- input the new events from raw_file
        customer <-- (existing + new) customers
        site_visit <-- existing + new site_visit
        order  <-- existing + new orders
        image  <-- existing + new images
    
TopXSimpleLTVCustomers(x,D) -->
        Update the Order table
        Total_revenue by each customer
        Total site_visit by customer
        List of Customers
        Calculate --> rev_per_visit=total_revenue/total_visits
        Calculate --> visits_per_wk=total_visits/num_weeks
        Calculate --> LTV_Value=rev_per_visit * visit_per_wk * 52 * 10(average lifespan for Shutterfly)
        Update the LTV_Table
        Write to Output_File
