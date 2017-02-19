# airline_seating
Airline seating reservation system 
In the first section of our code we have defined a class which will allocate the flight tickets by reading the database file.After reading the file we need to perform the seat allocation function i.e we need to find the next available sequence of seating, also we need to check if the number of seats available is greater than the request.If these two criterias are not satisfied we need to reject the request.
In our code we have defined three dictionary which contains the seating layout.These are seating_dict which contains the seating layout, row_together_avail which contains the number of seats continuously available in each row and row_avail_dict which contaons the number of seats available in the row.
As we are loading the seating_dict from the database we are refreshing  and updating the database everytime.
For each reservation request we are upating the reporting table for the number of rejections and for the number of passengers seated away.
For the successful reservation request we are updating the seating table.
In our code after reading the csv file we have a fuction load_seating_layout which is used for storing the seat plans into variable and also verify if the number of seats of the booking can be accomodate continuously.
load_seat_avail function checks the availability. 
The records are inserted in the database by using the insert_dbrecord. According the number of refused and seperated passengers the metrics tables are updated.
The function confirm_booking does the booking confirmation if the number of seats are avaible otherwise it updates the reporting databases.
We also have check_seating_avail function which checks for the seats which can be allocated together.This function iterates the rows and check if the number of seats can be allocated together and also checks for the seats which can be allocated randomly. At the end it returns the seats that can be booked.
