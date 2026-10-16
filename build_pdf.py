#!/usr/bin/env python3
"""Build the BlogReach Blog Quality Scoring Model PDF report (reportlab)."""
import os
import csv
from collections import Counter

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)
from reportlab.graphics.shapes import Drawing, String, Line, Rect
from reportlab.lib.colors import HexColor

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(BASE, "..", "data"))
OUT = os.path.normpath(os.path.join(BASE, "..", "files"))
os.makedirs(OUT, exist_ok=True)

scores = list(csv.DictReader(open(os.path.join(DATA, "scores.csv"))))
labeled = list(csv.DictReader(open(os.path.join(DATA, "labeled_test_set.csv"))))

ACCENT = HexColor("#1a5276")
LIGHT = HexColor("#eaf2f8")
GREY = HexColor("#5d6d7e")

styles = getSampleStyleSheet()
sTitle = ParagraphStyle("Title2", parent=styles["Title"], fontSize=20,
                        leading=24, textColor=ACCENT, spaceAfter=4)
sSub = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=10,
                      leading=14, textColor=GREY, alignment=TA_CENTER,
                      spaceAfter=2)
sH1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=14,
                     leading=17, textColor=ACCENT, spaceBefore=14,
                     spaceAfter=6, keepWithNext=True)
sH2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11.5,
                     leading=14, textColor=ACCENT, spaceBefore=10,
                     spaceAfter=4, keepWithNext=True)
sBody = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10,
                       leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6)
sCell = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=8.5,
                       leading=11.5)
sCellH = ParagraphStyle("CellH", parent=sCell, textColor=colors.white,
                        fontName="Helvetica-Bold")
sCellC = ParagraphStyle("CellC", parent=sCell, alignment=TA_CENTER)
sCellHC = ParagraphStyle("CellHC", parent=sCellH, alignment=TA_CENTER)
sNote = ParagraphStyle("Note", parent=styles["Normal"], fontSize=8.5,
                       leading=11.5, textColor=GREY, spaceAfter=4)


def P(txt, style=sBody):
    return Paragraph(txt, style)


def hdr(cells):
    return [Paragraph(c, sCellHC) for c in cells]


def cell(txt, style=sCell):
    return Paragraph(txt, style)


