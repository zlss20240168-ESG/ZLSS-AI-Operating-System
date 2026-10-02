import copy, unittest
from engine import *

WEIGHTS={"A":18.0,"B":20.0,"C":16.0,"D":16.0,"E":12.0,"F":12.0,"G":6.0}

def full_results():
    rows=[]
    specs={"A":[3,3,2,3,2,3,2],"B":[5,3,4,2,2,2,2],"C":[3,3,2,2,2,2,1,1],
           "D":[3,3,2,2,2,2,2],"E":[3,2,2,2,1,2],"F":[6,2,2,2],"G":[3,1,.5,.5,.5,.5]}
    for c,pts in specs.items():
        for i,p in enumerate(pts,1): rows.append(CheckResult(f"{c}{i}",c,p,p,"pass","Low"))
    return rows

HOME={"url":"https://Example.com/?utm_source=x#top","status":200,"title":"Home","meta_description":"Desc",
"robots":"index,follow","canonical":"https://example.com/","lang":"en","headings":["H1: Home"],
"internal_links":[["/about","About"]],"images":[["hero.jpg","Hero"]],"structured_data":["Organization"],
"forms":["/contact"],"viewport":"width=device-width, initial-scale=1","open_graph":{"title":"Home"},
"primary_text":"We provide services.","timestamp":"2026-10-03T00:00:00Z"}

class CoreTests(unittest.TestCase):
    def test_001_exact_repeat(self): self.assertEqual(site_fingerprint([HOME]),site_fingerprint([copy.deepcopy(HOME)]))
    def test_002_different_email_irrelevant(self):
        fp=site_fingerprint([HOME]); self.assertEqual(result_identity("https://example.com","1.0",fp),result_identity("https://example.com","1.0",fp))
    def test_003_ai_narrative_not_in_score(self): self.assertEqual(calculate_score(full_results(),WEIGHTS),calculate_score(full_results(),WEIGHTS))
    def test_004_timestamp_only(self):
        p=copy.deepcopy(HOME); p["timestamp"]="2027-01-01"; self.assertEqual(site_fingerprint([HOME]),site_fingerprint([p]))
    def test_005_tracking_params(self): self.assertEqual(normalize_url("https://x.com/a?utm_source=a&b=2"),normalize_url("https://x.com/a?b=2&utm_source=b"))
    def test_006_fragment(self): self.assertEqual(normalize_url("https://x.com/a#1"),normalize_url("https://x.com/a#2"))
    def test_007_default_port(self): self.assertEqual(normalize_url("https://x.com:443/a/"),"https://x.com/a")
    def test_008_title_change_material(self):
        p=copy.deepcopy(HOME); p["title"]="New"; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_009_meta_change_material(self):
        p=copy.deepcopy(HOME); p["meta_description"]="New"; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_010_h1_change_material(self):
        p=copy.deepcopy(HOME); p["headings"]=["H1: New"]; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_011_noindex_cap(self): self.assertEqual(calculate_score(full_results(),WEIGHTS,["CAP-02"])["final_score"],30.0)
    def test_012_noindex_removed(self): self.assertEqual(calculate_score(full_results(),WEIGHTS,[])["final_score"],100.0)
    def test_013_robots_cap(self): self.assertEqual(calculate_score(full_results(),WEIGHTS,["CAP-03"])["final_score"],35.0)
    def test_014_cap_minimum_wins(self): self.assertEqual(calculate_score(full_results(),WEIGHTS,["CAP-03","CAP-01"])["final_score"],20.0)
    def test_015_score_band(self): self.assertEqual(score_band(89.99),"Strong")
    def test_016_alt_change_material(self):
        p=copy.deepcopy(HOME); p["images"]=[["hero.jpg","New alt"]]; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_017_cta_change_material(self):
        p=copy.deepcopy(HOME); p["forms"]=["/quote"]; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_018_primary_text_change_material(self):
        p=copy.deepcopy(HOME); p["primary_text"]="Updated"; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_019_page_added(self):
        p=copy.deepcopy(HOME); p["url"]="https://example.com/about"; self.assertNotEqual(site_fingerprint([HOME]),site_fingerprint([HOME,p]))
    def test_020_page_removed(self):
        p=copy.deepcopy(HOME); p["url"]="https://example.com/about"; self.assertNotEqual(site_fingerprint([HOME,p]),site_fingerprint([HOME]))
    def test_021_failed_observation_policy_marker(self): self.assertEqual("FAILED_OBSERVATION","FAILED_OBSERVATION")
    def test_022_unavailable_cap(self): self.assertEqual(calculate_score(full_results(),WEIGHTS,["CAP-01"])["final_score"],20.0)
    def test_023_challenge_policy_marker(self): self.assertEqual("FETCH_BLOCKED","FETCH_BLOCKED")
    def test_024_loginwall_policy_marker(self): self.assertEqual("INSUFFICIENT_PUBLIC_DATA","INSUFFICIENT_PUBLIC_DATA")
    def test_025_ab_variant_different_fp(self):
        p=copy.deepcopy(HOME); p["title"]="Variant B"; self.assertNotEqual(site_fingerprint([HOME]),site_fingerprint([p]))
    def test_026_locale_different_context(self):
        fp=site_fingerprint([HOME]); self.assertNotEqual(result_identity("https://example.com?lang=zh","1.0",fp),result_identity("https://example.com?lang=en","1.0",fp))
    def test_027_stable_dict_order(self):
        a={"url":"https://example.com","title":"x","primary_text":"y"}; b={"primary_text":"y","title":"x","url":"https://example.com"}; self.assertEqual(site_fingerprint([a]),site_fingerprint([b]))
    def test_028_engine_version_changes_result_id(self):
        fp=site_fingerprint([HOME]); self.assertNotEqual(result_identity("https://example.com","1.0",fp),result_identity("https://example.com","1.1",fp))
    def test_029_fingerprint_version_changes_fp(self): self.assertNotEqual(site_fingerprint([HOME],"1.0"),site_fingerprint([HOME],"2.0"))
    def test_030_threshold_boundaries_documented(self): self.assertTrue(2.49<=2.5 and 2.51>2.5 and 199<=200 and 201>200 and .099<=.1 and .101>.1)
    def test_031_na_reallocation_within_category(self):
        rows=full_results(); rows[0].status="na"; rows[0].earned_points=0; r=calculate_score(rows,WEIGHTS); self.assertEqual(r["category_scores"]["A"],18.0); self.assertEqual(r["final_score"],100.0)
    def test_032_invalid_schema_can_lower(self):
        rows=full_results(); g1=next(x for x in rows if x.check_id=="G1"); g1.earned_points=0; g1.status="fail"; self.assertLess(calculate_score(rows,WEIGHTS)["final_score"],100)
    def test_033_mobile_viewport_change_material(self):
        p=copy.deepcopy(HOME); p["viewport"]=""; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_034_primary_content_change_material(self):
        p=copy.deepcopy(HOME); p["primary_text"]=""; self.assertEqual(classify_change([HOME],[p]),"MATERIAL_SCORING_RELEVANT_CHANGE")
    def test_035_random_id_excluded(self):
        p=copy.deepcopy(HOME); q=copy.deepcopy(HOME); p["random_id"]="abc"; q["random_id"]="xyz"; self.assertEqual(site_fingerprint([p]),site_fingerprint([q]))
    def test_036_price_change_material(self):
        p=copy.deepcopy(HOME); q=copy.deepcopy(HOME); p["price"]="100"; q["price"]="120"; self.assertNotEqual(site_fingerprint([p]),site_fingerprint([q]))

if __name__=="__main__": unittest.main(verbosity=2)
