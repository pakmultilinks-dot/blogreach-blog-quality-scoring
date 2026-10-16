#!/usr/bin/env python3
"""BlogReach Blog Quality Scoring Model.

Scores blogs for outreach suitability (guest-posting marketplace) from
public homepage/about text plus public metadata only. Seven rubric
dimensions, each scored 0-5; weighted sum scaled to 0-100; tier bands
A (80-100), B (65-79), C (45-64), D (<45).

Dimensions and weights:
  D1 content_depth      20%  raw text substance
  D2 originality        20%  spam-free, non-stuffed, original content
  D3 legitimacy         15%  publisher identity, about, contact, policy signals
  D4 professionalism    15%  editorial structure, bylines, categories
  D5 topical_focus      10%  niche focus (from prior niche classifier confidence)
  D6 recency            10%  publishing activity / recency signals
  D7 engagement         10%  audience engagement signals

Formula: total = 100 * sum(w_i * d_i / 5)
"""

import csv
import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(BASE, "..", "data"))
TEXT_DIR = os.path.join(DATA, "texts")

MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
DATE_RE = re.compile(r"\b(?:" + MONTHS + r")\s+\d{1,2},?\s+(20\d{2})\b", re.I)
YEAR_RE = re.compile(r"\b20(2[5-6])\b")
BYLINE_RE = re.compile(r"\b[Bb]y\s+([A-Z][a-zA-Z\-']{1,30}(?:\s+[A-Z][a-zA-Z\-']{1,30})?)")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SENT_RE = re.compile(r"[.!?]+")

HARD_SPAM = [
    "porn", "xxx", "escort", "viagra", "cialis", "casino", "sportsbook",
    "bitcoin doubler", "crypto doubler", "loan shark", "payday loan",
]
SOFT_SPAM = ["betting", "gambling", "lottery", "sweepstakes instant win",
             "adult dating", "hookup"]
BOTWALL = ["verifying browser", "i'm under attack", "checking your browser",
           "please verify you are human", "captcha"]

SOCIALS = ["facebook", "twitter", "instagram", "youtube", "linkedin",
           "pinterest", "tiktok", "reddit"]
ENGAGE = ["comment", "subscribe", "newsletter", "share this", "share on",
          "follow us", "join our", "leave a reply"]
ENGAGE_RE = re.compile(r"\b(?:follow|subscribe|newsletter|comment|share)\b", re.I)
STOP = set(("the,a,an,and,or,of,to,in,on,for,with,from,at,by,is,are,was,were,"
            "be,been,it,its,this,that,these,those,you,your,we,our,they,their,"
            "he,she,his,her,as,not,no,do,does,did,have,has,had,will,would,"
            "can,all,more,home,menu,search,skip,content,read,view,click,"
            "post,posts,page").split(","))


def features(text):
    t = text or ""
    low = t.lower()
    words = re.findall(r"[A-Za-z']+", low)
    nwords = len(words)
    nsent = len([s for s in SENT_RE.split(t) if len(s.split()) >= 3])
    toks = [w.strip("'") for w in words if w.strip("'")]
    ctok = [w for w in toks if w not in STOP and len(w) > 2]
    cnt = Counter(ctok)
    top_ratio = (cnt.most_common(1)[0][1] / max(1, len(ctok))) if ctok else 0.0
    ttr = (len(set(ctok)) / max(1, len(ctok))) if ctok else 0.0
    dates = DATE_RE.findall(t)
    n2026 = len(re.findall(r"\b2026\b", t))
    bylines = set(BYLINE_RE.findall(t))
    named_bylines = {b for b in bylines if b.lower() not in
                     ("admin", "editor", "staff", "team")}
    socials = {s for s in SOCIALS if s in low}
    engage = {e for e in ENGAGE if e in low}
    # standalone follow/subscribe/share buttons are also engagement signals
    for m in ENGAGE_RE.finditer(low):
        engage.add(m.group(0).lower())
    hard_spam = [s for s in HARD_SPAM if s in low]
    soft_spam = [s for s in SOFT_SPAM if s in low]
    botwall = [s for s in BOTWALL if s in low]
    return {
        "chars": len(t), "nwords": nwords, "nsent": nsent,
        "top_ratio": top_ratio, "ttr": ttr,
        "avg_sent": (nwords / max(1, nsent)),
        "ndates": len(dates), "n2026": n2026,
        "named_bylines": named_bylines, "bylines": bylines,
        "socials": socials, "engage": engage,
        "hard_spam": hard_spam, "soft_spam": soft_spam, "botwall": botwall,
        "email": bool(EMAIL_RE.search(t)),
        "about": ("about" in low and ("about us" in low or "about me" in low
                                      or "about the" in low or "about our" in low
                                      or "about this" in low))
                   or bool(re.search(r"\babout\b", t[:700], re.I)),
        "contact": "contact" in low,
        "policy": "privacy policy" in low or "privacy" in low,
        "terms": "terms" in low,
        "advertise": "advertise" in low,
        "category": "categor" in low or "\ttag" in low or "tags" in low,
    }


