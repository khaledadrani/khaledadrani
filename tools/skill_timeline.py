#!/usr/bin/env python3
"""Generate assets/skill-timeline-{light,dark}.svg: skill usage across the years.

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

# ---- engagements (start, end) ------------------------------------------------
UBI_ALL = (start(2021, 11), end(2022, 9))
UBI_PLAT = (start(2021, 12), end(2022, 5))  # NLP scientific documents platform
UBI_ANN = (start(2022, 5), end(2022, 9))  # annotation tool platform
ALGO_1 = (start(2022, 9), end(2022, 11))
ALGO_2 = (start(2023, 3), end(2023, 4))
ALLIANZ = (start(2022, 12), end(2023, 4))
ELGENN = (start(2023, 5), end(2023, 11))
CAHPP = (start(2023, 11), end(2024, 2))
ELYADATA = (start(2022, 9), end(2024, 4))
INFOR = (start(2024, 4), NOW)
AGENT = (start(2026, 1), NOW)  # local coding agent
FT = (start(2026, 5), NOW)  # LLM fine-tuning

ROLES = [  # (label, span, kind)
    ("UBIAI", UBI_ALL, "a"),
    ("Elyadata", ELYADATA, "b"),
    ("Infor IDeAS", INFOR, "a"),
]
ENGAGEMENTS = [  # thin ticks under the Elyadata lane
    ("Algobrain", ALGO_1),
    ("Allianz", ALLIANZ),
    ("Algobrain", ALGO_2),
    ("ELGENN", ELGENN),
    ("CAHPP", CAHPP),
]
SIDE = [("Side projects", AGENT)]

H, L = 1.0, 0.42  # core vs supporting

# group -> [(skill, [(span, level)])]
GROUPS = [
    ("Backend & Software", "backend", [
        ("Python", [(UBI_ALL, H), ((start(2022, 9), NOW), H)]),
        ("Django", [(UBI_PLAT, H)]),
        ("FastAPI", [(UBI_PLAT, L), (ALLIANZ, H), (ELGENN, H), (CAHPP, H)]),
        ("Celery", [(ELGENN, H), (CAHPP, H)]),
        ("Kafka", [(ALGO_1, H), (ALGO_2, H)]),
        ("Domain-Driven Design", [(CAHPP, H)]),
        ("Pytest", [(ALLIANZ, H)]),
        ("Locust", [(ELGENN, H)]),
        ("Angular", [(UBI_PLAT, L)]),
    ]),
    ("LLMs & NLP", "ai", [
        ("NLP / NER", [(UBI_ALL, H), (CAHPP, H)]),
        ("spaCy", [(UBI_ALL, H)]),
        ("NLTK", [(UBI_ALL, H)]),
        ("Document AI / OCR", [(UBI_ANN, H), (ALGO_1, L), (ALGO_2, L)]),
        ("LLM APIs & prompting", [(UBI_ANN, H), (ELGENN, H), (CAHPP, L), (FT, H)]),
        ("LangChain", [(ELGENN, H), (CAHPP, H)]),
        ("RAG / vector search", [(ELGENN, H), (CAHPP, L)]),
        ("Agents & tool-calling", [(ELGENN, H), (AGENT, H)]),
        ("Fine-tuning (QLoRA, Ollama)", [(FT, H)]),
    ]),
    ("Data & ML", "data", [
        ("Pandas / NumPy", [(INFOR, H)]),
        ("PySpark", [(INFOR, H)]),
        ("Forecasting (XGBoost, Prophet)", [(INFOR, H)]),
        ("Simulation & optimization", [(INFOR, H)]),
        ("MLflow", [(ELGENN, L), (INFOR, H)]),
        ("Kedro", [(ELGENN, L)]),
        ("Orchestration (ION / Airflow)", [(INFOR, H)]),
    ]),
    ("Databases & Storage", "store", [
        ("SQL / PostgreSQL", [(ELGENN, H), (CAHPP, H), (INFOR, H)]),
        ("Elasticsearch", [(ELYADATA, L)]),
        ("pgvector / Milvus", [(ELGENN, H), (CAHPP, L)]),
        ("Neo4j", [(UBI_PLAT, L)]),
        ("S3 / Data Lake", [(UBI_PLAT, L), (INFOR, H)]),
    ]),
    ("Cloud & DevOps", "cloud", [
        ("AWS (Lambda, ECS, EC2)", [(UBI_ALL, H)]),
        ("Docker", [(UBI_PLAT, H), (ALLIANZ, H)]),
        ("Kubernetes / Helm", [(ALLIANZ, H)]),
        ("Jenkins CI/CD", [(ALLIANZ, H)]),
        ("Azure Blob", [(ALLIANZ, L)]),
    ]),
]

THEMES = {
    "light": dict(
        bg="#ffffff", text="#1f2328", muted="#656d76", grid="#d8dee4", row="#f6f8fa",
        card="#f6f8fa", border="#d0d7de",
        backend="#4f46e5", ai="#c026d3", data="#0d9488", store="#16a34a", cloud="#d97706",
        lane_a="#24292f", lane_b="#57606a", lane_text="#ffffff", now="#cf222e",
    ),
    "dark": dict(
        bg="#0d1117", text="#e6edf3", muted="#8b949e", grid="#30363d", row="#161b22",
        card="#161b22", border="#30363d",
        backend="#818cf8", ai="#e879f9", data="#2dd4bf", store="#4ade80", cloud="#fbbf24",
        lane_a="#e6edf3", lane_b="#8b949e", lane_text="#0d1117", now="#ff7b72",
    ),
}

W = 980
LABEL_W = 218
PAD_R = 24
X0, X1 = LABEL_W, W - PAD_R
T0, T1 = 2021.6, 2027.0
ROW_H = 22
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def px(t):
    return X0 + (min(max(t, T0), T1) - T0) / (T1 - T0) * (X1 - X0)


def merge(spans, gap=0.05):
    """Join touching spans of the same level so translucent bars show no seams."""
    merged = []
    for (a, b), lvl in sorted(spans, key=lambda s: (s[1], s[0][0])):
        if merged and merged[-1][1] == lvl and a <= merged[-1][0][1] + gap:
            (pa, pb), _ = merged[-1]
            merged[-1] = ((pa, max(pb, b)), lvl)
        else:
            merged.append(((a, b), lvl))
    return merged


def render(name, c):
    out = []
    add = out.append

    # --- layout -------------------------------------------------------------
    y_axis = 74
    y_lane = 100
    y = y_lane + 74
    body_top = y
    for _, _, skills in GROUPS:
        y += 34 + len(skills) * ROW_H
    body_bottom = y
    legend_y = body_bottom + 18
    height = legend_y + 36

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" font-family="{FONT}" role="img" '
        f'aria-label="Timeline of skill usage from 2021 to {TODAY.year}">')
    add(f'<rect width="{W}" height="{height}" rx="14" fill="{c["bg"]}"/>')
    add(f'<rect x=".5" y=".5" width="{W - 1}" height="{height - 1}" rx="14" fill="none" stroke="{c["border"]}"/>')

    # --- header -------------------------------------------------------------
    add(f'<text x="28" y="40" font-size="20" font-weight="700" fill="{c["text"]}">Skills, as they were used</text>')
    add(f'<text x="28" y="60" font-size="12" fill="{c["muted"]}">'
        f'Each bar is a real engagement, {int(UBI_ALL[0])}–{TODAY.year}. Not self-rated levels.</text>')

    # --- year grid + axis ---------------------------------------------------
    for yr in range(int(T0) + 1, int(T1) + 1):
        if yr > TODAY.year + 0.99:
            continue
        x = px(yr)
        add(f'<line x1="{x:.1f}" y1="{y_axis + 6}" x2="{x:.1f}" y2="{body_bottom}" stroke="{c["grid"]}" stroke-dasharray="2 4"/>')
        add(f'<text x="{x:.1f}" y="{y_axis}" font-size="12" font-weight="600" text-anchor="middle" fill="{c["muted"]}">{yr}</text>')

    # --- role lane ----------------------------------------------------------
    add(f'<text x="28" y="{y_lane + 19}" font-size="11" font-weight="700" letter-spacing="1" fill="{c["muted"]}">WHERE</text>')
    for label, (a, b), kind in ROLES:
        xa, xb = px(a), px(b)
        fill = c["lane_a"] if kind == "a" else c["lane_b"]
        add(f'<rect x="{xa:.1f}" y="{y_lane}" width="{xb - xa:.1f}" height="28" rx="14" fill="{fill}"/>')
        add(f'<text x="{(xa + xb) / 2:.1f}" y="{y_lane + 18.5}" font-size="12" font-weight="600" '
            f'text-anchor="middle" fill="{c["lane_text"]}">{escape(label)}</text>')
    for label, (a, b) in SIDE:
        xa, xb = px(a), px(b)
        add(f'<rect x="{xa:.1f}" y="{y_lane + 34}" width="{xb - xa:.1f}" height="16" rx="8" fill="none" '
            f'stroke="{c["lane_a"]}" stroke-dasharray="3 3"/>')
        add(f'<text x="{xa - 6:.1f}" y="{y_lane + 46}" font-size="10.5" text-anchor="end" fill="{c["muted"]}">{label}</text>')
    # engagement ticks under the Elyadata lane
    for label, (a, b) in ENGAGEMENTS:
        xa, xb = px(a), px(b)
        add(f'<rect x="{xa:.1f}" y="{y_lane + 34}" width="{max(xb - xa, 3):.1f}" height="16" rx="8" fill="{c["lane_b"]}" fill-opacity=".22"/>')
    placed = {}
    for label, (a, b) in ENGAGEMENTS:
        if label in placed:
            continue
        placed[label] = True
        xa, xb = px(a), px(b)
        add(f'<text x="{(xa + xb) / 2:.1f}" y="{y_lane + 62}" font-size="9.5" text-anchor="middle" fill="{c["muted"]}">{label}</text>')

    # --- skill groups -------------------------------------------------------
    y = body_top
    for gname, gkey, skills in GROUPS:
        color = c[gkey]
        add(f'<rect x="20" y="{y + 4}" width="4" height="14" rx="2" fill="{color}"/>')
        add(f'<text x="32" y="{y + 16}" font-size="11" font-weight="700" letter-spacing="1" fill="{color}">{escape(gname.upper())}</text>')
        y += 34
        for i, (skill, spans) in enumerate(skills):
            if i % 2 == 0:
                add(f'<rect x="12" y="{y - 3}" width="{W - 24}" height="{ROW_H}" rx="6" fill="{c["row"]}"/>')
            add(f'<text x="{LABEL_W - 12}" y="{y + 12}" font-size="12" text-anchor="end" fill="{c["text"]}">{escape(skill)}</text>')
            for (a, b), lvl in merge(spans):
                xa, xb = px(a), px(b)
                add(f'<rect x="{xa:.1f}" y="{y + 1}" width="{max(xb - xa, 4):.1f}" height="12" rx="6" '
                    f'fill="{color}" fill-opacity="{lvl}"/>')
            y += ROW_H

    # --- today marker -------------------------------------------------------
    xn = px(NOW)
    add(f'<line x1="{xn:.1f}" y1="{y_lane - 8}" x2="{xn:.1f}" y2="{body_bottom}" stroke="{c["now"]}" stroke-width="1.5"/>')
    add(f'<circle cx="{xn:.1f}" cy="{y_lane - 8}" r="3.5" fill="{c["now"]}"/>')

    # --- legend -------------------------------------------------------------
    add(f'<rect x="32" y="{legend_y}" width="26" height="10" rx="5" fill="{c["backend"]}"/>')
    add(f'<text x="66" y="{legend_y + 9}" font-size="11" fill="{c["muted"]}">core to the work</text>')
    add(f'<rect x="170" y="{legend_y}" width="26" height="10" rx="5" fill="{c["backend"]}" fill-opacity="{L}"/>')
    add(f'<text x="204" y="{legend_y + 9}" font-size="11" fill="{c["muted"]}">supporting / used alongside</text>')
    add(f'<line x1="400" y1="{legend_y - 1}" x2="400" y2="{legend_y + 11}" stroke="{c["now"]}" stroke-width="1.5"/>')
    add(f'<text x="410" y="{legend_y + 9}" font-size="11" fill="{c["muted"]}">today</text>')
    add(f'<text x="{W - 28}" y="{legend_y + 9}" font-size="11" text-anchor="end" fill="{c["muted"]}">'
        f'generated by tools/skill_timeline.py</text>')
    add("</svg>")

    OUT.mkdir(exist_ok=True)
    path = OUT / f"skill-timeline-{name}.svg"
    path.write_text("\n".join(out), encoding="utf-8")
    print("wrote", path)


if __name__ == "__main__":
    for n, c in THEMES.items():
        render(n, c)
