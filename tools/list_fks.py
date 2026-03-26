import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

sql = text(
    "SELECT fk.name AS fk_name, tp.name AS parent_table, cp.name AS parent_column, "
    "tr.name AS referenced_table, cr.name AS referenced_column "
    "FROM sys.foreign_keys fk "
    "JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id "
    "JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id "
    "JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id "
    "JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id "
    "JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id "
    "ORDER BY parent_table, fk.name"
)

with engine.connect() as conn:
    rows = conn.execute(sql).all()
    if not rows:
        print("Aucune FK trouvée")
    else:
        for r in rows:
            print(f"{r.parent_table}.{r.parent_column} -> {r.referenced_table}.{r.referenced_column} ({r.fk_name})")
