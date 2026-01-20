import json
import pandas as pd


def load_yield_data(path):
    """
    Load CSV with columns: maturity, yield (in decimal or pct/100).
    """
    df = pd.read_csv(path)
    if df["yield"].max() > 1.0:
        df["yield"] = df["yield"] / 100.0
    return df


def save_summary_json(summary_dict, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary_dict, f, indent=2)
