"""Download the UCI Online Retail workbook into data/raw/."""
from pathlib import Path
import zipfile
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
ZIP_PATH = RAW_DIR / "online-retail.zip"
URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if not any(RAW_DIR.glob("*.xlsx")):
        print(f"Downloading dataset from {URL}")
        response = requests.get(URL, timeout=120)
        response.raise_for_status()
        ZIP_PATH.write_bytes(response.content)
        with zipfile.ZipFile(ZIP_PATH) as archive:
            archive.extractall(RAW_DIR)
        print("Download and extraction complete.")
    else:
        print("Excel workbook already exists; skipping download.")

    workbooks = list(RAW_DIR.glob("*.xlsx"))
    if not workbooks:
        raise FileNotFoundError("No .xlsx workbook found after extraction.")
    print(f"Workbook ready: {workbooks[0]}")


if __name__ == "__main__":
    main()
