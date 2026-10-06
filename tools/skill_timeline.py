#!/usr/bin/env python3
"""Generate the skill-usage timelines in assets/.

    skill-timeline-vertical-{light,dark}.svg          full scroll-down timeline
    skill-timeline-vertical-recent-{light,dark}.svg   first RECENT orgs (shown in the README)
    skill-timeline-vertical-earlier-{light,dark}.svg  the rest (collapsed in the README)
    skill-timeline-{light,dark}.svg            horizontal Gantt variant
    docs/skills.html                           interactive explorer (filter, search, click a skill)

Source of truth: the engagements and skills below, derived from the CVs in
job_search/archetypes/*. Edit the data, rerun, commit the SVGs.

    python3 tools/skill_timeline.py
"""
from datetime import date
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"


def start(y, m):
    return y + (m - 1) / 12


def end(y, m):
    return y + m / 12


TODAY = date.today()
NOW = TODAY.year + (TODAY.month - 1) / 12 + TODAY.day / 365

# ---- engagements -------------------------------------------------------------
# id -> spans (decimal years); a skill lists the ids it was used in.
SPANS = {
    "tt": [(start(2019, 8), end(2019, 8))],
    "projs": [(start(2019, 4), end(2020, 12))],
    "travaris": [(start(2020, 7), end(2020, 8))],
    "talan": [(start(2021, 2), end(2021, 8))],
    "ubiai": [(start(2021, 11), end(2022, 9))],
    "ubi_plat": [(start(2021, 12), end(2022, 5))],
    "ubi_ann": [(start(2022, 5), end(2022, 9))],
    "elyadata": [(start(2022, 9), end(2024, 4))],
    "algo": [(start(2022, 9), end(2022, 11)), (start(2023, 3), end(2023, 4))],
    "allianz": [(start(2022, 12), end(2023, 4))],
    "elgenn": [(start(2023, 5), end(2023, 11))],
    "cahpp": [(start(2023, 11), end(2024, 2))],
    "infor": [(start(2024, 4), end(2026, 8))],
    "deda": [(start(2026, 9), NOW)],
}

# Vertical layout, newest first: (org label, dates, org id | None, [cards])
# card: (id, title, dates, blurb)
ORGS = [
    ("Dedagroup AI US", "Sep 2026 \u2013 now", None, [
        ("deda", "Senior Data Scientist, Gen AI & LLMs", "Sep 2026 \u2013 now",
         "ML and GenAI use cases, including credit scoring, on Python, Spring Boot and Dagster, deployed on Kubernetes."),
    ]),
    ("Infor IDeAS", "Apr 2024 – Aug 2026", None, [
        ("infor", "Data Science Engineer", "Apr 2024 – Aug 2026",
         "Inventory optimization, forecasting and pricing on ERP data. "
         "5 PoCs, 2 converted to subscriptions."),
    ]),
    ("Elyadata", "Sep 2022 – Apr 2024", "elyadata", [
        ("cahpp", "Software Consultant · CAHPP", "Nov 2023 – Feb 2024",
         "Medical product mapping with NER + fuzzy matching, >90% accuracy."),
        ("elgenn", "ELGENN internal product", "May 2023 – Nov 2023",
         "LLM inference APIs, document RAG, agentic SQL pipeline."),
        ("allianz", "Software Consultant · Allianz", "Dec 2022 – Apr 2023",
         "Real-time ML inference microservices for insurance models."),
        ("algo", "Software Data Engineer · Algobrain", "Sep 2022 – Apr 2023",
         "Kafka event-driven workflows, OCR and speech-to-text integrations."),
    ]),
    ("UBIAI", "Nov 2021 – Sep 2022", "ubiai", [
        ("ubi_ann", "Annotation tool platform", "May 2022 – Sep 2022",
         "GPT-3 document understanding, LayoutLM serving moved to Lambda."),
        ("ubi_plat", "NLP scientific documents platform", "Dec 2021 – May 2022",
         "Django backend on AWS, ~27x faster batch ingestion."),
    ]),
    ("ENICar, student years", "2018 \u2013 2021", None, [
        ("talan", "ML Intern, graduation project \u00b7 Talan", "Feb 2021 \u2013 Aug 2021",
         "Fake-news detection: satire and credibility models, bias metric, served as an API."),
        ("travaris", "Data Science Intern \u00b7 Travaris", "Jul 2020 \u2013 Aug 2020",
         "Geolocation clustering and a POI recommender prototype."),
        ("projs", "Student projects", "2019 \u2013 2020",
         "MERN web app, Discord bots, news scraper, Java desktop app. #1 in a Kaggle ML competition."),
        ("tt", "Java Developer Intern \u00b7 Tunisie Telecom", "Aug 2019",
         "Java Swing + Apache POI utility for a regional recovery system."),
    ]),
]

RECENT = 2  # README shows ORGS[:RECENT] inline, the rest behind <details>

H, L = 1.0, 0.42  # core vs supporting

