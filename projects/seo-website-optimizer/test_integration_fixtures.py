import unittest
from extractor import extract_observation
from fixtures import FIXTURES
from engine import site_fingerprint, classify_change

URL="https://example.com/"

class IntegrationFixtureTests(unittest.TestCase):
    def obs(self,name): return extract_observation(FIXTURES[name],URL)
    def test_f01_baseline_extract(self):
        o=self.obs("F01_baseline"); self.assertEqual(o["title"],"Acme"); self.assertIn("H1: Acme Services",o["headings"]); self.assertIn("Organization",o["structured_data"])
    def test_f02_noindex_extract(self): self.assertIn("noindex",self.obs("F02_noindex")["robots"])
    def test_f03_no_description(self): self.assertEqual(self.obs("F03_no_description")["meta_description"],"")
    def test_f04_no_canonical(self): self.assertEqual(self.obs("F04_no_canonical")["canonical"],"")
    def test_f05_missing_h1(self): self.assertIn("H1: ",self.obs("F05_missing_h1")["headings"])
    def test_f06_missing_alt(self): self.assertEqual(self.obs("F06_missing_alt")["images"][0][1],"")
    def test_f07_broken_cta(self): self.assertEqual(self.obs("F07_broken_cta")["forms"],[])
    def test_f08_no_viewport(self): self.assertEqual(self.obs("F08_no_viewport")["viewport"],"")
    def test_f09_no_schema(self): self.assertEqual(self.obs("F09_no_schema")["structured_data"],[])
    def test_f10_multilingual(self): self.assertEqual(self.obs("F10_multilingual_zh")["lang"],"zh-TW")
    def test_f11_f12_price_change_material(self):
        a=self.obs("F11_price_v1"); b=self.obs("F12_price_v2")
        self.assertEqual(classify_change([a],[b]),"MATERIAL_SCORING_RELEVANT_CHANGE")
        self.assertNotEqual(site_fingerprint([a]),site_fingerprint([b]))
    def test_repeated_extraction_stable(self):
        a=self.obs("F01_baseline"); b=self.obs("F01_baseline"); self.assertEqual(site_fingerprint([a]),site_fingerprint([b]))

if __name__=="__main__": unittest.main(verbosity=2)