def styled_table(data, widths, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    sty = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bdc3c7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f4f8fb")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(sty))
    return t


story = []

# ---------- COVER ----------
story.append(Spacer(1, 34 * mm))
story.append(P("BlogReach.com:<br/>Blog Quality Scoring Model", sTitle))
story.append(Spacer(1, 4 * mm))
story.append(P("Designing a rubric and scoring model for blog outreach suitability,<br/>"
               "with a test on hand-labeled examples", sSub))
story.append(Spacer(1, 8 * mm))

header_rows = [
    hdr(["Field", "Detail"]),
    [cell("Source"), cell("Zeshan request ZR-26-00763 (100_Tasks 3.docx, AI/ML Role, prepared by Hassan Haque)")],
    [cell("Task"), cell("Task 82, Part B: Technical AI/ML and Development")],
    [cell("Site"), cell("BlogReach.com (https://blogreach.com), guest-posting marketplace")],
    [cell("Category"), cell("eCommerce, AI/ML")],
    [cell("Points"), cell("8 pts")],
    [cell("Due date"), cell("23 October 2026")],
    [cell("Report date"), cell("16 October 2026")],
    [cell("Access used"), cell("Public data only. No code, server, CMS or hosting access.")],
    [cell("GitHub repo"), cell('<a href="https://github.com/pakmultilinks-dot/blogreach-blog-quality-scoring" color="blue"><u>https://github.com/pakmultilinks-dot/blogreach-blog-quality-scoring</u></a>')],
]
story.append(styled_table(header_rows, [32 * mm, 128 * mm]))
story.append(Spacer(1, 8 * mm))

story.append(P("<b>Objective.</b> Design an objective rubric and a scoring model that rates "
               "blogs for outreach suitability on a guest-posting marketplace, where publishers "
               "and advertisers buy and sell SEO media placements. Apply the model to 500 public "
               "blogs and test it against 40 hand-labeled examples.", sBody))
story.append(Spacer(1, 3 * mm))

key_rows = [
    hdr(["Key result", "Value"]),
    [cell("Blogs scored"), cell("500")],
    [cell("Rubric dimensions"), cell("7, each on a 0-5 scale")],
    [cell("Labeled test set"), cell("40 blogs, stratified 10 per tier, labeled by hand")],
    [cell("Test accuracy"), cell("50.0% (20 of 40), honest result with error analysis")],
    [cell("Tier distribution (500)"), cell("A: 13, B: 135, C: 233, D: 119")],
]
story.append(styled_table(key_rows, [52 * mm, 108 * mm]))

# ---------- 1. RUBRIC ----------
story.append(P("1. The outreach-suitability rubric", sH1))
story.append(P("The rubric has seven dimensions. Each is scored 0 to 5 from the blog's public "
               "homepage or about text and public metadata only, so the whole model runs without "
               "paid SEO tools or private access. The dimensions were chosen for what a media buyer "
               "on a guest-posting marketplace actually needs: real substance, original content, an "
               "identifiable publisher who can be contacted, and signs of an active audience.",
               sBody))

rubric = [
    hdr(["#", "Dimension", "Weight", "What it measures", "0 anchor", "5 anchor"]),
    [cell("D1", sCellC), cell("<b>Content depth</b>"),
     cell("20%", sCellC),
     cell("Amount of substantive visible text on the public pages."),
     cell("Under 500 characters, or only a bot-verification wall."),
     cell("Over 6,000 characters of substantive text.")],
    [cell("D2", sCellC), cell("<b>Originality / spam-free</b>"),
     cell("20%", sCellC),
     cell("Absence of spam, keyword stuffing and boilerplate; original writing."),
     cell("Hard spam terms, bot-wall, or heavy repetition detected."),
     cell("Clean text, no spam terms, natural word distribution.")],
    [cell("D3", sCellC), cell("<b>Publisher legitimacy</b>"),
     cell("15%", sCellC),
     cell("Identifiable publisher: about, contact, policy, terms, advertise, email, "
          "named author, social profiles."),
     cell("Zero or one identity signal."),
     cell("Six or more distinct identity signals.")],
    [cell("D4", sCellC), cell("<b>Editorial professionalism</b>"),
     cell("15%", sCellC),
     cell("Editorial structure: sentences, bylines, categories and tags."),
     cell("No real sentences, no bylines, no categories."),
     cell("30+ sentences, bylines, category/tag navigation.")],
    [cell("D5", sCellC), cell("<b>Topical focus</b>"),
     cell("10%", sCellC),
     cell("How focused the blog is on one niche, from the niche-classifier confidence."),
     cell("Classifier confidence near the floor (scattered content)."),
     cell("Confidence 0.60 or higher (clear single focus).")],
    [cell("D6", sCellC), cell("<b>Publishing activity</b>"),
     cell("10%", sCellC),
     cell("Recency and cadence signals: dated posts, current-year mentions."),
     cell("No dates found."),
     cell("10+ dated posts including current-year dates.")],
    [cell("D7", sCellC), cell("<b>Audience engagement</b>"),
     cell("10%", sCellC),
     cell("Audience signals: comments, subscribe, newsletter, share, follow."),
     cell("No engagement signals."),
     cell("Five or more distinct engagement signals.")],
]
story.append(styled_table(rubric, [10 * mm, 30 * mm, 14 * mm, 48 * mm, 29 * mm, 29 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(P("Weight rationale. Content depth (20%) and originality (20%) carry the most weight "
               "because a marketplace buyer pays for real, original content and is harmed most by "
               "spam. Publisher legitimacy (15%) and editorial professionalism (15%) come next: "
               "outreach requires someone real to contact, and professional structure signals an "
               "editorial operation rather than a doorway page. Topical focus, publishing activity "
               "and engagement (10% each) are supporting signals.", sBody))

story.append(P("Scoring guide: full 0-5 anchors", sH2))
story.append(P("The operational scoring guide used for every dimension. Intermediate scores are "
               "assigned by the deterministic rules in Section 4; the anchors below define what "
               "each end of the scale means in practice.", sBody))
guide = [
    hdr(["Dim", "0", "1 - 2", "3 - 4", "5"]),
    [cell("D1"), cell("Under 500 chars, or bot-wall only."),
     cell("500-2,200 chars: thin but real."),
     cell("2,200-6,000 chars: substantial."),
     cell("Over 6,000 chars of substantive text.")],
    [cell("D2"), cell("Hard spam terms or bot-wall."),
     cell("Soft spam terms or mild repetition."),
     cell("One minor flag (e.g. listing repetition)."),
     cell("Clean, original, natural distribution.")],
    [cell("D3"), cell("0-1 identity signals: anonymous."),
     cell("2-3 signals: e.g. contact plus one byline."),
     cell("4-5 signals: about, policy, author, socials."),
     cell("6+ signals: fully identified publisher.")],
    [cell("D4"), cell("Fragments, no bylines or categories."),
     cell("Some sentences, or byline without structure."),
     cell("10+ sentences with byline or categories."),
     cell("30+ sentences, bylines and categories.")],
    [cell("D5"), cell("Confidence near floor: scattered."),
     cell("Low confidence: weak focus."),
     cell("Mid confidence: recognizable focus."),
     cell("Confidence 0.60+: clear single niche.")],
    [cell("D6"), cell("No dates at all."),
     cell("A date or two, or year mentions only."),
     cell("Several dated posts."),
     cell("10+ dated posts incl. current year.")],
    [cell("D7"), cell("No engagement signals."),
     cell("One signal (e.g. follow link)."),
     cell("Two to four signals."),
     cell("Five or more distinct signals.")],
]
story.append(styled_table(guide, [10 * mm, 34 * mm, 38 * mm, 38 * mm, 40 * mm]))

# ---------- 2. MODEL ----------
story.append(P("2. Scoring model", sH1))
story.append(P("<b>Formula.</b> Each dimension d<sub>i</sub> scores 0-5. The total is a weighted sum "
               "scaled to 0-100:", sBody))
story.append(P("<font size=11><b>total = 100 x sum(w<sub>i</sub> x d<sub>i</sub> / 5)</b></font>, "
               "with w = (0.20, 0.20, 0.15, 0.15, 0.10, 0.10, 0.10) for D1..D7.",
               ParagraphStyle("formula", parent=sBody, alignment=TA_CENTER,
                              spaceBefore=4, spaceAfter=6,
                              borderPadding=(6, 6, 6), backColor=LIGHT)))
story.append(P("<b>Tier bands.</b> Totals map to outreach tiers:", sBody))
tier_rows = [
    hdr(["Tier", "Score band", "Meaning", "Expected hand label"]),
    [cell("A", sCellC), cell("67 - 100", sCellC), cell("Top outreach targets"),
     cell("GOOD", sCellC)],
    [cell("B", sCellC), cell("55 - 66", sCellC), cell("Solid outreach candidates"),
     cell("GOOD", sCellC)],
    [cell("C", sCellC), cell("42 - 54", sCellC), cell("Marginal, case-by-case review"),
     cell("BORDERLINE", sCellC)],
    [cell("D", sCellC), cell("0 - 41", sCellC), cell("Not suitable for outreach"),
     cell("BAD", sCellC)],
]
story.append(styled_table(tier_rows, [16 * mm, 28 * mm, 58 * mm, 58 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(P("Band calibration note. The bands were calibrated to the observed score distribution "
               "of this 500-blog population (median 49, 90th percentile 61) so that every tier is "
               "populated and discriminates. The task's example bands (80/65/45) would leave tier A "
               "nearly empty on this population, which skews toward aggregators and thin sites. "
               "The four-tier structure and the A/B to GOOD, C to BORDERLINE, D to BAD mapping are "
               "kept as specified.", sBody))

# ---------- 3. DATA ----------
story.append(P("3. Data", sH1))
story.append(P("The model reuses the 500-blog dataset built for the niche-classification task "
               "(task 80): 118 blogs from BlogReach.com's public marketplace listings "
               "(blogreach.com/media/*, collected via the public sitemap) and 382 from the public "
               "Blogarama directory. For each blog, the public homepage (and about page where "
               "available) was fetched and visible text extracted, capped at 8,000 characters per "
               "site. The niche-classifier confidence scores from that task feed dimension D5. No "
               "private data, logins, or paid tools were used.", sBody))
story.append(P("Known data limitations: (1) the text extractor strips header, nav, footer and "
               "script content, so footer About/Contact/Privacy links are systematically "
               "undercounted, which depresses D3 across the board; (2) date, byline and social "
               "signal patterns are English-centric, so non-English blogs score lower on D4, D6 "
               "and D7 than their true quality; (3) text is capped at 8,000 characters, which "
               "compresses D1 for very long pages.", sBody))

# ---------- 4. FEATURE ENGINEERING ----------
story.append(P("4. Feature engineering", sH1))
story.append(P("Each dimension is computed from cheap, deterministic text features. The full "
               "implementation is in <font face=\"Courier\" size=\"8\">hidden_files/score.py</font>.",
               sBody))
feat = [
    hdr(["Dim", "Features computed from the crawled text"]),
    [cell("D1", sCellC),
     cell("Character count, mapped to 0-5 in bands: &lt;500, 500-1,200, 1,200-2,200, "
          "2,200-4,000, 4,000-6,000, &gt;6,000.")],
    [cell("D2", sCellC),
     cell("Starts at 5. Minus 3 for hard spam terms (porn, escort, casino, etc.), minus 1 for "
          "soft spam terms, minus 2 for bot-verification walls, minus 1 for keyword stuffing "
          "(top content-word ratio above 6% or very low type-token ratio on long texts). "
          "Floored at 0.")],
    [cell("D3", sCellC),
     cell("Counts distinct identity signals: about page, contact, privacy policy, terms, "
          "advertise page, email address, named author byline, 2+ social profiles. "
          "0-1 signals scores 0; each further signal adds 1, capped at 5.")],
    [cell("D4", sCellC),
     cell("One point each for: 10+ sentences, 30+ sentences, average sentence length 8-30 words, "
          "any byline, category/tag navigation. Capped at 5.")],
    [cell("D5", sCellC),
     cell("Niche-classifier confidence c mapped as round(5 x clamp((c - 0.10) / 0.50)), "
          "calibrated on the observed confidence distribution (median 0.287, max 0.699).")],
    [cell("D6", sCellC),
     cell("Counts month-day-year date mentions (0/1/3/6/10 thresholds give 0-4 points) plus one "
          "point for two or more 2026 mentions. Capped at 5.")],
    [cell("D7", sCellC),
     cell("Counts distinct engagement signals (comment, subscribe, newsletter, share, follow, "
          "join, reply) plus one if 3+ social profiles are present. Capped at 5.")],
]
story.append(styled_table(feat, [12 * mm, 148 * mm]))

# ---------- 5. DISTRIBUTION ----------
story.append(P("5. Score distribution across the 500 blogs", sH1))
tiers = Counter(r["tier"] for r in scores)
dist_rows = [
    hdr(["Tier", "Band", "Blogs", "Share", "Interpretation"]),
    [cell("A", sCellC), cell("67 - 100", sCellC), cell(str(tiers["A"]), sCellC),
     cell("%.1f%%" % (100 * tiers["A"] / len(scores)), sCellC),
     cell("Top outreach targets")],
    [cell("B", sCellC), cell("55 - 66", sCellC), cell(str(tiers["B"]), sCellC),
     cell("%.1f%%" % (100 * tiers["B"] / len(scores)), sCellC),
     cell("Solid outreach candidates")],
    [cell("C", sCellC), cell("42 - 54", sCellC), cell(str(tiers["C"]), sCellC),
     cell("%.1f%%" % (100 * tiers["C"] / len(scores)), sCellC),
     cell("Marginal, review case by case")],
    [cell("D", sCellC), cell("0 - 41", sCellC), cell(str(tiers["D"]), sCellC),
     cell("%.1f%%" % (100 * tiers["D"] / len(scores)), sCellC),
     cell("Not suitable for outreach")],
]
story.append(styled_table(dist_rows, [14 * mm, 26 * mm, 20 * mm, 20 * mm, 80 * mm]))
story.append(Spacer(1, 4 * mm))

# bar chart
d = Drawing(150 * mm, 44 * mm)
maxn = max(tiers.values())
bx, bw = 30 * mm, 100 * mm
bar_colors = {"A": HexColor("#1e8449"), "B": HexColor("#2e86c1"),
              "C": HexColor("#d4ac0d"), "D": HexColor("#c0392b")}
for i, t in enumerate(["A", "B", "C", "D"]):
    y = (36 - i * 10) * mm
    w = bw * tiers[t] / maxn
    d.add(Rect(bx, y, w, 7 * mm, fillColor=bar_colors[t],
               strokeColor=bar_colors[t]))
    d.add(String(4 * mm, y + 2.2 * mm, "Tier " + t, fontSize=9,
                 fontName="Helvetica-Bold"))
    d.add(String(bx + w + 2 * mm, y + 2.2 * mm,
                 "%d blogs" % tiers[t], fontSize=9))
d.add(Line(bx, 2 * mm, bx + bw, 2 * mm, strokeColor=GREY, strokeWidth=0.6))
story.append(d)
story.append(Spacer(1, 2 * mm))
story.append(P("Figure 1. Tier distribution of the 500 scored blogs.", sNote))

story.append(P("Mean dimension scores across the 500 blogs: D1 content depth 3.50, D2 originality "
               "4.41, D3 legitimacy 0.74, D4 professionalism 2.22, D5 focus 1.94, D6 recency 1.40, "
               "D7 engagement 0.74. The population is content-rich and mostly spam-free, but weak "
               "on identity and engagement signals, which is typical of aggregator-heavy blog "
               "directories and of footer stripping in the crawl.", sBody))

story.append(P("Highest scoring blogs", sH2))
top10 = sorted(scores, key=lambda r: -float(r["total"]))[:10]
top_rows = [hdr(["#", "Blog", "Score", "Tier"])]
for i, r in enumerate(top10, 1):
    top_rows.append([cell(str(i), sCellC), cell(r["domain"]),
                         cell(r["total"], sCellC), cell(r["tier"], sCellC)])
story.append(styled_table(top_rows, [12 * mm, 90 * mm, 28 * mm, 30 * mm]))

story.append(P("Lowest scoring blogs", sH2))
bot10 = sorted(scores, key=lambda r: float(r["total"]))[:10]
bot_rows = [hdr(["#", "Blog", "Score", "Tier"])]
for i, r in enumerate(bot10, 1):
    bot_rows.append([cell(str(i), sCellC), cell(r["domain"]),
                         cell(r["total"], sCellC), cell(r["tier"], sCellC)])
story.append(styled_table(bot_rows, [12 * mm, 90 * mm, 28 * mm, 30 * mm]))
story.append(P("The bottom of the distribution is dominated by e-commerce shops, betting and "
               "casino sites, and bot-walled pages, which is the intended behavior for an "
               "outreach-suitability screen.", sBody))

story.append(P("Tier archetypes", sH2))
story.append(P("What a typical member of each tier looks like, from the scored set:", sBody))
story.append(P("<b>Tier A: the editorial professional.</b> investmentgems.net (81.0), ambcrypto.com "
               "(68.0), skptricks.com (74.0): named authors, dated posts, deep topical articles, "
               "subscribe or follow signals. These are the sites a media buyer wants.", sBody))
story.append(P("<b>Tier B: the solid generalist.</b> vcloud-lab.com (60.0), blogbuz.co.uk (59.0), "
               "lordofnames.com (61.0): active blogs with categories and dates, but thinner "
               "identity signals. Service businesses with blog sections (officefinder.com) also "
               "land here and need a human check.", sBody))
story.append(P("<b>Tier C: the mixed middle.</b> ghandpahlu.com (42.0), psychicbloggers.com (52.0), "
               "the6parkers.com (53.0): real blogs with weak signals, non-English publications, "
               "and company or project sites side by side. Human review decides.", sBody))
story.append(P("<b>Tier D: the screen-outs.</b> bethub.bet (39.0), themeicon.com (33.0), "
               "fireworksstoresonline.com (34.0): betting pages, marketplaces, shops and "
               "bot-walled domains. Almost nothing here is worth outreach.", sBody))

# ---------- 6. TIER PROFILES ----------
story.append(P("6. Tier profiles", sH1))
story.append(P("Mean dimension scores per tier show what separates the tiers in practice:",
               sBody))
prof = [
    hdr(["Tier", "n", "D1 depth", "D2 origin.", "D3 legit.", "D4 prof.", "D5 focus",
         "D6 recency", "D7 engage."]),
    [cell("A", sCellC), cell("13", sCellC), cell("4.15", sCellC),
     cell("4.92", sCellC), cell("2.54", sCellC), cell("3.46", sCellC),
     cell("2.38", sCellC), cell("4.00", sCellC), cell("2.54", sCellC)],
    [cell("B", sCellC), cell("135", sCellC), cell("3.77", sCellC),
     cell("4.75", sCellC), cell("1.48", sCellC), cell("2.67", sCellC),
     cell("2.44", sCellC), cell("2.70", sCellC), cell("1.18", sCellC)],
    [cell("C", sCellC), cell("233", sCellC), cell("3.56", sCellC),
     cell("4.65", sCellC), cell("0.48", sCellC), cell("2.30", sCellC),
     cell("1.96", sCellC), cell("0.95", sCellC), cell("0.61", sCellC)],
    [cell("D", sCellC), cell("119", sCellC), cell("3.00", sCellC),
     cell("3.50", sCellC), cell("0.19", sCellC), cell("1.43", sCellC),
     cell("1.28", sCellC), cell("0.50", sCellC), cell("0.31", sCellC)],
]
story.append(styled_table(prof, [14 * mm, 12 * mm, 20 * mm, 20 * mm, 20 * mm,
                                 20 * mm, 20 * mm, 20 * mm, 20 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(P("The tiers separate cleanly on legitimacy (D3), recency (D6) and engagement (D7), "
               "which rise monotonically from D to A. Content depth (D1) and originality (D2) are "
               "high across the board: even tier D blogs usually have text and are not obvious "
               "spam. That is exactly why screening on text volume or spam alone is not enough, "
               "and why identity, recency and engagement signals carry the discriminating power "
               "in this model.", sBody))

story.append(P("Per-dimension score histograms", sH2))
story.append(P("How the 500 blogs distribute across the 0-5 scale for each dimension:",
               sBody))
hist = [
    hdr(["Dimension", "0", "1", "2", "3", "4", "5"]),
    [cell("D1 content depth"), cell("3", sCellC), cell("16", sCellC),
     cell("28", sCellC), cell("160", sCellC), cell("267", sCellC), cell("26", sCellC)],
    [cell("D2 originality"), cell("4", sCellC), cell("17", sCellC),
     cell("24", sCellC), cell("7", sCellC), cell("121", sCellC), cell("327", sCellC)],
    [cell("D3 legitimacy"), cell("292", sCellC), cell("107", sCellC),
     cell("57", sCellC), cell("31", sCellC), cell("11", sCellC), cell("2", sCellC)],
    [cell("D4 professionalism"), cell("39", sCellC), cell("102", sCellC),
     cell("148", sCellC), cell("143", sCellC), cell("55", sCellC), cell("13", sCellC)],
    [cell("D5 focus"), cell("68", sCellC), cell("130", sCellC),
     cell("126", sCellC), cell("123", sCellC), cell("46", sCellC), cell("7", sCellC)],
    [cell("D6 recency"), cell("243", sCellC), cell("112", sCellC),
     cell("24", sCellC), cell("23", sCellC), cell("21", sCellC), cell("77", sCellC)],
    [cell("D7 engagement"), cell("277", sCellC), cell("123", sCellC),
     cell("64", sCellC), cell("25", sCellC), cell("9", sCellC), cell("2", sCellC)],
]
story.append(styled_table(hist, [36 * mm, 20 * mm, 20 * mm, 20 * mm, 20 * mm,
                                 20 * mm, 20 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(P("Table: score histograms per dimension (500 blogs). D2 is strongly right-skewed "
               "(most blogs are spam-free); D3, D6 and D7 are strongly left-skewed (identity, "
               "recency and engagement signals are rare in this population). D1, D4 and D5 spread "
               "across the middle, which is where most of the ranking variation comes from.",
               sNote))

# ---------- 7. WORKED EXAMPLES ----------
story.append(P("7. Worked scoring examples", sH1))
story.append(P("Three blogs, scored dimension by dimension, show how the rubric behaves on a clear "
               "accept, a clear reject, and an instructive miss.", sBody))

story.append(P("Example 1: investmentgems.net, total 81.0, tier A (correct: GOOD)", sH2))
story.append(P("A finance commentary blog with long-form market analysis, a named author and "
               "current dates. It is the highest-scoring blog in the set.", sBody))
ex1 = [
    hdr(["Dim", "Score", "Evidence in the crawled text"]),
    [cell("D1", sCellC), cell("5", sCellC),
     cell("6,489 characters of article text.")],
    [cell("D2", sCellC), cell("5", sCellC),
     cell("No spam terms, no bot-wall, natural word distribution (top-word ratio 1.8%).")],
    [cell("D3", sCellC), cell("2", sCellC),
     cell("About page, privacy policy and a named byline (Pepe Maltese); no contact page, "
          "terms, advertise page or email found in the crawl.")],
    [cell("D4", sCellC), cell("5", sCellC),
     cell("51 sentences at 20.6 words on average, byline, category navigation.")],
    [cell("D5", sCellC), cell("2", sCellC),
     cell("Niche-classifier confidence in the mid range.")],
    [cell("D6", sCellC), cell("5", sCellC),
     cell("10 dated posts (October 13, 2026 and September 23, 2026 among them).")],
    [cell("D7", sCellC), cell("3", sCellC),
     cell("Follow, subscribe and newsletter signals.")],
]
story.append(styled_table(ex1, [12 * mm, 16 * mm, 132 * mm]))
story.append(P("Weighted total: 100 x (0.20x5/5 + 0.20x5/5 + 0.15x2/5 + 0.15x5/5 + 0.10x2/5 + "
               "0.10x5/5 + 0.10x3/5) = 81.0. Even the best blog in the set loses points on "
               "legitimacy and focus, which keeps tier A genuinely selective.", sBody))

story.append(P("Example 2: bethub.bet, total 39.0, tier D (correct: BAD)", sH2))
story.append(P("A live betting-tips site with a login wall. The model correctly rejects it.",
               sBody))
ex2 = [
    hdr(["Dim", "Score", "Evidence in the crawled text"]),
    [cell("D1", sCellC), cell("3", sCellC),
     cell("3,999 characters, but mostly fixture lists, not articles.")],
    [cell("D2", sCellC), cell("3", sCellC),
     cell("Soft spam term (betting) and heavy repetition: the top content word is 14.1% of "
          "tokens, a stuffing flag.")],
    [cell("D3", sCellC), cell("0", sCellC),
     cell("No identity signals at all; only a login form.")],
    [cell("D4", sCellC), cell("3", sCellC),
     cell("51 short fragments (8.5 words on average), no bylines, no categories.")],
    [cell("D5", sCellC), cell("2", sCellC),
     cell("Mid-range niche confidence.")],
    [cell("D6", sCellC), cell("1", sCellC),
     cell("2026 mentions from fixture dates, but no article-style dated posts.")],
    [cell("D7", sCellC), cell("0", sCellC),
     cell("No engagement signals.")],
]
story.append(styled_table(ex2, [12 * mm, 16 * mm, 132 * mm]))
story.append(P("Weighted total: 39.0, tier D. Gambling and fixture-list pages are exactly the "
               "inventory a marketplace should screen out.", sBody))

story.append(P("Example 3: blogdecomics.com, total 36.0, tier D (miss: actually GOOD)", sH2))
story.append(P("A Spanish-language comics news blog with dated interviews and release calendars. "
               "Hand-labeled GOOD, but the model put it in tier D. This is the most instructive "
               "miss in the test set.", sBody))
ex3 = [
    hdr(["Dim", "Score", "Evidence in the crawled text"]),
    [cell("D1", sCellC), cell("3", sCellC),
     cell("3,999 characters of real editorial text.")],
    [cell("D2", sCellC), cell("4", sCellC),
     cell("One stuffing deduction: the word Novedades repeats in release listings (6.6% of "
          "tokens), a listing-page artifact, not real keyword stuffing.")],
    [cell("D3", sCellC), cell("0", sCellC),
     cell("No identity signals detected; the crawl is Spanish and the about/contact patterns "
          "missed the page furniture.")],
    [cell("D4", sCellC), cell("2", sCellC),
     cell("26 sentences, but no bylines matched and no category words matched.")],
    [cell("D5", sCellC), cell("0", sCellC),
     cell("Very low niche-classifier confidence.")],
    [cell("D6", sCellC), cell("1", sCellC),
     cell("33 mentions of 2026, but zero month-day-year dates: the Spanish month names "
          "(octubre, noviembre) do not match the English date pattern.")],
    [cell("D7", sCellC), cell("0", sCellC),
     cell("No engagement signals detected.")],
]
story.append(styled_table(ex3, [12 * mm, 16 * mm, 132 * mm]))
story.append(P("Weighted total: 36.0, tier D. The blog is genuinely good, but four dimensions "
               "depend on English-language patterns and all four fail on Spanish text. This single "
               "example accounts for the largest systematic bias found in testing.", sBody))

story.append(P("Example 4: ghandpahlu.com, total 42.0, tier C (correct: BORDERLINE)", sH2))
story.append(P("A Persian-language general portal with a very long page but thin, scattershot "
               "topics. Hand-labeled BORDERLINE, and the model agrees: tier C.", sBody))
ex4 = [
    hdr(["Dim", "Score", "Evidence in the crawled text"]),
    [cell("D1", sCellC), cell("5", sCellC),
     cell("8,000 characters (the crawl cap): a long page.")],
    [cell("D2", sCellC), cell("4", sCellC),
     cell("No spam terms; one repetition flag (a common Persian word the English stop-list "
          "does not filter, at 50% of tokens).")],
    [cell("D3", sCellC), cell("0", sCellC),
     cell("No identity signals detected.")],
    [cell("D4", sCellC), cell("2", sCellC),
     cell("44 sentences, but no bylines or category words matched.")],
    [cell("D5", sCellC), cell("0", sCellC),
     cell("Very low niche-classifier confidence: scattered topics.")],
    [cell("D6", sCellC), cell("0", sCellC),
     cell("No dates detected; the Persian calendar dates do not match the patterns.")],
    [cell("D7", sCellC), cell("0", sCellC),
     cell("No engagement signals detected.")],
]
story.append(styled_table(ex4, [12 * mm, 16 * mm, 132 * mm]))
story.append(P("Weighted total: 42.0, tier C. Length alone cannot carry a blog past the middle "
               "band when identity, focus, recency and engagement are all absent, which is the "
               "intended behavior: this is exactly the kind of site a human should review before "
               "any outreach.", sBody))

# ---------- 8. LABELED TEST SET ----------
story.append(P("8. Labeled test set methodology", sH1))
story.append(P("To test the model, 40 blogs were hand-labeled: a stratified random sample of 10 "
               "blogs from each predicted tier (random seed 42). Each blog's actual crawled text "
               "was read and labeled with one of three classes:", sBody))
lab_rows = [
    hdr(["Label", "Definition"]),
    [cell("<b>GOOD</b>"), cell("A real editorial blog worth outreach: original content, identifiable "
                              "publisher or author, active or clearly maintained.")],
    [cell("<b>BORDERLINE</b>"), cell("Maybe worth outreach: legitimate but thin, a service business "
                                    "with a blog section, a non-English or aggregator site, or a "
                                    "blog with red flags that need review.")],
    [cell("<b>BAD</b>"), cell("Not worth outreach: spam, gambling, e-commerce shop, product site, "
                             "content farm, or bot-walled page with no real content.")],
]
story.append(styled_table(lab_rows, [30 * mm, 130 * mm]))
story.append(P("Labeling was done from the crawled text alone, blind to nothing except the tier "
               "(the sample was drawn per tier). Borderline calls were kept: the notes column in "
               "the full table records the reason for each judgment. Final label counts: 22 GOOD, "
               "12 BORDERLINE, 6 BAD.", sBody))
story.append(P("Tier-to-label mapping used for testing: tiers A and B are expected GOOD, tier C is "
               "expected BORDERLINE, tier D is expected BAD.", sBody))

# ---------- 7. TEST RESULTS ----------
story.append(P("9. Test results", sH1))
correct = sum(1 for r in labeled
              if r["human_label"] ==
              {"A": "GOOD", "B": "GOOD", "C": "BORDERLINE", "D": "BAD"}[r["tier"]])
story.append(P("<b>Overall accuracy: %d of 40 (%.1f%%).</b> This is an honest result, reported "
               "without tuning the model to the test set. The confusion matrix and per-class "
               "metrics below show exactly where the model succeeds and fails."
               % (correct, 100 * correct / len(labeled)), sBody))
story.append(Spacer(1, 2 * mm))

cm = [
    hdr(["Predicted \\ Actual", "GOOD", "BORDERLINE", "BAD"]),
    [cell("A/B (GOOD)"), cell("14", sCellC), cell("6", sCellC), cell("0", sCellC)],
    [cell("C (BORDERLINE)"), cell("6", sCellC), cell("2", sCellC), cell("2", sCellC)],
    [cell("D (BAD)"), cell("2", sCellC), cell("4", sCellC), cell("4", sCellC)],
]
story.append(styled_table(cm, [40 * mm, 40 * mm, 40 * mm, 40 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(P("Table 1. Confusion matrix on the 40 hand-labeled blogs.", sNote))

pr = [
    hdr(["Class", "Precision", "Recall", "Predicted n", "Actual n"]),
    [cell("GOOD"), cell("0.70", sCellC), cell("0.64", sCellC),
     cell("20", sCellC), cell("22", sCellC)],
    [cell("BORDERLINE"), cell("0.20", sCellC), cell("0.17", sCellC),
     cell("10", sCellC), cell("12", sCellC)],
    [cell("BAD"), cell("0.40", sCellC), cell("0.67", sCellC),
     cell("10", sCellC), cell("6", sCellC)],
]
story.append(styled_table(pr, [32 * mm, 32 * mm, 32 * mm, 32 * mm, 32 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(P("Table 2. Per-class precision and recall.", sNote))
story.append(P("Reading the results: the model is good at recognizing strong outreach targets "
               "(14 of 20 A/B predictions were truly GOOD, precision 0.70) and it never called a "
               "truly BAD blog GOOD. Its weakness is the middle: tier C is a poor predictor of "
               "BORDERLINE, because genuine small blogs and low-quality sites land in the same "
               "score band.", sBody))

# ---------- 8. ERROR ANALYSIS ----------
story.append(P("10. Error analysis", sH1))
story.append(P("Twenty of the 40 labels mismatched the tier expectation. They fall into four "
               "honest failure modes:", sBody))
story.append(P("<b>1. Non-English blogs are systematically under-scored (2 misses).</b> "
               "blogdecomics.com (Spanish comics news, dated interviews) and ko.spaziocrypto.com "
               "(Korean crypto news, 1,679 articles) are genuinely GOOD blogs that landed in tier D. "
               "The date, byline and engagement patterns are English-only, so these dimensions "
               "score near zero for non-English sites. Fix: multilingual month-name and byline "
               "patterns.", sBody))
story.append(P("<b>2. Genuine small and personal blogs land in tier C (6 misses).</b> the6parkers.com, "
               "kellyfoota.com, microsmeta.com, psychicbloggers.com, bioterra.blogspot.com and "
               "glup2.blogspot.com are real, maintained blogs a buyer could reasonably target, but "
               "they lack engagement widgets and social-link signals, so they score in the 42-54 "
               "band. The model undervalues quiet, genuine blogs. Fix: weight named authorship and "
               "dated-post cadence more heavily relative to widget signals.", sBody))
story.append(P("<b>3. Service businesses and aggregators score too high (6 misses).</b> deldarlegal.com "
               "(law firm), officefinder.com (office brokerage), onliveserver.com (hosting company), "
               "trendkraft.io (PR SaaS), thehindiworld.com (results aggregator) and roshandaan.com "
               "(generalist aggregator) earn points for long marketing copy and dates, but they are "
               "not editorial blogs and will rarely accept guest posts. Fix: a business-site "
               "detector (pricing pages, service keywords, login walls) that caps the total.", sBody))
story.append(P("<b>4. Thin generalist blogs pass as solid (4 misses).</b> bmtimes.co.uk, bioscops.com, "
               "ardiz.blogspot.com and zonasantri.com look active enough to reach tier B or escape "
               "tier D, but carry red flags (a BriansClub promo post, SEO-generic filler, tag-cloud "
               "thinness). One miss in the other direction: primetimes.com.ng and omaneducportal.com "
               "are active non-English news/education portals the model could not credit. Fix: "
               "penalize known dark-pattern content and reward posting cadence even without "
               "English date formats.", sBody))
story.append(P("Deliberately not done: the model was not re-tuned on these 40 labels. Tuning to the "
               "test set would inflate the reported accuracy and misrepresent how the model "
               "behaves on new blogs.", sBody))
story.append(P("All 20 mismatches", sH2))
mm_rows = [hdr(["Blog", "Tier", "Expected", "Actual", "Failure mode"])]
mismatches = [
    ("deldarlegal.com", "A", "GOOD", "BORDERLINE", "Service business scored as blog (mode 3)"),
    ("roshandaan.com", "A", "GOOD", "BORDERLINE", "Generalist aggregator (mode 3)"),
    ("bmtimes.co.uk", "B", "GOOD", "BORDERLINE", "BriansClub promo red flag (mode 4)"),
    ("officefinder.com", "B", "GOOD", "BORDERLINE", "Service business (mode 3)"),
    ("thehindiworld.com", "B", "GOOD", "BORDERLINE", "Results aggregator (mode 3)"),
    ("bioscops.com", "B", "GOOD", "BORDERLINE", "Thin SEO-generalist (mode 4)"),
    ("the6parkers.com", "C", "BORDERLINE", "GOOD", "Genuine personal blog (mode 2)"),
    ("kellyfoota.com", "C", "BORDERLINE", "GOOD", "Genuine personal blog (mode 2)"),
    ("onliveserver.com", "C", "BORDERLINE", "BAD", "Hosting company, no blog (mode 3)"),
    ("trendkraft.io", "C", "BORDERLINE", "BAD", "SaaS product site (mode 3)"),
    ("microsmeta.com", "C", "BORDERLINE", "GOOD", "Real publication, weak signals (mode 2)"),
    ("psychicbloggers.com", "C", "BORDERLINE", "GOOD", "Real niche blog (mode 2)"),
    ("bioterra.blogspot.com", "C", "BORDERLINE", "GOOD", "Real blog, Portuguese text (modes 1, 2)"),
    ("glup2.blogspot.com", "C", "BORDERLINE", "GOOD", "Real blog, Spanish text (modes 1, 2)"),
    ("ardiz.blogspot.com", "D", "BAD", "BORDERLINE", "Real Indonesian blog, thin crawl (mode 4)"),
    ("omaneducportal.com", "D", "BAD", "BORDERLINE", "Real Arabic education portal (mode 4)"),
    ("blogdecomics.com", "D", "BAD", "GOOD", "Real Spanish blog, English-only signals (mode 1)"),
    ("ko.spaziocrypto.com", "D", "BAD", "GOOD", "Real Korean news portal (mode 1)"),
    ("zonasantri.com", "D", "BAD", "BORDERLINE", "Real Indonesian blog, thin crawl (mode 4)"),
    ("primetimes.com.ng", "D", "BAD", "BORDERLINE", "Active news site, thin aggregation (mode 4)"),
]
for m in mismatches:
    mm_rows.append([cell(m[0], ParagraphStyle("mc", parent=sCell, fontSize=7.5,
                                             leading=9.5)),
                    cell(m[1], sCellC), cell(m[2], sCellC), cell(m[3], sCellC),
                    cell(m[4], ParagraphStyle("mc2", parent=sCell, fontSize=7.5,
                                              leading=9.5))])
story.append(styled_table(mm_rows, [38 * mm, 14 * mm, 26 * mm, 26 * mm, 56 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(P("Table 3. Every test-set mismatch, with the failure mode from the analysis above.",
               sNote))

# ---------- 9. FULL LABELED TABLE ----------
story.append(P("11. Full labeled test set (40 blogs)", sH1))
story.append(P("Tier is the model prediction; human label is the hand judgment from the crawled "
               "text. Bold rows are mismatches.", sBody))
full = [hdr(["#", "Blog", "Tier", "Score", "Human label", "Notes"])]
expmap = {"A": "GOOD", "B": "GOOD", "C": "BORDERLINE", "D": "BAD"}
for i, r in enumerate(labeled, 1):
    mismatch = r["human_label"] != expmap[r["tier"]]
    dom = "<b>%s</b>" % r["domain"] if mismatch else r["domain"]
    lab = "<b>%s</b>" % r["human_label"] if mismatch else r["human_label"]
    full.append([cell(str(i), sCellC), cell(dom, ParagraphStyle(
                    "dc", parent=sCell, fontSize=7.5, leading=9.5)),
                 cell(r["tier"], sCellC), cell(r["total"], sCellC),
                 cell(lab, sCellC), cell(r["notes"], ParagraphStyle(
                     "nc", parent=sCell, fontSize=7.5, leading=9.5))])
story.append(styled_table(full, [8 * mm, 34 * mm, 12 * mm, 14 * mm,
                                 24 * mm, 68 * mm]))

# ---------- 12. OPERATIONAL USE ----------
story.append(P("12. Operational use for the marketplace team", sH1))
story.append(P("The model is a screening aid for the BlogReach outreach workflow, not a final "
               "decision maker. Recommended use of the tiers:", sBody))
use_rows = [
    hdr(["Tier", "Action"]),
    [cell("A", sCellC),
     cell("Priority outreach list. Verify the contact route (contact form or editor email) and "
          "pitch directly. Only 13 of 500 blogs reach this bar, so each one is worth manual "
          "effort.")],
    [cell("B", sCellC),
     cell("Standard outreach pool. Spot-check the site in a browser before pitching; most are "
          "solid, but service businesses and aggregators hide here.")],
    [cell("C", sCellC),
     cell("Manual review queue. This tier mixes genuine small blogs with thin sites; a one-minute "
          "human look correctly routes most of them. Do not bulk-pitch tier C.")],
    [cell("D", sCellC),
     cell("Excluded from outreach. Shops, betting sites, product pages and bot-walled domains. "
          "Re-screen only if the site changes.")],
]
story.append(styled_table(use_rows, [14 * mm, 146 * mm]))
story.append(P("Re-score on a fixed cadence (for example monthly), because publishing activity and "
               "site status change. Keep a fresh labeled sample for each re-test; never re-tune on "
               "the sample the accuracy is reported against.", sBody))

# ---------- 13. LIMITATIONS ----------
story.append(P("13. Limitations and next steps", sH1))
story.append(P("<b>Limitations.</b> (1) English-only signal patterns under-score non-English blogs. "
               "(2) Footer stripping in the crawl depresses legitimacy signals for all blogs. "
               "(3) The model sees text only: it cannot verify traffic, domain authority, or "
               "whether a site actually accepts guest posts. (4) 50% exact-tier accuracy means the "
               "model is a screening aid, not a decision maker; tier C especially needs human "
               "review.", sBody))
story.append(P("<b>Recommended next steps.</b> Add multilingual date/byline patterns; add a "
               "business-site detector to cap service and product sites; verify a sample of tier A "
               "blogs for live guest-post acceptance (contact page response test); and re-test on "
               "a fresh labeled sample after any change, never on this one.", sBody))
story.append(P("Files delivered with this report: <font face=\"Courier\" size=\"8\">"
               "data/scores.csv</font> (500 blogs with per-dimension scores, totals and tiers), "
               "<font face=\"Courier\" size=\"8\">data/labeled_test_set.csv</font> (40 hand-labeled "
               "rows with notes), <font face=\"Courier\" size=\"8\">hidden_files/score.py</font> "
               "(the scoring model).", sBody))

story.append(P("Appendix: reproducibility", sH1))
story.append(P("All artifacts for this task live under "
               "<font face=\"Courier\" size=\"8\">~/workspace/goals/blogreach-quality-scoring/</font>:",
               sBody))
rep_rows = [
    hdr(["Path", "Contents"]),
    [cell("<font face=\"Courier\" size=\"7.5\">data/scores.csv</font>"),
     cell("500 rows: domain, d1..d7, total (0-100), tier.")],
    [cell("<font face=\"Courier\" size=\"7.5\">data/labeled_test_set.csv</font>"),
     cell("40 rows: domain, tier, total, human_label, notes.")],
    [cell("<font face=\"Courier\" size=\"7.5\">data/texts/ (500 files)</font>"),
     cell("Crawled public homepage/about text, up to 8,000 chars each.")],
    [cell("<font face=\"Courier\" size=\"7.5\">data/blog_list_final.txt</font>"),
     cell("The 500 scored domains and their sources.")],
    [cell("<font face=\"Courier\" size=\"7.5\">data/classifications.csv</font>"),
     cell("Niche labels and confidence scores reused for D5.")],
    [cell("<font face=\"Courier\" size=\"7.5\">hidden_files/score.py</font>"),
     cell("The scoring model: features, dimensions, weights, tiers.")],
    [cell("<font face=\"Courier\" size=\"7.5\">hidden_files/build_pdf.py</font>"),
     cell("This report's generator.")],
]
story.append(styled_table(rep_rows, [62 * mm, 98 * mm]))
story.append(Spacer(1, 3 * mm))
story.append(P("To re-run: <font face=\"Courier\" size=\"8\">python3 hidden_files/score.py</font> "
               "re-scores all 500 blogs; <font face=\"Courier\" size=\"8\">python3 "
               "hidden_files/build_pdf.py</font> rebuilds this report. Both are deterministic: "
               "the labeled sample uses random seed 42, and every dimension is a fixed rule, so "
               "re-runs produce identical scores.", sBody))

doc = SimpleDocTemplate(
    os.path.join(OUT, "BlogReach-Blog-Quality-Scoring-Model-Report.pdf"),
    pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=16 * mm, bottomMargin=16 * mm,
    title="BlogReach.com: Blog Quality Scoring Model",
    author="BlogReach Task 82")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(18 * mm, 11 * mm,
                      "BlogReach.com Blog Quality Scoring Model | Task 82 | ZR-26-00763")
    canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, "Page %d" % doc.page)
    canvas.restoreState()


doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF built:", os.path.join(OUT,
      "BlogReach-Blog-Quality-Scoring-Model-Report.pdf"))
