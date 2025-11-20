from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()

data_raw = Path(ROOT_DIR / "data" / "raw" / "teste.csv")
data_processed = Path(ROOT_DIR / "data" / "processed" / "hospitais_pb.csv")


print (ROOT_DIR)