GROUP_TITLES = {
    "backend": "Backend & Software",
    "ai": "LLMs & NLP",
    "data": "Data & ML",
    "store": "Databases & Storage",
    "cloud": "Cloud & DevOps",
}
# (name, group, [(engagement id, level)])
SKILLS = [
    ("Python", "backend", [("projs", H), ("travaris", H), ("talan", H), ("ubiai", H), ("elyadata", H), ("infor", H), ("deda", H)]),
    ("Java", "backend", [("tt", H), ("projs", H)]),
    ("C / C++", "backend", [("projs", H)]),
    ("Node.js / React (MERN)", "backend", [("projs", H)]),
    ("Django", "backend", [("ubi_plat", H)]),
    ("FastAPI", "backend", [("talan", H), ("ubi_plat", L), ("allianz", H), ("elgenn", H), ("cahpp", H)]),
    ("Flask", "backend", [("projs", L)]),
    ("Celery", "backend", [("elgenn", H), ("cahpp", H)]),
    ("Kafka", "backend", [("algo", H)]),
    ("Microservices / BFF", "backend", [("allianz", H), ("cahpp", H)]),
    ("Auth (JWT, 2FA)", "backend", [("allianz", H)]),
    ("Domain-Driven Design", "backend", [("cahpp", H)]),
    ("Pytest", "backend", [("allianz", H)]),
    ("Locust", "backend", [("elgenn", H)]),
    ("Spring Boot", "backend", [("deda", H)]),
    ("Vue.js", "backend", [("deda", H)]),
    ("Angular", "backend", [("ubi_plat", L), ("allianz", H)]),
    ("NLP / NER", "ai", [("talan", H), ("ubiai", H), ("cahpp", H)]),
    ("spaCy", "ai", [("ubiai", H)]),
    ("NLTK", "ai", [("ubiai", H)]),
    ("Gensim / topic modeling", "ai", [("ubi_plat", H)]),
    ("Keras / TensorFlow", "ai", [("projs", H)]),
    ("Clustering & recommenders", "ai", [("travaris", H)]),
    ("Document AI / OCR", "ai", [("ubi_ann", H), ("algo", L)]),
    ("Speech APIs (TTS / STT)", "ai", [("algo", H), ("elyadata", L)]),
    ("LLM APIs & prompting", "ai", [("ubi_ann", H), ("elgenn", H), ("cahpp", L), ("deda", H)]),
    ("LangChain", "ai", [("elgenn", H), ("cahpp", H)]),
    ("RAG / vector search", "ai", [("elgenn", H), ("cahpp", L), ("deda", H)]),
    ("Agents & tool-calling", "ai", [("elgenn", H), ("deda", H)]),
    ("Machine learning", "data", [("infor", H), ("deda", H)]),
    ("Credit scoring", "data", [("deda", H)]),
    ("Pandas / NumPy", "data", [("projs", L), ("ubi_plat", H), ("allianz", L), ("infor", H)]),
    ("Scikit-learn", "data", [("projs", L), ("allianz", L), ("deda", H)]),
    ("Web scraping (BS4, Selenium)", "data", [("projs", H), ("travaris", H), ("talan", H)]),
    ("PySpark", "data", [("infor", H)]),
    ("Forecasting (XGBoost, Prophet)", "data", [("infor", H)]),
    ("Simulation & optimization", "data", [("infor", H)]),
    ("MLflow", "data", [("elgenn", L), ("infor", H), ("deda", H)]),
    ("Optuna (tuning & observability)", "data", [("infor", H), ("deda", H)]),
    ("XAI (explainability)", "data", [("infor", H), ("deda", H)]),
    ("Kedro", "data", [("elgenn", L)]),
    ("Orchestration (Dagster, Airflow, ION)", "data", [("infor", H), ("deda", H)]),
    ("Tableau / Birst", "data", [("infor", L)]),
    ("SQL", "store", [("infor", H)]),
    ("SQL / PostgreSQL", "store", [("allianz", H), ("elgenn", H), ("cahpp", H), ("deda", H)]),
    ("MySQL", "store", [("tt", H), ("projs", H)]),
    ("MongoDB", "store", [("projs", H), ("travaris", H), ("allianz", L), ("elyadata", L)]),
    ("Elasticsearch", "store", [("elyadata", L)]),
    ("pgvector / Milvus", "store", [("elgenn", H), ("cahpp", L)]),
    ("Neo4j", "store", [("ubi_plat", L)]),
    ("S3 / Data Lake", "store", [("ubi_plat", L), ("infor", H)]),
    ("AWS (Lambda, ECS, EC2)", "cloud", [("ubiai", H)]),
    ("Docker", "cloud", [("ubi_plat", H), ("allianz", H)]),
    ("Kubernetes / Helm", "cloud", [("allianz", H), ("deda", H)]),
    ("Jenkins CI/CD", "cloud", [("allianz", H)]),
    ("Azure Blob", "cloud", [("allianz", L)]),
]

