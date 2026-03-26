import os
from collections import defaultdict
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

views = [
    "View_AA_AvecFacture",
    "View_AA_Detail",
    "View_AA_SansFacture",
    "View_AA_Total",
    "View_FF_Detail",
    "View_FF_Entete",
    "View_FF_Total",
    "View_FREIGHT",
]

# Heuristics: group by normalized suffix after last underscore.
def normalize(col):
    return col.replace(" ", "").upper()

with engine.connect() as conn:
    cols_by_view = {}
    for view in views:
        cols = conn.execute(
            text(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=:view"
            ),
            {"view": view},
        ).scalars().all()
        cols_by_view[view] = cols

    # Build index by suffix and by token parts
    suffix_index = defaultdict(list)
    token_index = defaultdict(list)

    for view, cols in cols_by_view.items():
        for col in cols:
            n = normalize(col)
            suffix = n.split("_")[-1]
            suffix_index[suffix].append((view, col))
            for token in n.split("_"):
                token_index[token].append((view, col))

    # Suggest relations based on shared suffixes (e.g. NUMFACT, REFERENCE, DOSSIER, HOUSE, DATEPROCESS)
    interesting = {"NUMFACT", "REFERENCE", "DOSSIER", "HOUSE", "DATEPROCESS", "ETA", "ID", "NUM", "MASTERBL"}
    suggestions = []
    for key in interesting:
        candidates = suffix_index.get(key, [])
        if len(candidates) > 1:
            suggestions.append((key, candidates))

    print("Relations suggérées (par suffixe commun):")
    if not suggestions:
        print("Aucune relation suggérée.")
    else:
        for key, items in suggestions:
            print(f"\n- Suffixe: {key}")
            for view, col in items:
                print(f"  {view}.{col}")

    # Also show top tokens used across views
    print("\nTokens communs fréquents:")
    common_tokens = sorted(
        ((token, items) for token, items in token_index.items() if len(items) > 3),
        key=lambda x: (-len(x[1]), x[0])
    )
    for token, items in common_tokens[:20]:
        views_set = sorted({v for v, _ in items})
        print(f"{token}: {len(items)} colonnes, vues: {', '.join(views_set)}")
