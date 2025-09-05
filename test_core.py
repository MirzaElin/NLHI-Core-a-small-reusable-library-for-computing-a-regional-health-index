import pandas as pd
from nlhi import core

def test_units_and_compute():
    df = pd.DataFrame([
        {'name':'Resp','tliphs':365.25,'unit':'Day(s)','mortality':10},
        {'name':'Cardio','tliphs':52.1429,'unit':'Week(s)','mortality':5},
        {'name':'Neuro','tliphs':12,'unit':'Month(s)','mortality':2},
        {'name':'Other','tliphs':1,'unit':'Year(s)','mortality':1},
    ])
    rec = core.compute_record(age=40.0, population=1000.0, life_expectancy=80.0, domains_df=df)
    for d in rec['domains']:
        assert abs(d['TLIPHS_years'] - 1.0) < 1e-3
    assert 'NLHI' in rec and rec['NLHI'] > 0.0

def test_negative_le_minus_age_allowed():
    df = pd.DataFrame([{'name':'X','tliphs':0,'unit':'Year(s)','mortality':1}])
    rec = core.compute_record(age=80.0, population=1000.0, life_expectancy=75.0, domains_df=df)
    assert rec['domains'][0]['DSTLYA'] <= 0
