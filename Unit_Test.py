import unittest
import os
from converter import md_to_pdf


class TestMdToPdf(unittest.TestCase):
    def test_md_to_pdf(self):
        input_file = "test.md"
        output_file = "test_output.pdf"

        with open(input_file, "w") as f:
            f.write("# Test\nThis is a test.")

        md_to_pdf(input_file, output_file)

        self.assertTrue(os.path.exists(output_file))

        os.remove(input_file)
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()