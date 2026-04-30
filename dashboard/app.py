from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from ems.data_loader import load_profiles
from ems.ems_controller import run_dispatch


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results"


st.set_page_config(
    page_title="Microgrid EMS Dashboard",
    page_icon="EMS",
    layout="wide",
)

st.title("Microgrid Energy Management System")
st.caption("Professional dashboard for load, PV, grid power, and battery state-of-charge analysis.")

with st.sidebar:
    st.header("Simulation Inputs")
    load_scale = st.slider("Load scaling", 0.50, 1.50, 1.00, 0.05)
    solar_irradiance = st.slider("Solar irradiance (W/m2)", 200, 1000, 850, 50)

    st.divider()
    st.subheader("Battery Settings")
    battery_capacity = st.slider("Battery capacity (kWh)", 40.0, 200.0, 120.0, 10.0)
    initial_soc = st.slider("Initial SOC", 0.20, 0.95, 0.50, 0.05)
    max_power = st.slider("Max charge/discharge power (kW)", 10.0, 80.0, 35.0, 5.0)

profiles = load_profiles(DATA_DIR)
profiles["load_kw"] = profiles["load_kw"] * load_scale
profiles["solar_kw"] = profiles["solar_kw"] * (solar_irradiance / 1000)

results = run_dispatch(
    profiles,
    battery_capacity_kwh=battery_capacity,
    initial_soc=initial_soc,
    max_charge_kw=max_power,
    max_discharge_kw=max_power,
)

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
results.to_csv(RESULTS_DIR / "dispatch_results.csv", index=False)

total_cost = results["grid_energy_cost_usd"].sum()
total_import = results["grid_import_kw"].sum()
total_export = results["grid_export_kw"].sum()
renewable_energy = results["solar_kw"].sum()
average_soc = results["battery_soc"].mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Grid Cost", f"${total_cost:,.2f}")
col2.metric("Grid Import", f"{total_import:,.1f} kWh")
col3.metric("Grid Export", f"{total_export:,.1f} kWh")
col4.metric("Average SOC", f"{average_soc:,.1f}%")

st.divider()

plot_col1, plot_col2 = st.columns([1.25, 1])

with plot_col1:
    st.subheader("Load vs PV vs Grid Power")
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.plot(results["hour"], results["load_kw"], label="Load", linewidth=2.2)
    ax.plot(results["hour"], results["solar_kw"], label="PV", linewidth=2.2)
    ax.plot(results["hour"], results["grid_import_kw"], label="Grid Import", linewidth=2.2)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Power (kW)")
    ax.set_title("Microgrid Power Profile")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with plot_col2:
    st.subheader("Battery SOC Over Time")
    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.plot(results["hour"], results["battery_soc"] * 100, color="#16a34a", linewidth=2.4)
    ax.fill_between(results["hour"], results["battery_soc"] * 100, color="#16a34a", alpha=0.12)
    ax.set_xlabel("Hour")
    ax.set_ylabel("SOC (%)")
    ax.set_title("Battery State of Charge")
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with st.expander("Dispatch Results Table"):
    st.dataframe(results, use_container_width=True)

st.caption(f"PV energy generated in this scenario: {renewable_energy:,.1f} kWh")
