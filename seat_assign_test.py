import unittest
from shutil import copyfile
import os
from seat_assign_16203531_13214665_16200815 import AirlineReservation

class AirlineTests(unittest.TestCase):

    # Initialize airlineReservation object
    airlineReservation = AirlineReservation()

    def setUp(self):
        print("Copying the database file ")
        """
            Create copy of the database file and input csv file

        """
        self.airlineReservation = AirlineReservation()

    def tearDown(self):
        """
            Delete newly created database and csv
        """
        print("Removed the database file")
        del self.airlineReservation
        # os.remove('test_bookings.csv')
        # os.remove('fully_booked_seating.db')

    def test_refusal_count(self):
        self.longMessage = True
        # Given - The flight booking is empty
        # And maximum seat capacity is 60
        # And Metrics table is empty
        testdb = "test_data\\empty_seating.db"
        tempdb = "test_data\\temp_empty_seating.db"
        copyfile(testdb, tempdb)

        # When - Reservation request is issued for 100 seats
        self.airlineReservation.load_seating_avail(tempdb)
        self.airlineReservation.confirm_booking(100, "Bulk booking", tempdb)

        # Then - No seats are allocated
        # And - Metrics table is updated
        # And - Number of passenger refused count is 100
        self.airlineReservation.load_metrics(tempdb)
        self.assertEqual(100, self.airlineReservation.total_noof_refusal, 'Number of reservation refusal do not match')
        # Clean up temp database

        os.remove(tempdb)

    def test_non_consecutive_booking(self):
        self.longMessage = True
        # Given - Only 4 seats(non consecutive) are available in database
        # And Metrics table is empty
        testdb = "test_data\\non_consecutive_seating.db"
        tempdb = "test_data\\temp_non_consecutive_seating.db"
        copyfile(testdb, tempdb)
        # When - Reservation request is for 4 passenger is issued
        self.airlineReservation.load_seating_avail(tempdb)
        self.airlineReservation.confirm_booking(4, "Non_Consecutive_Test", tempdb)
        # Then - Seats are allocated to all 4 passenger
        # And - Metrics database is updated
        # And - Number of separation count is 4
        self.airlineReservation.load_metrics(tempdb)
        self.assertEqual(4, self.airlineReservation.total_noof_separation, 'Number of separation doesnt match')
        # Clean up temp database
        os.remove(tempdb)

    def test_no_seats_available(self):
        self.longMessage = True
        # Given - The flight is fully booked
        # And Metrics table is empty
        testdb = "test_data\\fully_booked_seating.db"
        tempdb = "test_data\\temp_fully_booked_seating.db"
        copyfile(testdb, tempdb)

        # When - Reservation request is for 1 passenger
        self.airlineReservation.load_seating_avail(tempdb)
        self.airlineReservation.confirm_booking(1, "No_Seats_Available", tempdb)

        # Then - No seats are allocated
        # And - Metrics database is updated
        # And - Number of refusal count is 1
        self.airlineReservation.load_metrics(tempdb)
        self.assertEqual(1, self.airlineReservation.total_noof_refusal, 'Number of reservation refusal do not match')
        # Clean up temp database
        os.remove(tempdb)

    def test_consecutive_bookings(self):
        print("Sample test")
        self.longMessage = True
        # Given - The are 4 consecutive seats and 2 non- consecutive seats available
        # And Metrics table is empty
        testdb = "test_data\\consecutive_seating.db"
        tempdb = "test_data\\temp_consecutive_seating.db"
        copyfile(testdb, tempdb)

        # When - Reservation request is issued for 4
        self.airlineReservation.load_seating_avail(tempdb)
        self.airlineReservation.confirm_booking(4, "Consecutive booking", tempdb)

        # Then - 4 consecutive seats are allocated
        # And - Metrics table is not updated
        # And - Number of passenger separation is zero
        self.airlineReservation.load_metrics(tempdb)
        self.assertEqual(0, self.airlineReservation.total_noof_separation, 'Number of separation doesnt match')
        # Clean up temp database
        os.remove(tempdb)


if __name__ == '__main__':
    unittest.main()