THEMES = {
    "light": dict(
        bg="#ffffff", text="#1f2328", muted="#656d76", grid="#d8dee4", row="#f6f8fa",
        card="#f6f8fa", border="#d0d7de",
        backend="#4f46e5", ai="#c026d3", data="#0d9488", store="#16a34a", cloud="#d97706",
        lane_a="#24292f", lane_b="#57606a", lane_text="#ffffff", now="#cf222e",
        chip_text="#ffffff", spine="#d0d7de",
    ),
    "dark": dict(
        bg="#0d1117", text="#e6edf3", muted="#8b949e", grid="#30363d", row="#161b22",
        card="#161b22", border="#30363d",
        backend="#818cf8", ai="#e879f9", data="#2dd4bf", store="#4ade80", cloud="#fbbf24",
        lane_a="#e6edf3", lane_b="#8b949e", lane_text="#0d1117", now="#ff7b72",
        chip_text="#0d1117", spine="#30363d",
    ),
}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def merge(spans, gap=0.25):
    """Join touching spans of the same level so translucent bars show no seams."""
    merged = []
    for (a, b), lvl in sorted(spans, key=lambda s: (s[1], s[0][0])):
        if merged and merged[-1][1] == lvl and a <= merged[-1][0][1] + gap:
            (pa, pb), _ = merged[-1]
            merged[-1] = ((pa, max(pb, b)), lvl)
        else:
            merged.append(((a, b), lvl))
    return merged


def skill_spans(uses):
    return [(span, lvl) for eid, lvl in uses for span in SPANS[eid]]


def svg_open(w, h, label, c):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{FONT}" role="img" aria-label="{escape(label)}">',
        f'<rect width="{w}" height="{h}" rx="14" fill="{c["bg"]}"/>',
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{c["border"]}"/>',
    ]


def write(name, lines):
    OUT.mkdir(exist_ok=True)
    path = OUT / name
    path.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", path)


# ==== vertical ==================================================================
VW = 860
SPINE_X = 128
CARD_X = 162
CARD_W = VW - CARD_X - 24
CHIP_H = 22
CHIP_GAP = 6
THROUGH_W = 118  # label column of the "throughout" row


def chip_w(text):
    return len(text) * 6.3 + 24


def chip_rows(chips, width):
    """Greedy flow layout -> rows of (x, chip, width)."""
    rows, row, x = [], [], 0
    for chip in chips:
        w = chip_w(chip[0])
        if row and x + w > width:
            rows.append(row)
            row, x = [], 0
        row.append((x, chip, w))
        x += w + CHIP_GAP
    if row:
        rows.append(row)
    return rows


def rows_h(rows):
    return len(rows) * (CHIP_H + CHIP_GAP) - CHIP_GAP if rows else 0


def draw_chips(add, rows, x0, y0, c):
    for r, row in enumerate(rows):
        y = y0 + r * (CHIP_H + CHIP_GAP)
        for x, (name, group, lvl), w in row:
            col = c[group]
            if lvl >= 1:
                add(f'<rect x="{x0 + x:.1f}" y="{y}" width="{w:.1f}" height="{CHIP_H}" rx="11" fill="{col}"/>')
                tc = c["chip_text"]
            else:
                add(f'<rect x="{x0 + x + .75:.1f}" y="{y + .75}" width="{w - 1.5:.1f}" height="{CHIP_H - 1.5}" '
                    f'rx="10.25" fill="none" stroke="{col}" stroke-width="1.5"/>')
                tc = col
            add(f'<text x="{x0 + x + w / 2:.1f}" y="{y + 15}" font-size="11.5" font-weight="600" '
                f'text-anchor="middle" fill="{tc}">{escape(name)}</text>')


def skills_for(eid):
    return [(n, g, lvl) for gkey in GROUP_TITLES for n, g, uses in SKILLS if g == gkey
            for uid, lvl in uses if uid == eid]


