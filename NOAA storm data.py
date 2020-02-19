#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:58:07 2020

@author: geraldsteven
"""

#Database Design and Implementation
#Professor Engel
#Gerald Steven
#Assignment 2

#Data source: (downloaded 02/08/20)
#National Oceanic and Atmospheric Administration (NOAA)
#https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/
#File name: StormEvents_details-ftp_v1.0_d2008_c20180718.csv


#FIVE MODIFICATIONS
#1. drop selected columns
#2. add computed columns
#3. replace empty values with N/A
#4. rename column titles
#5. only write unique records (i.e. delete records that are duplicates)

#PART I: DATA RETRIEVAL
import csv
def file_prepare():
    source_file = "StormEvents_details-ftp_v1.0_d2008_c20180718.csv"
    
    lines_written, lines_read = 0, 0
    
    try:
        in_file = open(source_file, 'r')
    except:
        print("The file could not be found or could not be opened")
    else:
        reader = csv.reader(in_file, skipinitialspace=True)
        
        out_file_name = 'Storm_details_2008.csv'
        out_file      = open(out_file_name,'w')

        writer = csv.writer(out_file, delimiter=",")
        
        #create an empty list that will store unique episode_id for modification 5
        all_episodes = []
        
        #loop through all records/rows
        for line in reader:
            lines_read += 1
            
            
            #PART II: DATA MANIPULATION
            #MODIFICATION 1: DROP SELECTED COLUMNS
            #the NOAA csv file has 51 columns, but we only care about some of them
            #use indexing to select certain columns
            episode_id = line[6]
            event_id = line[7]
            state_id = line[8]
            month_name = line[11] #year is not included because data is only from 2008
            event_type=line[12]
            injuries_direct = line[20] #data type is str
            injuries_indirect = line[21]
            deaths_direct = line[22]
            deaths_indirect = line[23]
            episode_narrative = line[48]
            event_narrative = line[49]
            
            
            #MODIFICATION TWO: ADD COLUMNS FOR TOTAL INJURIES AND TOTAL DEATHS
            #int with base 32, otherwise error
            total_injuries = int(injuries_direct, 32) + int(injuries_indirect, 32)
            total_deaths = int(deaths_direct, 32) + int(deaths_indirect, 32)
            
            
            #MODIFICATION THREE: REPLACE EMPTY VALUES WITH N/A
            #some entries for episode_narrative and event_narrative are blank
            #e.g.: the event_narrative for record 1 is blank
            #if blank, replace with "N/A"
            if episode_narrative == "":
                episode_narrative = "N/A"
            
            if event_narrative == "":
                event_narrative = "N/A"
            
            #MODIFICATION FOUR: RENAME COLUMN TITLES
            #before this modification, these variables took integer values
            #so they had to be renamed
            if lines_written == 0:
                total_injuries = "TOTAL_INJURIES"
                total_deaths = "TOTAL_DEATHS"
            
            #gather selected columns into one variable
            value = episode_id, event_id, state_id, month_name, event_type, injuries_direct, injuries_indirect, total_injuries, deaths_direct, deaths_indirect, total_deaths, episode_narrative, event_narrative
            
            
            #MODIFICATION FIVE: ONLY WRITE UNIQUE RECORDS
            #some records are duplicates as they have the exact same episode_narrative and event_narrative
            #duplicate records will have the same episode_id
            #so create an empty string that will store all unique episode_id
            #when iterating through the loop, if the episode_id is not in the list (i.e. unique)
            #write the value into the file
            #and append episode_id to the list so that duplicates will not be added

            if episode_id not in all_episodes:
                writer.writerow(value) #write variable into one record
                all_episodes += [episode_id] #append to list
            
                lines_written += 1
                
        out_file.close()
        in_file.close()
        print("Lines read: ", lines_read)
        print("Lines written: ",lines_written)
                
        
file_prepare()






