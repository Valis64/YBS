import unittest
from order_gui import load_workloads

class WorkloadPresetTest(unittest.TestCase):
    def test_presets_available(self):
        data = load_workloads()
        self.assertIn("YBS", data)
        self.assertIn("Vista", data)
        self.assertIn("art_dir", data["YBS"])
        self.assertIn("template_dir", data["Vista"])

if __name__ == "__main__":
    unittest.main()
