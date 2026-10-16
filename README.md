# BlogReach.com: Blog Quality Scoring Model

Task 82 (Zeshan request ZR-26-00763, Part B Technical AI/ML and Development): a rubric and scoring model for blog outreach suitability on the BlogReach.com guest-posting marketplace, tested on hand-labeled examples. Built with public data only; no code, server, CMS or hosting access was used.

## What is here

- `score.py`: the scoring model. Reads crawled public blog text, computes 7 rubric dimensions (0-5 each), and produces a weighted 0-100 total with tiers A (67-100), B (55-66), C (42-54), D (0-41).
- `build_pdf.py`: builds the PDF report with reportlab.
- `data/scores.csv`: all 500 blogs with per-dimension scores, total, tier.
- `data/labeled_test_set.csv`: 40 hand-labeled blogs (GOOD / BORDERLINE / BAD) used to test the model.
- `report/BlogReach-Blog-Quality-Scoring-Model-Report.pdf`: the full report.

## Rubric (weights)

1. Content depth (20%)
2. Originality / spam-free (20%)
3. Publisher legitimacy (15%)
4. Editorial professionalism (15%)
5. Topical focus (10%)
6. Publishing activity (10%)
7. Audience engagement (10%)

Total = 100 * sum(w_i * d_i / 5).

## Test results

40 hand-labeled blogs, stratified 10 per predicted tier. Accuracy 50.0% (20 of 40). The model never labeled a truly BAD blog as GOOD. Tier C is the weak zone and needs human review. Full error analysis is in the report.

## Run it

```
python3 score.py
python3 build_pdf.py
```
