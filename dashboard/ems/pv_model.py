import pandas as pd


def apply_pv_scale(profiles: pd.DataFrame, pv_scale: float) -> pd.DataFrame:
    scaled = profiles.copy()
    scaled["solar_kw"] = scaled["solar_kw"] * pv_scale
    return scaled
