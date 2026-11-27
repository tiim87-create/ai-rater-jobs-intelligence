import unittest
from build_market_snapshots import build_snapshot

class SnapshotTests(unittest.TestCase):
    def test_partial_and_multicountry(self):
        at = "2026-11-27T00:00:00+00:00"
        jobs = [
            {"id":"a","vendor":"RWS","status":"active","countries":["US","CA"],"project_family":"Search"},
            {"id":"b","vendor":"RWS","status":"archived","countries":["FR"]},
            {"id":"c","vendor":"TELUS","status":"active","countries":["DE"]},
        ]
        summary = {"generated_at":at,"sources":{"RWS":{"status":"ok"},"TELUS":{"status":"stale"}}}
        events = [{"id":"b","at":at,"type":"archived"},{"id":"a","at":at,"type":"reopened"}]
        s = build_snapshot(jobs,summary,events)
        self.assertFalse(s["complete"])
        self.assertEqual(s["observed_active_listings"],1)
        self.assertEqual(s["observed_countries"],["CA","US"])
        self.assertIsNone(s["vendors"]["TELUS"]["active_listings"])
        self.assertEqual(s["vendors"]["TELUS"]["retained_active_listings"],1)
        self.assertEqual(s["vendors"]["RWS"]["events"],{"archived":1,"reopened":1})
        self.assertEqual(s["vendors"]["RWS"]["country_associations"],{"US":1,"CA":1})

if __name__ == "__main__":
    unittest.main()
