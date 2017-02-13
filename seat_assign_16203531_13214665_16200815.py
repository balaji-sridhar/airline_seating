# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 22:38:31 2017

@author: SubramanianB and MeadsA
"""
import sqlite3 as sq
import csv

# This class is to allocate the flight tickets by reading the database fine
# Following are the list of functions that needs to be part of this application
# Reading the csv file and loading them in arrary/set
# Query the database to find the seating availability
# Query to update the reports- number of seats allocated to rejection
# Seat allocation function
# 	-- Find the next available sequence
# 	-- If not check if the number total number of seats available is greater than request
# 	-- If not reject the input
# Below are list of TODO:
# Unit testing to be part of this submission
# Comments needs to be incorporated
#  

#TODO: update the 1st line of the comment below
"""

    1.Define three dictinary, which contains the seating layout
        - seating_dict should contain the seating layout, 
        - row_together_avail number of seats continiously available in each row
        - row_avail_dict number of seats available in the row
    2.Define a variable total_avail to check total number of seats avaiable in the flight
    3.Load the seating_dict from the database
        - refresh/update this dict everytime the database is udpated
    4.For each reservation request
        - Update the reporting table 1) No:of rejection 2) No:of passengers seated away
        - In case of successful reservation request, upate the seating table
        - update the following variable (total_avail, row_avail_dict and row_together_avail)
            
"""
# TODO: Define the structure of the dictionry/hashmap
#       - 

# Definining global variables
seating_layout = []
seating_avail = {}
consecutive_seats = []
separated_seats = []
seating_pattern = 'ABCDEF'
total_rows = 15

# TODO: Parametrise the filename
def read_bookings(inp_fname = 'bookings.csv' ):
    """
        read_bookings - Reads the csv files and will invoke the reservation function for every row in the file
        :param inp_fname: name of the booking csv file to be read
        
    """
    #TODO: Add call to the resevation function
    bookingFile = open(inp_fname)
    bookingReader = csv.reader(bookingFile)
    for row in bookingReader:
        print("Value of " , str(bookingReader.line_num) , " th row is" ,  str(row)  )
       

if __name__ == "__main__":
    """
        This is the main function and its invoked by default when the python script is executed. Here lies the configuration 
        to starting point of the reservation system.
        
    """
    
    read_bookings()
    