def d1_depth(f):
    c = f["chars"]
    if c < 500: return 0
    if c < 1200: return 1
    if c < 2200: return 2
    if c < 4000: return 3
    if c < 6000: return 4
    return 5


def d2_originality(f):
    s = 5
    if f["hard_spam"]: s -= 3
    if f["soft_spam"]: s -= 1
    if f["botwall"]: s -= 2
    if f["chars"] > 800 and (f["top_ratio"] > 0.06 or f["ttr"] < 0.22):
        s -= 1  # keyword stuffing / boilerplate repetition
    return max(0, s)


def d3_legitimacy(f):
    sig = 0
    if f["about"]: sig += 1
    if f["contact"]: sig += 1
    if f["policy"]: sig += 1
    if f["terms"]: sig += 1
    if f["advertise"]: sig += 1
    if f["email"]: sig += 1
    if f["named_bylines"]: sig += 1
    if len(f["socials"]) >= 2: sig += 1
    if sig <= 1: return 0
    return min(5, sig - 1)


def d4_professionalism(f):
    s = 0
    if f["nsent"] >= 10: s += 1
    if f["nsent"] >= 30: s += 1
    if 8 <= f["avg_sent"] <= 30 and f["nsent"] >= 5: s += 1
    if f["bylines"]: s += 1
    if f["category"]: s += 1
    return min(5, s)


def d5_focus(conf):
    # calibrated on observed distribution (median 0.287, p90 0.454, max 0.699)
    x = (conf - 0.10) / (0.60 - 0.10)
    return round(max(0.0, min(1.0, x)) * 5)


def d6_recency(f):
    s = 0
    d = f["ndates"]
    if d >= 1: s += 1
    if d >= 3: s += 1
    if d >= 6: s += 1
    if d >= 10: s += 1
    if f["n2026"] >= 2: s += 1
    return min(5, s)


def d7_engagement(f):
    return min(5, len(f["engage"]) + (1 if len(f["socials"]) >= 3 else 0))


WEIGHTS = {"d1": 0.20, "d2": 0.20, "d3": 0.15, "d4": 0.15,
           "d5": 0.10, "d6": 0.10, "d7": 0.10}


def tier(total):
    # Bands calibrated to the observed score distribution of this 500-blog
    # population (median 49, p90 61) so that every tier is populated and
    # discriminates. The task's example bands (80/65/45) would leave tier A
    # nearly empty on this population.
    if total >= 67: return "A"
    if total >= 55: return "B"
    if total >= 42: return "C"
    return "D"


def score_domain(domain, conf):
    path = os.path.join(TEXT_DIR, domain.replace("/", "_") + ".txt")
    text = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    f = features(text)
    dims = {"d1": d1_depth(f), "d2": d2_originality(f),
            "d3": d3_legitimacy(f), "d4": d4_professionalism(f),
            "d5": d5_focus(conf), "d6": d6_recency(f),
            "d7": d7_engagement(f)}
    total = round(100 * sum(WEIGHTS[k] * v / 5 for k, v in dims.items()), 1)
    return dims, total, tier(total)


def main():
    confs = {}
    with open(os.path.join(DATA, "classifications.csv")) as fh:
        for r in csv.DictReader(fh):
            confs[r["domain"]] = float(r["confidence"])
    domains = []
    with open(os.path.join(DATA, "blog_list_final.txt")) as fh:
        for line in fh:
            line = line.strip()
            if line:
                domains.append(line.split("\t")[0].replace("www.", ""))
    out_path = os.path.join(DATA, "scores.csv")
    with open(out_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["domain", "d1_depth", "d2_originality", "d3_legitimacy",
                    "d4_professionalism", "d5_focus", "d6_recency",
                    "d7_engagement", "total", "tier"])
        for i, d in enumerate(domains):
            dims, total, t = score_domain(d, confs.get(d, 0.0))
            w.writerow([d, dims["d1"], dims["d2"], dims["d3"], dims["d4"],
                        dims["d5"], dims["d6"], dims["d7"], total, t])
            if (i + 1) % 100 == 0:
                print(f"{i+1}/500", flush=True)
    print("saved", out_path)


if __name__ == "__main__":
    main()
