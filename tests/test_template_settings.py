import unittest
from order_gui import load_template_settings

class TemplateSettingsTest(unittest.TestCase):
    def test_rt3055_rotation(self):
        settings = load_template_settings("RT3055")
        self.assertEqual(settings.get("rotation"), 270)

    def test_tt3055_rotation(self):
        settings = load_template_settings("TT3055")
        self.assertEqual(settings.get("rotation"), 270)

    def test_pb004_rotation(self):
        settings = load_template_settings("PB004")
        self.assertEqual(settings.get("rotation"), 180)

    def test_rt3722_rotation(self):
        settings = load_template_settings("RT3722")
        self.assertEqual(settings.get("rotation"), 90)

if __name__ == "__main__":
    unittest.main()
