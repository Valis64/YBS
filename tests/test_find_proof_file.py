import unittest
import tempfile
import os
from order_gui import find_proof_file

class FindProofFileTest(unittest.TestCase):
    def test_find_proof_recursive(self):
        with tempfile.TemporaryDirectory() as tmp:
            month_dir = tmp
            order_dir = os.path.join(month_dir, "Company", "12345")
            proof_dir = os.path.join(order_dir, "proof")
            os.makedirs(proof_dir)
            fname = "12345.1-test.pdf"
            open(os.path.join(proof_dir, fname), "w").close()

            path = find_proof_file(month_dir, "12345", 1)
            self.assertEqual(path, os.path.join(proof_dir, fname))

if __name__ == "__main__":
    unittest.main()
