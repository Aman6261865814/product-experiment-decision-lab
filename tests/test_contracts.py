import sys, unittest, sqlite3, json
from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from common import load_clean

class DataContractTests(unittest.TestCase):
    def test_conflicting_duplicates_rejected(self):
        with self.assertRaises(ValueError): load_clean(pd.DataFrame({'id':[1,1],'value':[2,3]}),['id'])
    def test_exact_retry_removed(self):
        clean,n=load_clean(pd.DataFrame({'id':[1,1],'value':[2,2]}),['id'])
        self.assertEqual((len(clean),n),(1,1))
    def test_null_key_rejected(self):
        with self.assertRaises(AssertionError):load_clean(pd.DataFrame({'id':[None]}),['id'])
    def test_srm_blocks_launch(self):
        from pipeline import evaluate
        d=pd.read_csv(ROOT/'data/processed/fact_experiment.csv')
        bad=pd.concat([d[d.variant=='control'],d[d.variant=='treatment'].iloc[:300]])
        self.assertTrue(evaluate(bad)['decision'].startswith('INVALID'))
    def test_zero_effect_does_not_ship(self):
        from pipeline import evaluate
        d=pd.DataFrame({'variant':['control']*200+['treatment']*200,'converted':([0]*180+[1]*20)*2,'crashed':([0]*196+[1]*4)*2})
        self.assertEqual(evaluate(d)['decision'],'HOLD')
    def test_sql_python_parity(self):
        a=pd.read_csv(ROOT/'reports/sql_result.csv');b=pd.read_csv(ROOT/'data/processed/variant_metrics.csv')
        np.testing.assert_allclose(a.conversion_rate,b.conversion_rate)
    def test_randomization_unit(self):
        d=pd.read_csv(ROOT/'data/processed/fact_experiment.csv')
        self.assertTrue(d.user_id.is_unique);self.assertTrue(d.converted.isin([0,1]).all())
    def test_swap_arms_flips_effect(self):
        from pipeline import evaluate
        d=pd.read_csv(ROOT/'data/processed/fact_experiment.csv');a=evaluate(d)
        d.variant=d.variant.map({'control':'treatment','treatment':'control'});b=evaluate(d)
        self.assertAlmostEqual(a['conversion_delta_pp'],-b['conversion_delta_pp'])