def layout_vertical(add, c, orgs):
    y = 122
    for org, org_dates, org_id, cards in orgs:
        add(f'<rect x="{SPINE_X - 14}" y="{y}" width="{VW - SPINE_X - 10}" height="30" rx="15" fill="{c["lane_a"]}"/>')
        add(f'<text x="{SPINE_X + 6}" y="{y + 19.5}" font-size="13" font-weight="700" fill="{c["lane_text"]}">{escape(org)}</text>')
        add(f'<text x="{VW - 30}" y="{y + 19.5}" font-size="11.5" text-anchor="end" fill="{c["lane_text"]}" '
            f'fill-opacity=".75">{escape(org_dates)}</text>')
        y += 44
        for eid, title, dates, blurb in cards:
            rows = chip_rows(skills_for(eid), CARD_W - 32)
            card_h = 62 + rows_h(rows) + 16
            add(f'<circle cx="{SPINE_X}" cy="{y + 22}" r="6" fill="{c["bg"]}" stroke="{c["lane_b"]}" stroke-width="2.5"/>')
            add(f'<rect x="{CARD_X}" y="{y}" width="{CARD_W}" height="{card_h}" rx="12" fill="{c["card"]}" stroke="{c["border"]}"/>')
            add(f'<text x="{CARD_X + 16}" y="{y + 26}" font-size="14" font-weight="700" fill="{c["text"]}">{escape(title)}</text>')
            if not (len(cards) == 1 and dates == org_dates):  # the org pill already shows it
                add(f'<text x="{CARD_X + CARD_W - 16}" y="{y + 26}" font-size="11.5" text-anchor="end" fill="{c["muted"]}">{escape(dates)}</text>')
            add(f'<text x="{CARD_X + 16}" y="{y + 46}" font-size="12" fill="{c["muted"]}">{escape(blurb)}</text>')
            draw_chips(add, rows, CARD_X + 16, y + 60, c)
            y += card_h + 14
        chips = skills_for(org_id) if org_id else []
        if chips:
            rows = chip_rows(chips, CARD_W - THROUGH_W)
            add(f'<text x="{CARD_X}" y="{y + 15}" font-size="10.5" font-weight="700" letter-spacing="1" '
                f'fill="{c["muted"]}">THROUGHOUT</text>')
            draw_chips(add, rows, CARD_X + THROUGH_W, y, c)
            y += rows_h(rows) + 16
        y += 10
    return y


def render_vertical(name, c, orgs=ORGS, suffix="", title="Skills, as they were used",
                    subtitle="Newest first. Every chip is a tool from a real engagement, not a self-rated level."):
    body = []
    end_y = layout_vertical(body.append, c, orgs)
    legend_y = end_y + 2
    height = legend_y + 44

    out = svg_open(VW, height, "Vertical timeline of skills by engagement, 2019 to today", c)
    add = out.append
    add(f'<text x="28" y="42" font-size="22" font-weight="700" fill="{c["text"]}">{escape(title)}</text>')
    add(f'<text x="28" y="64" font-size="12.5" fill="{c["muted"]}">{escape(subtitle)}</text>')
    add(f'<rect x="28" y="78" width="46" height="22" rx="11" fill="{c["backend"]}"/>')
    add(f'<text x="51" y="93" font-size="11.5" font-weight="600" text-anchor="middle" fill="{c["chip_text"]}">core</text>')
    add(f'<text x="84" y="93" font-size="11.5" fill="{c["muted"]}">central to the work</text>')
    add(f'<rect x="228.75" y="78.75" width="76.5" height="20.5" rx="10.25" fill="none" '
        f'stroke="{c["backend"]}" stroke-width="1.5"/>')
    add(f'<text x="267" y="93" font-size="11.5" font-weight="600" text-anchor="middle" fill="{c["backend"]}">supporting</text>')
    add(f'<text x="316" y="93" font-size="11.5" fill="{c["muted"]}">used alongside</text>')
    add(f'<line x1="{SPINE_X}" y1="122" x2="{SPINE_X}" y2="{end_y - 14}" stroke="{c["spine"]}" stroke-width="3" stroke-linecap="round"/>')
    out.extend(body)
    kx = 28
    for gkey, gtitle in GROUP_TITLES.items():
        add(f'<circle cx="{kx + 5}" cy="{legend_y + 14}" r="5" fill="{c[gkey]}"/>')
        add(f'<text x="{kx + 16}" y="{legend_y + 18}" font-size="11.5" fill="{c["muted"]}">{escape(gtitle)}</text>')
        kx += 34 + len(gtitle) * 6.2
    add(f'<text x="{VW - 28}" y="{legend_y + 18}" font-size="10.5" text-anchor="end" fill="{c["muted"]}">generated by tools/skill_timeline.py</text>')
    add("</svg>")
    write(f"skill-timeline-vertical{suffix}-{name}.svg", out)


# ==== horizontal ================================================================
W = 980
LABEL_W = 218
PAD_R = 24
X0, X1 = LABEL_W, W - PAD_R
T0, T1 = 2019.4, 2027.0
ROW_H = 22

ROLES = [("ENICar", (start(2018, 9), end(2021, 10)), "b"), ("UBIAI", SPANS["ubiai"][0], "a"), ("Elyadata", SPANS["elyadata"][0], "b"),
         ("Infor IDeAS", SPANS["infor"][0], "a"),
         ("Dedagroup AI US", SPANS["deda"][0], "b")]


def px(t):
    return X0 + (min(max(t, T0), T1) - T0) / (T1 - T0) * (X1 - X0)


