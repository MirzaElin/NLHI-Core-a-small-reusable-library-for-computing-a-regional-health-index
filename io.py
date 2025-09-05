import json, os
from typing import Dict

class Store:
    """Simple JSON store: store[region][date] = record_dict"""
    def __init__(self, path: str):
        self.path = path
        self.data = {}
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def upsert(self, region: str, date: str, record: Dict):
        self.data.setdefault(region, {})
        self.data[region][date] = record
        self._save()

    def time_series(self, region: str):
        if region not in self.data:
            return []
        pairs = sorted(self.data[region].items(), key=lambda kv: kv[0])
        return [{"date": d, "NLHI": r.get("NLHI", r.get("NLCHI", 0.0))} for d, r in pairs]

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)
