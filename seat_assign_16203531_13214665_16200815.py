# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 22:38:31 2017

@author: SubramanianB,ShaliniS and MeadsA
"""
import sqlite3 as sq
import csv
import unittest
from shutil import copyfile
import os

# This class is to allocate the flight tickets by reading the database fine
# Following are the list of functions that needs to be part of this application
# Reading the csv file and loading them in arrary/set
# Query the database to find the seating availability
# Query to update the reports- number of seats allocated to rejection
# Seat allocation function
# 	-- Find the next available sequence
# 	-- If not check if the number total number of seats available is greater than request
# 	-- If not reject the input
#


class AirlineReservation:
    # Defining global variables
    seating_layout = []         # Contains the seating layout of the flight
    seating_avail = {}          # Contains the seating availability, i.e snapshot of database
    consecutive_seats = []      # List to store consecutive seats for reservation
    separated_seats = []        # List to store separated seats for reservation
    seating_pattern = 'ACDEF'   # Seating pattern of rows in the flight or columns in flight
    total_rows = 15             # Total number of rows available in flight
    total_noof_reservations = 0 # Total number of seats reserved in database
    total_noof_refusal = 0      # Tracks the number of seats/passengers that application refused to allocate seat
    total_noof_separation = 0    # Tracks the number of passenger allocated seats away for their group
    total_noof_reservation_req = 0  # Total number of requests handled by the application in a session

    def load_seating_layout(self, db_name='airline_seating.db'):

        """
            load_seating_layout - This is used to store the flight plan into a variable
            and verify if the number of seats in the booking can be accommodated
            continuously.
        """

        conn = sq.connect(db_name)  # Connect to the database
        curs = conn.cursor()        # Open the cursor for executing query
        # Iterate over the table, loads the first row to determine flight layout
        # We assume that number of rows and column pattern is defined in first row or only one row is available
        for rows in curs.execute('SELECT * FROM rows_cols'):
            # print(rows)
            row_no = rows[0]    # No: of rows in the flight
            seats = rows[1]     # Column pattern for each row
            if row_no in self.seating_layout:
                print(" row already exist in the seating layout")
            else:
                self.seating_layout.append((row_no, seats))
        # print("Seating layout loaded is: ", self.seating_layout)
        conn.close()

    def load_seating_avail(self, db_name='airline_seating.db'):
        """
            load_seating_avail - This function is used to query the database to retrieve the availability
            :param db_name: Name of the database file to be processed

        """
        conn = sq.connect(db_name)
        # print("Connection value",conn)
        curs = conn.cursor()
        # Iterate over seating table and load the current availability.
        for rows in curs.execute('SELECT * FROM seating'):
            row_num = rows[0]           # Row number
            seat_num = rows[1]          # Column number
            passenger_name = rows[2]    # Passenger name
            # print(row_num, seat_num, passenger_name )

            # Check if the row exist in the list, if not create one
            if self.seating_avail.__contains__(row_num):
                self.seating_avail[row_num][seat_num] = passenger_name
            else:
                self.seating_avail[row_num] = {}
                self.seating_avail[row_num][seat_num] = passenger_name
        # print("Loaded seating layout is: ", self.seating_avail )
        conn.close()

    def insert_dbrecord(self, query, values, db_name='airline_seating.db'):
        """
            insert_dbrecord - Inserts records into the database. Takes query to be executed and the values to be inserted
            as the parameters.
            :param query: Contains the SQLite query that needs to be executed
            :param values: Contains the list of the values to be passed on the query before execution
            :param db_name: Name of the database file to be processed

        """
        conn = sq.connect(db_name)      # Connect to the database
        # Check if the query passed is not empty, if not execute the query
        if query != '' and query is not None:
            conn.execute(query, values)     # Execute the query
            conn.commit()                   # Commit the transaction
        else:
            print("Empty sql sent for execution")
        conn.close()    # Close the database connection

    def update_report(self, refused=0, separated=0, db_name='airline_seating.db'):
        """
            Increases the number of refused and separated passengers in the metrics table
            :param refused: contains number of passengers refused
            :param separated: contains number of passengers whose allocation is separated
            :param db_name: Name of the database file to be processed
            Sample insert query : insert into metrics (passengers_refused, passengers_separated) values (1,2)

        """
        # Query to update the metrics, for each update_report call new row is appended
        query = '''insert into metrics (passengers_refused, passengers_separated) values (?,?);'''
        values = (refused, separated)
        # Calling insert_dbrecord to update values in the database
        self.insert_dbrecord(query, values,db_name)

    def update_seating(self, passenger_name, rowno, seat, db_name = 'airline_seating.db'):
        """
            update_seating - Updates the seating table using update sql query. Take row no and seat and find the corresponding
            row from the table and updates the Passenger name against it.
            :param passenger_name: Name of the passenger against which reservation has to made
            :param rowno: Row number where the reservation has to made
            :param seat: Seat number of the reservation to be made
            :param db_name: Name of the database file to be processed
            Sample update query: update seating set name="Testing_Reservation1"  where row = 1 and seat = 'A';

        """
        # Query to update the seating table. Here for the selected row, passenger name is updated
        # If passenger name is empty, its assumed as availability
        query = ''' update seating set name= ?  where row = ? and seat = ? ; '''
        value = (passenger_name, rowno, seat)
        # Calling the insert_dbrecord() to update the seat allocation
        self.insert_dbrecord(query, value, db_name)      # Executing query for reservation of seat

    def check_seating_avail(self, passenger_count, seating_avail, seating_pattern):
        """
            check_seating_avail - Will iterate to all the rows and check if the seats can be allocated together
            1. Checks for togetherness
            2. Checks if the number seats can be allocated randomly
            3. Return the seats that can booked
        """
        # Objective of this function is of two fold, we achieve this by iterating the seating_avail list
        # 1. Find if at-least requested number of consecutive number of seats are available.
        # 2. Find if at-least requested number of seats available, even if its not consecutive

        self.consecutive_seats.clear()      # Tuples to store consecutive seats
        self.separated_seats.clear()        # Tuples to store non-consecutive seats
        # print("______________",self.seating_avail)
        # Iterating over seating_avail
        for row_key, row_values in self.seating_avail.items():
            if self.consecutive_seats.__len__() >= passenger_count:
                break;  # Break the loop, found conseccutive seats
            else:
                self.consecutive_seats.clear()
                # print("Sequence broken, resetting the consecutive pattern")
            # Iterating each row
            for col in self.seating_pattern:
                # Check if passenger name is empty, this implies there is no seat allocation
                if row_values.__contains__(col):
                    if row_values[col] == "":
                        # print("Seat is available in row ", row_key, " column ", col)
                        self.consecutive_seats.append((row_key, col))
                        self.separated_seats.append((row_key, col))
                    else:
                        # Sequence broken, resetting the consecutive pattern
                        self.consecutive_seats.clear()
                        # print(self.consecutive_seats.__len__(), " Consecutive seats are: " , self.consecutive_seats)
                        # print(self.separated_seats.__len__()," Separated Seats are: ", self.separated_seats)

    def load_metrics(self, db_name='airline_seating.db'):
        """
            load_metrics : This function reads the database and recomuptes the below metrics parameter
                    total_noof_reservations => Total number of passengers reserved so far
                    total_noof_refusal => total number of rejeccted reservation, due to seat inavailability
                    toatl_noof_sepration => toatl number of passengers seprated from each other
            :param db_name: Name of the database file to be processed
        """
        # Load the metric table, iterate the rows and sum the value of each row
        # Load the seating table, count the number of empty seats (rows where passenger name is empty)

        conn = sq.connect(db_name)
        curs = conn.cursor()

        # Counting the number of reservation
        for rows in curs.execute('SELECT count(*) FROM seating where name != ""'):
            # Obtain the number of seats whose passenger name is not null or not empty
            self.total_noof_reservations = int(rows[0])
        print("Total number of reservations as of now: ", self.total_noof_reservations)

        # Counting number of rejections and separations
        # For every update metrics request, one row is added. So all the rows in metrics  table has to be summed up
        for rows in curs.execute('SELECT * FROM metrics'):
            # Two variables, one to count the number of rejection and other to count the number of passenger separation
            self.total_noof_refusal = self.total_noof_refusal + int(rows[0])
            self.total_noof_separation = self.total_noof_separation + int(rows[1])
        print("Total number of seprations :", self.total_noof_separation)
        print("Total number of refusals : ", self.total_noof_refusal)
        print("Total number of reservation requests handled in this session : ", self.total_noof_reservation_req)
        conn.close()

    def confirm_booking(self, passenger_count, passenger_name, db_name='airline_seating.db'):
        """
            confirm_booking - Does the booking confirmation if the number of seats requested are available.
            If not updates the reporting database.
            :param passenger_count: Number of passengers
            :param passenger_name: Name of the passengers
        """
        # This function servers as bulk processing or batch processing
        # Reads all the row in the passed csv file and confirms the booking
        self.load_seating_layout(db_name)      # Load seating layout
        self.load_seating_avail(db_name)       # Load seating availability
        # Check if the seats are available
        self.check_seating_avail(passenger_count, self.seating_avail, self.seating_layout[0][1])
        self.total_noof_reservation_req = self.total_noof_reservation_req + 1
        # Check if the passenger count is greater than current availability, if so update metrics for refusal
        if self.consecutive_seats.__len__() < passenger_count and self.separated_seats.__len__() < passenger_count:
            print(passenger_name, "'s Current seat availability is less than ", passenger_count, "seats")
            print("Updated the passengers_refused metrics")
            self.update_report(passenger_count, 0, db_name)
        # Check if consecutive seats are available, if so update the metrics table
        elif self.consecutive_seats.__len__() >= passenger_count:
            print("Consecutive seats are available for the reservation request")
            # Confirm seat bookings from list of consecutive seats
            for i in range(0, passenger_count):
                print(passenger_name, self.consecutive_seats[i][0], self.consecutive_seats[i][1])
                self.update_seating(passenger_name, self.consecutive_seats[i][0], self.consecutive_seats[i][1],db_name)
            print("Updated the seating table and the reservation is completed successfully")
        # If consecutive seats are not available, fall back to separated seats
        else:
            print("Consecutive seats are not available for reservation request.")
            # Confirm seat bookings from list of separated seats
            for i in range(0, passenger_count):
                print(passenger_name, self.separated_seats[i][0], self.separated_seats[i][1])
                self.update_seating(passenger_name, self.separated_seats[i][0], self.separated_seats[i][1], db_name)
            print("We will try to allocate seats as close as possible")
            print(passenger_name, "'s Updated the passengers_separated metrics ", passenger_count)
            self.update_report(0, passenger_count, db_name)

    def read_bookings(self, inp_fname='bookings.csv', db_name='airline_seating.db'):
        """
            read_bookings - Reads the csv files and will invoke the reservation function for every row in the file
            :param inp_fname: name of the booking csv file to be read
            :param db_name: Name of the database file to be processed

        """
        # Iterates over the csv file. If the file name is not available, falls back to booking.csv file
        total_pass_in_req = 0
        bookingFile = open(inp_fname)   # Opens the csv input file
        bookingReader = csv.reader(bookingFile) # Uses csv reader to parse the lines
        # Iterates each line and issues request to confirm the booking
        for row in bookingReader:
            # print("Value of " , str(bookingReader.line_num) , " th row is" ,  str(row)  )
            total_pass_in_req = total_pass_in_req + int(row[1])
            self.confirm_booking(int(row[1]), row[0],db_name)

        print("Number of passegers in the csv file :", total_pass_in_req)
        self.load_metrics(db_name)  # Now load the metrics


if __name__ == "__main__":
    """
        This is the main function and its invoked by default when the python script is executed. Here lies the configuration
        to starting point of the reservation system.

    """
    print("Loading the classes")
    airlineReserv = AirlineReservation()
    airlineReserv.read_bookings()