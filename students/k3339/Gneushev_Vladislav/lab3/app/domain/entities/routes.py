from dataclasses import dataclass
from datetime import time

from app.domain.entities.base import Entity


@dataclass
class Route(Entity):
    id: int | None
    name: str
    start_point_name: str
    end_point_name: str
    start_time: time
    end_time: time
    interval_seconds: int
    duration_seconds: int