def render_horizontal(name, c):
    groups = [(t, k, [(n, skill_spans(u)) for n, g, u in SKILLS if g == k]) for k, t in GROUP_TITLES.items()]
    y_axis, y_lane = 74, 100
    y = y_lane + 74
    body_top = y
    for _, _, skills in groups:
        y += 34 + len(skills) * ROW_H
    body_bottom = y
    legend_y = body_bottom + 18
    height = legend_y + 36

    out = svg_open(W, height, f"Timeline of skill usage from 2019 to {TODAY.year}", c)
    add = out.append
    add(f'<text x="28" y="40" font-size="20" font-weight="700" fill="{c["text"]}">Skills, as they were used</text>')
    add(f'<text x="28" y="60" font-size="12" fill="{c["muted"]}">'
        f'Each bar is a real engagement, {int(T0)}–{TODAY.year}. Not self-rated levels.</text>')
    for yr in range(int(T0) + 1, int(T1) + 1):
        if yr > TODAY.year + 0.99:
            continue
        x = px(yr)
        add(f'<line x1="{x:.1f}" y1="{y_axis + 6}" x2="{x:.1f}" y2="{body_bottom}" stroke="{c["grid"]}" stroke-dasharray="2 4"/>')
        add(f'<text x="{x:.1f}" y="{y_axis}" font-size="12" font-weight="600" text-anchor="middle" fill="{c["muted"]}">{yr}</text>')
    add(f'<text x="28" y="{y_lane + 19}" font-size="11" font-weight="700" letter-spacing="1" fill="{c["muted"]}">WHERE</text>')
    for label, (a, b), kind in ROLES:
        xa, xb = px(a), px(b)
        fill = c["lane_a"] if kind == "a" else c["lane_b"]
        add(f'<rect x="{xa:.1f}" y="{y_lane}" width="{xb - xa:.1f}" height="28" rx="14" fill="{fill}"/>')
        if xb - xa < 80:  # too narrow for the label: set it above the pill, right-aligned
            add(f'<text x="{xb:.1f}" y="{y_lane - 6}" font-size="11" font-weight="600" text-anchor="end" '
                f'fill="{c["text"]}">{escape(label)}</text>')
            continue
        add(f'<text x="{(xa + xb) / 2:.1f}" y="{y_lane + 18.5}" font-size="12" font-weight="600" '
            f'text-anchor="middle" fill="{c["lane_text"]}">{escape(label)}</text>')
    for eid, label in (("tt", "T. Telecom"), ("travaris", "Travaris"), ("talan", "Talan"), ("algo", "Algobrain"),
                       ("allianz", "Allianz"), ("elgenn", "ELGENN"), ("cahpp", "CAHPP")):
        for a, b in SPANS[eid]:
            add(f'<rect x="{px(a):.1f}" y="{y_lane + 34}" width="{max(px(b) - px(a), 5):.1f}" height="16" rx="8" '
                f'fill="{c["lane_b"]}" fill-opacity=".22"/>')
        a, b = SPANS[eid][0]
        add(f'<text x="{(px(a) + px(b)) / 2:.1f}" y="{y_lane + 62}" font-size="9.5" text-anchor="middle" '
            f'fill="{c["muted"]}">{label}</text>')

    y = body_top
    for gtitle, gkey, skills in groups:
        color = c[gkey]
        add(f'<rect x="20" y="{y + 4}" width="4" height="14" rx="2" fill="{color}"/>')
        add(f'<text x="32" y="{y + 16}" font-size="11" font-weight="700" letter-spacing="1" fill="{color}">{escape(gtitle.upper())}</text>')
        y += 34
        for i, (skill, spans) in enumerate(skills):
            if i % 2 == 0:
                add(f'<rect x="12" y="{y - 3}" width="{W - 24}" height="{ROW_H}" rx="6" fill="{c["row"]}"/>')
            add(f'<text x="{LABEL_W - 12}" y="{y + 12}" font-size="12" text-anchor="end" fill="{c["text"]}">{escape(skill)}</text>')
            for (a, b), lvl in merge(spans):
                add(f'<rect x="{px(a):.1f}" y="{y + 1}" width="{max(px(b) - px(a), 4):.1f}" height="12" rx="6" '
                    f'fill="{color}" fill-opacity="{lvl}"/>')
            y += ROW_H
    xn = px(NOW)
    add(f'<line x1="{xn:.1f}" y1="{y_lane - 8}" x2="{xn:.1f}" y2="{body_bottom}" stroke="{c["now"]}" stroke-width="1.5"/>')
    add(f'<circle cx="{xn:.1f}" cy="{y_lane - 8}" r="3.5" fill="{c["now"]}"/>')
    add(f'<rect x="32" y="{legend_y}" width="26" height="10" rx="5" fill="{c["backend"]}"/>')
    add(f'<text x="66" y="{legend_y + 9}" font-size="11" fill="{c["muted"]}">core to the work</text>')
    add(f'<rect x="170" y="{legend_y}" width="26" height="10" rx="5" fill="{c["backend"]}" fill-opacity="{L}"/>')
    add(f'<text x="204" y="{legend_y + 9}" font-size="11" fill="{c["muted"]}">supporting / used alongside</text>')
    add(f'<line x1="400" y1="{legend_y - 1}" x2="400" y2="{legend_y + 11}" stroke="{c["now"]}" stroke-width="1.5"/>')
    add(f'<text x="410" y="{legend_y + 9}" font-size="11" fill="{c["muted"]}">today</text>')
    add(f'<text x="{W - 28}" y="{legend_y + 9}" font-size="11" text-anchor="end" fill="{c["muted"]}">generated by tools/skill_timeline.py</text>')
    add("</svg>")
    write(f"skill-timeline-{name}.svg", out)


