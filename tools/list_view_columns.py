import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

views = ["View_FF_Entete", "View_FF_Total"]

with engine.connect() as conn:
    for view in views:
        rows = conn.execute(text(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME=:view ORDER BY ORDINAL_POSITION"
        ), {"view": view}).scalars().all()
        print(f"{view}: {', '.join(rows)}")
