"""Charge les CSV DVF bruts dans DuckDB (table raw_dvf)."""

from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "dvf.duckdb"
RAW_GLOB = (ROOT / "data" / "raw" / "974_*.csv.gz").as_posix()

if __name__ == "__main__":
    con = duckdb.connect(str(DB_PATH))
    con.sql(f"""
        CREATE OR REPLACE TABLE raw_dvf AS
        SELECT * FROM read_csv_auto('{RAW_GLOB}', union_by_name = true)
    """)
    nb = con.sql("SELECT COUNT(*) FROM raw_dvf").fetchone()[0]
    print(f"raw_dvf : {nb} lignes chargées")
    con.close()