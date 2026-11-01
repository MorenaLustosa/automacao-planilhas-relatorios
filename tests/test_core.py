import unittest
import pandas as pd
from core import process,to_excel

class TestAutomation(unittest.TestCase):
    def test_duplicate_and_bad_date(self):
        df=pd.DataFrame([{'data':'2026-10-01','setor':'A','indicador':'B','valor':90,'meta':80},{'data':'2026-10-01','setor':'A','indicador':'B','valor':90,'meta':80},{'data':'x','setor':'A','indicador':'B','valor':90,'meta':80}])
        clean,issues,report=process(df)
        self.assertEqual(len(clean),1)
        self.assertEqual(len(issues),2)
        self.assertEqual(report.iloc[0]['percentual_metas_atingidas'],1)
        self.assertTrue(to_excel(clean,issues,report).startswith(b'PK'))

if __name__=='__main__': unittest.main()
