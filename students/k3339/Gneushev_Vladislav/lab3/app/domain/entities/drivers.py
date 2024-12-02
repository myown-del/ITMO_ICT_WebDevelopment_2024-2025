from dataclasses import dataclass
from datetime import time

from app.domain.entities.base import Entity


@dataclass
class DriverClass(Entity):
    id: int | None
    name: str


@dataclass
class DriverSalary(Entity):
    id: int | None
    work_experience_over_months: int
    driver_class: DriverClass
    salary_rub: int


@dataclass
class Driver(Entity):
    id: int | None
    first_name: str
    last_name: str
    passport_info: str
    driver_class: DriverClass
    work_experience_months: int
    salary: DriverSalary | None = None


@dataclass
class DayWorkingHours:
    start_time: time
    end_time: time


@dataclass
class DriverWorkSchedule(Entity):
    driver: Driver
    monday: DayWorkingHours | None
    tuesday: DayWorkingHours | None
    wednesday: DayWorkingHours | None
    thursday: DayWorkingHours | None
    friday: DayWorkingHours | None
    saturday: DayWorkingHours | None
    sunday: DayWorkingHours | None
