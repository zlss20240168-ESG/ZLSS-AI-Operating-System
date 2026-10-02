from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import hashlib, json, re

TRACKING_EXACT={"fbclid","gclid","msclkid"}
VOLATILE_KEYS={"timestamp","current_time","session_id","csrf_token","random_id","analytics_session","cache_buster","visitor_counter"}

def _is_tracking_param(key:str)->bool:
    k=key.lower()
    return k.startswith("utm_") or k in TRACKING_EXACT

def normalize_url(url:str)->str:
    s=urlsplit(url.strip())
    scheme=s.scheme.lower() or "https"
    host=(s.hostname or "").lower()
    port=s.port
    netloc=host
    if port and not ((scheme=="http" and port==80) or (scheme=="https" and port==443)):
        netloc=f"{host}:{port}"
    path=re.sub(r"/{2,}","/",s.path or "/")
    if len(path)>1 and path.endswith("/"): path=path[:-1]
    params=[(k,v) for k,v in parse_qsl(s.query,keep_blank_values=True) if not _is_tracking_param(k)]
    params.sort(key=lambda kv:(kv[0],kv[1]))
    return urlunsplit((scheme,netloc,path,urlencode(params,doseq=True),""))

def stable_json(obj:Any)->str:
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def hash_obj(obj:Any)->str:
    return hashlib.sha256(stable_json(obj).encode("utf-8")).hexdigest()

def sanitize_page_for_fingerprint(page:Dict[str,Any])->Dict[str,Any]:
    def clean(x):
        if isinstance(x,dict): return {k:clean(v) for k,v in sorted(x.items()) if k not in VOLATILE_KEYS}
        if isinstance(x,list): return [clean(v) for v in x]
        if isinstance(x,str): return re.sub(r"\s+"," ",x).strip()
        return x
    p=clean(page)
    if "url" in p: p["url"]=normalize_url(p["url"])
    return p

def page_fingerprint(page:Dict[str,Any])->str:
    return hash_obj(sanitize_page_for_fingerprint(page))

def site_fingerprint(pages:List[Dict[str,Any]],fingerprint_version:str="1.0.0")->str:
    normalized=[]
    for p in pages:
        q=sanitize_page_for_fingerprint(p)
        normalized.append({"url":q.get("url",""),"fp":hash_obj(q)})
    normalized.sort(key=lambda x:(x["url"],x["fp"]))
    return hash_obj({"fingerprint_version":fingerprint_version,"pages":normalized})

@dataclass
class CheckResult:
    check_id:str
    category:str
    max_points:float
    earned_points:float=0.0
    status:str="fail"
    severity:str="Medium"
    evidence:Any=None
    def normalized(self):
        ep=0.0 if self.status=="na" else max(0.0,min(float(self.earned_points),float(self.max_points)))
        return CheckResult(self.check_id,self.category,float(self.max_points),ep,self.status,self.severity,self.evidence)

def category_score(results:List[CheckResult],category:str,category_weight:float)->float:
    rows=[r.normalized() for r in results if r.category==category]
    applicable=[r for r in rows if r.status!="na"]
    denom=sum(r.max_points for r in applicable)
    if denom<=0: return 0.0
    return round(category_weight*(sum(r.earned_points for r in applicable)/denom),4)

def score_band(score:float)->str:
    if score>=90:return "Excellent foundation"
    if score>=80:return "Strong"
    if score>=70:return "Good / material improvements available"
    if score>=60:return "Needs improvement"
    if score>=40:return "Weak"
    return "Critical"

def calculate_score(results:List[CheckResult],category_weights:Dict[str,float],triggered_caps:Optional[List[str]]=None,cap_values:Optional[Dict[str,float]]=None)->Dict[str,Any]:
    triggered_caps=triggered_caps or []
    cap_values=cap_values or {"CAP-01":20.0,"CAP-02":30.0,"CAP-03":35.0}
    cat={k:category_score(results,k,w) for k,w in category_weights.items()}
    raw=round(sum(cat.values()),2)
    cap=min([cap_values[c] for c in triggered_caps if c in cap_values],default=None)
    final=round(min(raw,cap) if cap is not None else raw,2)
    return {"category_scores":cat,"raw_score":raw,"critical_cap":cap,"final_score":final,"score_band":score_band(final)}

def result_identity(normalized_origin:str,engine_version:str,site_fp:str)->str:
    return hash_obj({"normalized_origin":normalize_url(normalized_origin),"audit_engine_version":engine_version,"site_fingerprint":site_fp})

def classify_change(old_pages:List[Dict[str,Any]],new_pages:List[Dict[str,Any]],scoring_fields=None)->str:
    if site_fingerprint(old_pages)==site_fingerprint(new_pages): return "NO_MATERIAL_CHANGE"
    scoring_fields=set(scoring_fields or ["url","status","title","meta_description","robots","x_robots_tag","canonical","lang","headings","internal_links","images","structured_data","forms","viewport","open_graph","primary_text","price","cta"])
    def project(pages):
        out=[]
        for p in pages:
            q=sanitize_page_for_fingerprint(p)
            out.append({k:q.get(k) for k in sorted(scoring_fields) if k in q})
        return sorted(out,key=lambda x:x.get("url",""))
    if hash_obj(project(old_pages))==hash_obj(project(new_pages)): return "MINOR_NON_SCORING_CHANGE"
    return "MATERIAL_SCORING_RELEVANT_CHANGE"
