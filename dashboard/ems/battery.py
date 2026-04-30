from dataclasses import dataclass

import numpy as np


@dataclass
class Battery:
    capacity_kwh: float
    initial_soc: float
    min_soc: float
    max_soc: float
    max_charge_kw: float
    max_discharge_kw: float
    round_trip_efficiency: float

    def __post_init__(self) -> None:
        self.soc = self.initial_soc
        self.charge_efficiency = np.sqrt(self.round_trip_efficiency)
        self.discharge_efficiency = np.sqrt(self.round_trip_efficiency)

    @property
    def energy_kwh(self) -> float:
        return self.soc * self.capacity_kwh

    def charge(self, available_power_kw: float, duration_h: float = 1.0) -> float:
        power_kw = min(max(available_power_kw, 0.0), self.max_charge_kw)
        free_capacity_kwh = (self.max_soc * self.capacity_kwh) - self.energy_kwh
        accepted_energy_kwh = min(power_kw * duration_h * self.charge_efficiency, free_capacity_kwh)
        self.soc += accepted_energy_kwh / self.capacity_kwh
        return accepted_energy_kwh / duration_h

    def discharge(self, required_power_kw: float, duration_h: float = 1.0) -> float:
        power_kw = min(max(required_power_kw, 0.0), self.max_discharge_kw)
        usable_energy_kwh = self.energy_kwh - (self.min_soc * self.capacity_kwh)
        delivered_energy_kwh = min(power_kw * duration_h, usable_energy_kwh * self.discharge_efficiency)
        self.soc -= (delivered_energy_kwh / self.discharge_efficiency) / self.capacity_kwh
        return delivered_energy_kwh / duration_h
