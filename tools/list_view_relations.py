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

with engine.connect() as conn:
    cols_by_view = {}
    for view in views:
        rows = conn.execute(
            text(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=:view"
            ),
            {"view": view},
        ).scalars().all()
        cols_by_view[view] = set(rows)

    view_pairs = []
    for i, v1 in enumerate(views):
        for v2 in views[i + 1 :]:
            common = sorted(cols_by_view[v1] & cols_by_view[v2])
            if common:
                view_pairs.append((v1, v2, common))

    if not view_pairs:
        print("Aucune colonne commune trouvée entre les vues.")
    else:
        for v1, v2, common in view_pairs:
            print(f"{v1} <-> {v2}")
            print("  Colonnes communes:")
            for col in common:
                print(f"    - {col}")
            print("")
