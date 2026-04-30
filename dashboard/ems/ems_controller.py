import pandas as pd

from .battery import Battery


def run_dispatch(
    profiles: pd.DataFrame,
    battery_capacity_kwh: float = 120.0,
    initial_soc: float = 0.50,
    min_soc: float = 0.20,
    max_soc: float = 0.95,
    max_charge_kw: float = 35.0,
    max_discharge_kw: float = 35.0,
    round_trip_efficiency: float = 0.92,
) -> pd.DataFrame:
    battery = Battery(
        capacity_kwh=battery_capacity_kwh,
        initial_soc=initial_soc,
        min_soc=min_soc,
        max_soc=max_soc,
        max_charge_kw=max_charge_kw,
        max_discharge_kw=max_discharge_kw,
        round_trip_efficiency=round_trip_efficiency,
    )

    records = []
    for row in profiles.itertuples(index=False):
        net_power_kw = row.solar_kw - row.load_kw
        battery_charge_kw = 0.0
        battery_discharge_kw = 0.0
        grid_import_kw = 0.0
        grid_export_kw = 0.0

        if net_power_kw > 0:
            battery_charge_kw = battery.charge(net_power_kw)
            grid_export_kw = max(net_power_kw - battery_charge_kw, 0.0)
        else:
            battery_discharge_kw = battery.discharge(abs(net_power_kw))
            grid_import_kw = max(abs(net_power_kw) - battery_discharge_kw, 0.0)

        records.append(
            {
                **row._asdict(),
                "battery_charge_kw": battery_charge_kw,
                "battery_discharge_kw": battery_discharge_kw,
                "grid_import_kw": grid_import_kw,
                "grid_export_kw": grid_export_kw,
                "battery_soc": battery.soc,
            }
        )

    results = pd.DataFrame(records)
    results["grid_energy_cost_usd"] = results["grid_import_kw"] * results["tariff_usd_per_kwh"]
    return results
