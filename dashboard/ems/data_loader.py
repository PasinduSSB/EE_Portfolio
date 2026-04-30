from pathlib import Path

import pandas as pd


def load_profiles(data_dir: Path) -> pd.DataFrame:
    load = pd.read_csv(data_dir / "load_profile.csv")
    solar = pd.read_csv(data_dir / "solar_profile.csv")
    tariff = pd.read_csv(data_dir / "tariff_profile.csv")

    profiles = load.merge(solar, on="hour").merge(tariff, on="hour")
    return profiles.sort_values("hour").reset_index(drop=True)
