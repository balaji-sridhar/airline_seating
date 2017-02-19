# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 22:38:31 2017

@author: SubramanianB,ShaliniS and MeadeA
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
       

def load_seating_layout(db_name='airline_seating.db'):
    
    """load_seeating_layout - This is used to store the flight plan into a variable 
        and verify if the number of seats in the booking can be accomodated
        continiously. """

    conn = sq.connect(db_name)
    curs = conn.cursor()
    for rows in curs.execute('SELECT * FROM rows_cols'):
        row_no = rows[0]
        seats = rows[1]
        if(row_no in seating_layout):
            print(" row already exist in the seating layout")
        else:
            seating_layout.append((row_no, seats))
    print("Seating layout loaded is: ", seating_layout)

def load_seating_avail(db_name='airline_seating.db'):
    """ 
        load_seating_avail - This function is used to query the database to retrieve the availability
        :param db_name: Name of the database file to be processed
        
    """
    # TODO: First read the database and store it hash map
    conn = sq.connect(db_name)
    print("Connection value",conn)
    curs = conn.cursor()
    for rows in curs.execute('SELECT * FROM seating'):
        row_num = rows[0]
        seat_num = rows[1]
        passenger_name = rows[2]
        print(row_num, seat_num, passenger_name )
        
        if seating_avail.__contains__(row_num):
            seating_avail[row_num][seat_num] = passenger_name 
        else:
            seating_avail[row_num] = {}
            seating_avail[row_num][seat_num] = passenger_name 
    print("Loaded seating layout is: ", seating_avail )
    conn.close()    

def insert_dbrecord(query, values, db_name='airline_seating.db' ):
    """
        insert_dbrecord - Inserts records into the database. Takes query to be executed and the values to be inserted
        as the parameters.
        :param query: Contains the SQLite query that needs to be executed 
        :param values: Contains the list of the values to be passed on the query before execution
        :param db_name: Name of the database file to be processed
        
    """
    conn = sq.connect(db_name)
    if(query != '' and query!= None):
        conn.execute(query, values)
        conn.commit()
        print("Updated the record into database sucessfully")
    else:
        print("Empty sql sent for execution")
    conn.close()
    
def update_report(refused = 0,separated = 0, db_name='airline_seating.db'):
    """
        Increases the number of refused and seprated passengers in the metrics table
        :param refused: contains number of passengers refused
        :param seprated: contains number of passengers whoes allocation is seprated
        :param db_name: Name of the database file to be processed
        Sample insert query : insert into metrics (passengers_refused, passengers_separated) values (1,2)
        
    """       
    query = '''insert into metrics (passengers_refused, passengers_separated) values (?,?);'''
    values = (refused, separated)
    #Calling insert_dbrecord to update values in the database
    insert_dbrecord(query,values)
    
def update_seating(passenger_name, rowno, seat):
    """
        update_seating - Updates the seating table using update sql query. Take row no and seat and find the corresponding
        row from the table and updates the Passenger name against it.
        :param passenger_name: Name of the passenger against which reservation has to made
        :param rowno: Row number where the reservation has to made
        :param seat: Seat number of the reservation to be made
        Sample update query: update seating set name="Testing_Reservation1"  where row = 1 and seat = 'A';
        
    """
    query = ''' update seating set name= ?  where row = ? and seat = ? ; '''
    value = (passenger_name, rowno, seat)
    #Calling the inser_dbrecord() to update the seat allocation
    insert_dbrecord(query,value)    
    
def confirm_booking(passenger_count, passenger_name ):
    """
        confirm_booking - Does the booking confirmation if the number of seats requested are available. 
        If not updates the reporting database.
        :param passenger_count: Number of passengers
        :param passenger_name: Name of the passengers
    """
    load_seating_layout()
    load_seating_avail()
    check_seating_avail(passenger_count,seating_avail,seating_layout[0][1])
    if (consecutive_seats.__len__() < passenger_count and separated_seats.__len__() < passenger_count):
        print("Current seat availability is less than ", passenger_count ,"seats")
        print("Updated the passengers_refused metrics")
        update_report(passenger_count)
    elif (consecutive_seats.__len__() >= passenger_count ):
        print("Consecutive seats are available for the reservation request")
        for i in range(0, passenger_count):
            print(passenger_name, consecutive_seats[i][0], consecutive_seats[i][1])
            update_seating(passenger_name, consecutive_seats[i][0], consecutive_seats[i][1])
        print("Updated the seating table and the reservations are completed successfully")
    else:
        print("Consecutive seats are not available for reservation request.")
        for i in range(0, passenger_count):
            print(passenger_name, separated_seats[i][0], separated_seats[i][1])
            update_seating(passenger_name, separated_seats[i][0], separated_seats[i][1])
        print("We will try to allocate seats as close as possible")
        print("Updated the passengers_separated metrics")
        
def check_seating_avail(passenger_count,seating_avail,seating_pattern):
    """
        check_seating_avail - Will iterate to all the rows and check if seats can be allocated together
        1. Checks if the number seats can be allocated together
        2. Checks if the number seats can be allocated randomly
        3. Return the seats that can booked
    """
    consecutive_seats.clear()
    separated_seats.clear()
    print("______________",seating_avail)
    for row_key, row_values in seating_avail.items():
        print(row_key)
        if(consecutive_seats.__len__() >= passenger_count ):
            break;
        else:
            consecutive_seats.clear()
            print("Sequence broken, resetting the consecutive pattern")
                     
    for col in seating_pattern:
        if(row_values.__contains__(col)):
            if ( row_values[col] == ""):
                print("Seat is available in row ", row_key, " column ", col)
                consecutive_seats.append((row_key, col))
                separated_seats.append((row_key, col))
            else:
                print("Sequence broken, resetting the consecutive pattern")
                consecutive_seats.clear()
        print(consecutive_seats.__len__(), " Consecutive seats are: " , consecutive_seats)
    print(separated_seats.__len__()," Separated seats are: ", separated_seats)    
    
if __name__ == "__main__":
    """
        This is the main function and its invoked by default when the python script is executed. Here lies the configuration 
        to starting point of the reservation system.
        
    """
    
    read_bookings()
    