# ==== interactive ===============================================================
HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Khaled Adrani, skills explorer</title>
<style>
:root{--bg:#fff;--fg:#1f2328;--mut:#656d76;--card:#f6f8fa;--bd:#d0d7de;--pill:#24292f;--pilltx:#fff;
--backend:#4f46e5;--ai:#c026d3;--data:#0d9488;--store:#16a34a;--cloud:#d97706;--chiptx:#fff;--now:#cf222e}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--mut:#8b949e;--card:#161b22;--bd:#30363d;
--pill:#e6edf3;--pilltx:#0d1117;--backend:#818cf8;--ai:#e879f9;--data:#2dd4bf;--store:#4ade80;--cloud:#fbbf24;--chiptx:#0d1117;--now:#ff7b72}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
main{max-width:920px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:26px;margin:0 0 4px}
.sub{color:var(--mut);margin:0 0 16px;font-size:14px}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0 12px;border-bottom:1px solid var(--bd)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}
input[type=search]{flex:1 1 220px;min-width:0;padding:8px 12px;border-radius:999px;border:1px solid var(--bd);background:var(--card);color:var(--fg);font:inherit}
.cat,.tog{border:1.5px solid var(--c,var(--bd));background:transparent;color:var(--c,var(--fg));border-radius:999px;padding:4px 12px;font:600 12.5px inherit;font-family:inherit;cursor:pointer}
.cat.on{background:var(--c);color:var(--chiptx)}
.tog{--c:var(--mut)}.tog.on{background:var(--mut);color:var(--bg)}
.panel{margin-top:6px;min-height:92px;font-size:13.5px;color:var(--mut)}
.panel b{color:var(--fg)}
.panel svg{width:100%;height:46px;display:block;margin-top:6px}
.org{display:flex;justify-content:space-between;align-items:center;background:var(--pill);color:var(--pilltx);border-radius:999px;padding:5px 16px;font-weight:700;font-size:14px;margin:26px 0 12px}
.org span{font-weight:400;font-size:12.5px;opacity:.75}
.thr{display:flex;gap:8px;align-items:flex-start;margin:0 0 10px 34px}
.thr small{flex:none;width:92px;padding-top:4px;color:var(--mut);font-weight:700;letter-spacing:.08em;font-size:10.5px}
.card{margin:0 0 12px 34px;padding:12px 16px 12px;background:var(--card);border:1px solid var(--bd);border-radius:12px;position:relative;transition:opacity .15s,box-shadow .15s}
.card:before{content:"";position:absolute;left:-30px;top:18px;width:11px;height:11px;border-radius:50%;background:var(--bg);border:2.5px solid var(--mut)}
.card:after{content:"";position:absolute;left:-25px;top:-14px;bottom:-14px;width:3px;background:var(--bd);z-index:-1}
.card h3{margin:0;font-size:15px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;cursor:pointer}
.card h3 em{font:400 12.5px inherit;font-family:inherit;color:var(--mut)}
.card p{margin:2px 0 8px;color:var(--mut);font-size:13px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{--c:var(--backend);border:1.5px solid var(--c);border-radius:999px;padding:2px 11px;font:600 12px/18px inherit;font-family:inherit;cursor:pointer;background:var(--c);color:var(--chiptx);transition:opacity .15s,transform .1s}
.chip.sup{background:transparent;color:var(--c)}
.chip:hover{transform:translateY(-1px)}
.chip[hidden]{display:none}
body.sel .card:not(.hit){opacity:.28}
body.sel .chip:not(.sel){opacity:.35}
.card.hit{box-shadow:0 0 0 2px var(--hl,var(--mut))}
.card.hidden,.thr.hidden{display:none}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:var(--mut);margin-top:28px}
.legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;background:var(--c)}
.empty{display:none;text-align:center;color:var(--mut);padding:40px 0}
</style>
</head>
<body>
<main>
<h1>Skills, as they were used</h1>
<p class="sub">Filter by category, search, or click any skill to see where and for how long it was used. Click a card title to light up its skills.</p>
<div class="bar">
  <div class="row"><input id="q" type="search" placeholder="Search skills, e.g. rag, kafka, postgres" aria-label="Search skills"></div>
  <div class="row" id="cats"></div>
  <div class="row"><button class="tog" id="core">Core only</button><button class="tog" id="clear">Clear selection</button></div>
  <div class="panel" id="panel"></div>
