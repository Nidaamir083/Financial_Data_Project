import unittest
import pandas as pd
from src.core_logic import read_excel_file, summarize_dataframe

class TestCoreLogic(unittest.TestCase):

    def test_summarize_dataframe(self):
        data = {'A': [1, 2, None], 'B': [4, 5, 6]}
        df = pd.DataFrame(data)
        summary = summarize_dataframe(df)
        self.assertEqual(summary['shape'], (3, 2))
        self.assertIn('A', summary['nulls'])
        self.assertEqual(summary['nulls']['A'], 1)

if __name__ == '__main__':
    unittest.main()
