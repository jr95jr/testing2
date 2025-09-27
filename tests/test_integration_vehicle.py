import unittest, sqlite3
from src.service import VehicleService

class TestVehicleIntegration(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.svc = VehicleService(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_register_and_list_inventory(self):
        vid = self.svc.register_vehicle("Toyota", "Corolla", 2020)
        self.assertIsInstance(vid, int)
        items = self.svc.inventory()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].brand, "Toyota")
        self.assertEqual(items[0].model, "Corolla")
        self.assertEqual(items[0].year, 2020)

    def test_invalid_year_raises(self):
        with self.assertRaises(ValueError):
            self.svc.register_vehicle("Ford", "T", 1800)

if __name__ == "__main__":
    unittest.main()