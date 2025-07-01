import unittest
import tempfile
from pathlib import Path

from preset_ybs import fetch_art


class FetchArtTest(unittest.TestCase):
    def test_month_dir_pairs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            month_dir = Path(tmpdir)
            order_root = month_dir / "56789" / "proof"
            order_root.mkdir(parents=True)

            pair1 = order_root / "56789.1.pdf"
            pair2 = order_root / "56789.2.pdf"
            pair1.write_text("a")
            pair2.write_text("b")

            settings = {"month_dir": str(month_dir)}
            self.assertEqual(fetch_art(settings, "56789", 1), pair1.resolve())
            self.assertEqual(fetch_art(settings, "56789", 2), pair2.resolve())

    def test_recycle_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            month_dir = Path(tmpdir)
            recycle = month_dir / "12345" / "proof" / "$Recycle.Bin"
            recycle.mkdir(parents=True)
            bad = recycle / "12345.1.pdf"
            bad.write_text("x")

            settings = {"month_dir": str(month_dir)}
            with self.assertRaises(ValueError):
                fetch_art(settings, "12345", 1)


if __name__ == "__main__":
    unittest.main()
