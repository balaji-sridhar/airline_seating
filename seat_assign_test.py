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
        # Given - When the flight booking is empty
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


if __name__ == '__main__':
    unittest.main()