</div>
<div id="tl"></div>
<div class="empty" id="empty">No skills match.</div>
<div class="legend" id="legend"></div>
</main>
<script>
const D = __DATA__;
const T0 = D.t0, T1 = D.t1, NOW = D.now;
const GROUPS = D.groups, SPANS = D.spans;
const state = {cats: new Set(Object.keys(GROUPS)), q: "", core: false, sel: null};
const $ = (s) => document.querySelector(s);
const el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.textContent = h; return e; };
const col = (g) => `var(--${g})`;

// ---- skill index ----
const skillByName = Object.fromEntries(D.skills.map(s => [s.name, s]));
function spansOf(skill) {
  const out = [];
  skill.uses.forEach(u => (SPANS[u[0]] || []).forEach(sp => out.push(sp)));
  out.sort((a, b) => a[0] - b[0]);
  const m = [];
  out.forEach(([a, b]) => { if (m.length && a <= m[m.length-1][1] + 0.02) m[m.length-1][1] = Math.max(m[m.length-1][1], b); else m.push([a, b]); });
  return m;
}
const fmt = (t) => { const y = Math.floor(t + 1e-9), mo = Math.min(11, Math.floor((t - y) * 12 + 1e-6)); return ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][mo] + " " + y; };

// ---- build ----
const tl = $("#tl");
D.orgs.forEach(org => {
  const h = el("div", "org", org.label); h.appendChild(el("span", "", org.dates)); tl.appendChild(h);
  const mk = (id) => {
    const box = el("div", "chips");
    D.skills.filter(s => s.uses.some(u => u[0] === id)).sort((a, b) => D.order.indexOf(a.group) - D.order.indexOf(b.group)).forEach(s => {
      const lvl = s.uses.find(u => u[0] === id)[1];
      const c = el("button", "chip" + (lvl < 1 ? " sup" : ""), s.name);
      c.style.setProperty("--c", col(s.group)); c.dataset.skill = s.name; c.dataset.group = s.group; c.dataset.lvl = lvl;
      c.title = (lvl < 1 ? "Supporting" : "Core") + " · " + GROUPS[s.group];
      c.onclick = (e) => { e.stopPropagation(); select(state.sel === s.name ? null : s.name); };
      box.appendChild(c);
    });
    return box;
  };
  org.cards.forEach(cd => {
    const c = el("div", "card"); c.dataset.id = cd.id;
    const t = el("h3", "", cd.title); if (!(org.cards.length === 1 && cd.dates === org.dates)) t.appendChild(el("em", "", cd.dates));
    t.onclick = () => selectCard(cd.id);
    c.appendChild(t); c.appendChild(el("p", "", cd.blurb)); c.appendChild(mk(cd.id)); tl.appendChild(c);
  });
  if (org.org_id) {
    const row = el("div", "thr"); row.appendChild(el("small", "", "THROUGHOUT")); row.appendChild(mk(org.org_id)); tl.appendChild(row);
  }
});
const cats = $("#cats");
Object.entries(GROUPS).forEach(([k, name]) => {
  const b = el("button", "cat on", name); b.style.setProperty("--c", col(k)); b.dataset.k = k;
  b.onclick = () => { state.cats.has(k) ? state.cats.delete(k) : state.cats.add(k); b.classList.toggle("on"); apply(); };
  cats.appendChild(b);
  const l = el("span"); const i = el("i"); i.style.setProperty("--c", col(k)); l.appendChild(i); l.appendChild(document.createTextNode(name)); $("#legend").appendChild(l);
});
$("#q").oninput = (e) => { state.q = e.target.value.trim().toLowerCase(); apply(); };
$("#core").onclick = (e) => { state.core = !state.core; e.target.classList.toggle("on"); apply(); };
$("#clear").onclick = () => select(null);
document.addEventListener("keydown", (e) => { if (e.key === "Escape") select(null); });

// ---- behaviour ----
function select(name) {
  state.sel = name; state.card = null;
  history.replaceState(null, "", name ? "#skill=" + encodeURIComponent(name) : location.pathname);
  apply();
}
function selectCard(id) { state.sel = null; state.card = state.card === id ? null : id; apply(); }

function apply() {
  const filtering = state.q || state.core || state.cats.size < Object.keys(GROUPS).length;
  document.querySelectorAll(".chip").forEach(c => {
    const ok = state.cats.has(c.dataset.group) && (!state.q || c.dataset.skill.toLowerCase().includes(state.q)) && (!state.core || +c.dataset.lvl >= 1);
    c.hidden = !ok;
    c.classList.toggle("sel", c.dataset.skill === state.sel);
  });
  let shown = 0;
  document.querySelectorAll(".card, .thr").forEach(n => {
    const vis = n.querySelectorAll(".chip:not([hidden])").length;
    n.classList.toggle("hidden", filtering && !vis);
    if (n.classList.contains("card")) {
      const uses = state.sel && skillByName[state.sel].uses.some(u => u[0] === n.dataset.id);
      const parent = state.sel && D.parents[n.dataset.id] && skillByName[state.sel].uses.some(u => u[0] === D.parents[n.dataset.id]);
      n.classList.toggle("hit", !!(uses || parent || state.card === n.dataset.id));
      if (vis) shown++;
    }
  });
  document.body.classList.toggle("sel", !!(state.sel || state.card));
  $("#empty").style.display = filtering && !shown ? "block" : "none";
  if (state.card) {
    const cid = state.card;
    document.querySelectorAll(".card").forEach(n => n.classList.toggle("hit", n.dataset.id === cid));
    document.querySelectorAll(".chip").forEach(c => c.classList.toggle("sel", !!c.closest(".card[data-id='" + cid + "']")));
  }
  panel();
}

