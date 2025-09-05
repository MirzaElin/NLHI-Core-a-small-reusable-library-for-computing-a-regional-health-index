import pandas as pd
from nlhi import core, io

def test_store_roundtrip(tmp_path):
    store_path = tmp_path/'s.json'
    store = io.Store(str(store_path))
    df = pd.DataFrame([{'name':'R','tliphs':120,'unit':'Day(s)','mortality':12}])
    rec = core.compute_record(32.5, 52000, 80.7, df)
    store.upsert('Avalon','2025-06-01',rec)
    out = io.Store(str(store_path)).time_series('Avalon')
    assert len(out) == 1 and 'NLHI' in out[0]
