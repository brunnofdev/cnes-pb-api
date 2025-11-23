from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()

data_raw = Path(ROOT_DIR / "data" / "raw" / "cnes_estabelecimentos.csv")
data_processed = Path(ROOT_DIR / "data" / "processed" / "hospitais_pb.csv")


sql_rawTable = Path(ROOT_DIR / "sql" / "create_rawTable.sql")
sql_tables = Path(ROOT_DIR / "sql" / "create_tables.sql")
sql_normalize = Path(ROOT_DIR / "sql" / "normalize.sql")