function panel() {
  const p = $("#panel");
  if (!state.sel) {
    const n = D.skills.length, m = D.orgs.reduce((a, o) => a + o.cards.length, 0);
    p.innerHTML = state.card ? "<b>" + (document.querySelector(".card[data-id='" + state.card + "'] h3").firstChild.textContent) + "</b>: its skills are highlighted. Click the title again to clear."
      : "<b>" + n + " skills</b> across <b>" + m + " engagements</b>, " + Math.floor(T0) + " to today. Solid chips were core to the work, outlined chips were used alongside.";
    return;
  }
  const s = skillByName[state.sel], sp = spansOf(s);
  const months = Math.round(sp.reduce((a, [x, y]) => a + (y - x) * 12, 0));
  const yrs = months >= 24 ? (months / 12).toFixed(1).replace(".0", "") + " years" : months + " month" + (months === 1 ? "" : "s");
  const ids = s.uses.map(u => u[0]);
  const where = D.orgs.flatMap(o => o.cards).filter(c => ids.includes(c.id) || ids.includes(D.parents[c.id])).map(c => c.title.split(" · ")[0]);
  const W = 1000, x = (t) => (Math.min(Math.max(t, T0), T1) - T0) / (T1 - T0) * W;
  let svg = `<svg viewBox="0 0 ${W} 46" preserveAspectRatio="none" aria-hidden="true">`;
  for (let y = Math.ceil(T0); y <= Math.floor(NOW); y++) svg += `<line x1="${x(y)}" x2="${x(y)}" y1="0" y2="30" stroke="currentColor" opacity=".25" stroke-dasharray="3 5"/>`;
  sp.forEach(([a, b]) => svg += `<rect x="${x(a)}" y="6" width="${Math.max(x(b) - x(a), 6)}" height="18" rx="9" fill="${col(s.group)}"/>`);
  svg += `<line x1="${x(NOW)}" x2="${x(NOW)}" y1="0" y2="30" stroke="var(--now)" stroke-width="2"/></svg>`;
  let ticks = ""; for (let y = Math.ceil(T0); y <= Math.floor(NOW); y++) ticks += `<span style="position:absolute;left:${(y - T0) / (T1 - T0) * 100}%;transform:translateX(-50%)">${y}</span>`;
  p.innerHTML = `<b style="color:${col(s.group)}">${s.name}</b> · ${GROUPS[s.group]} · <b>${yrs}</b> in use, ${fmt(sp[0][0])} to ${sp[sp.length-1][1] >= NOW - 0.05 ? "today" : fmt(sp[sp.length-1][1] - 0.01)}<br>${where.join(", ")}` +
    svg + `<div style="position:relative;height:16px;font-size:11px">${ticks}</div>`;
}

const m = location.hash.match(/skill=([^&]+)/);
if (m && skillByName[decodeURIComponent(m[1])]) state.sel = decodeURIComponent(m[1]);
apply();
</script>
</body>
</html>
"""


def render_interactive():
    import json
    data = {
        "t0": T0, "t1": T1, "now": NOW,
        "groups": GROUP_TITLES, "order": list(GROUP_TITLES),
        "spans": {k: [list(sp) for sp in v] for k, v in SPANS.items()},
        "skills": [{"name": n, "group": g, "uses": [list(u) for u in uses]} for n, g, uses in SKILLS],
        "orgs": [{"label": o, "dates": d, "org_id": oid,
                  "cards": [{"id": i, "title": t, "dates": dt, "blurb": b} for i, t, dt, b in cards]}
                 for o, d, oid, cards in ORGS],
        "parents": {"ubi_plat": "ubiai", "ubi_ann": "ubiai", "cahpp": "elyadata", "elgenn": "elyadata",
                    "allianz": "elyadata", "algo": "elyadata"},
    }
    path = OUT.parent / "docs" / "skills.html"
    path.parent.mkdir(exist_ok=True)
    path.write_text(HTML.replace("__DATA__", json.dumps(data)), encoding="utf-8")
    print("wrote", path)


if __name__ == "__main__":
    for n, c in THEMES.items():
        render_vertical(n, c)
        render_vertical(n, c, ORGS[:RECENT], "-recent")
        render_vertical(n, c, ORGS[RECENT:], "-earlier", "Earlier engagements",
                        "2018 \u2013 2024: consulting, platform work and student years.")
        render_horizontal(n, c)
    render_interactive()
