from html.parser import HTMLParser
from urllib.parse import urljoin
import json, re

class AuditHTMLParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url=base_url
        self.lang=""; self.title=""; self.meta={}; self.links=[]; self.images=[]; self.headings=[]; self.forms=[]; self.structured_data=[]; self.text=[]
        self._in_title=False; self._heading=None; self._heading_text=[]; self._in_script=False; self._script_type=""; self._script_buf=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); tag=tag.lower()
        if tag=="html": self.lang=a.get("lang","")
        elif tag=="title": self._in_title=True
        elif tag=="meta":
            name=(a.get("name") or a.get("property") or "").lower()
            if name: self.meta[name]=a.get("content","")
        elif tag=="link":
            rel=(a.get("rel") or "").lower()
            if "canonical" in rel: self.meta["canonical"]=urljoin(self.base_url,a.get("href",""))
        elif tag in ("h1","h2","h3","h4","h5","h6"): self._heading=tag.upper(); self._heading_text=[]
        elif tag=="a":
            href=a.get("href","")
            if href: self.links.append([urljoin(self.base_url,href),""])
        elif tag=="img":
            src=a.get("src",""); self.images.append([urljoin(self.base_url,src) if src else "",a.get("alt","")])
        elif tag=="form": self.forms.append(urljoin(self.base_url,a.get("action","")) if a.get("action") else "")
        elif tag=="script": self._in_script=True; self._script_type=(a.get("type") or "").lower(); self._script_buf=[]
    def handle_endtag(self, tag):
        tag=tag.lower()
        if tag=="title": self._in_title=False
        elif tag in ("h1","h2","h3","h4","h5","h6") and self._heading:
            txt=re.sub(r"\s+"," "," ".join(self._heading_text)).strip()
            self.headings.append(f"{self._heading}: {txt}"); self._heading=None; self._heading_text=[]
        elif tag=="script":
            if "ld+json" in self._script_type:
                raw="".join(self._script_buf).strip()
                if raw:
                    try:
                        data=json.loads(raw); items=data if isinstance(data,list) else [data]
                        for item in items:
                            if isinstance(item,dict):
                                typ=item.get("@type")
                                if isinstance(typ,list): self.structured_data.extend(map(str,typ))
                                elif typ: self.structured_data.append(str(typ))
                    except Exception: self.structured_data.append("__INVALID_JSON_LD__")
            self._in_script=False; self._script_type=""; self._script_buf=[]
    def handle_data(self, data):
        if self._in_title: self.title+=data
        if self._heading: self._heading_text.append(data)
        if self._in_script: self._script_buf.append(data); return
        txt=re.sub(r"\s+"," ",data).strip()
        if txt: self.text.append(txt)

def extract_observation(html: str, url: str, status: int=200, headers=None):
    p=AuditHTMLParser(url); p.feed(html)
    headers={k.lower():v for k,v in (headers or {}).items()}
    return {"url":url,"status":status,"title":re.sub(r"\s+"," ",p.title).strip(),"meta_description":p.meta.get("description",""),
    "robots":p.meta.get("robots",""),"x_robots_tag":headers.get("x-robots-tag",""),"canonical":p.meta.get("canonical",""),"lang":p.lang,
    "headings":p.headings,"internal_links":p.links,"images":p.images,"structured_data":sorted(p.structured_data),"forms":p.forms,
    "viewport":p.meta.get("viewport",""),"open_graph":{"title":p.meta.get("og:title",""),"description":p.meta.get("og:description",""),"image":p.meta.get("og:image","")},
    "primary_text":" ".join(p.text)}
