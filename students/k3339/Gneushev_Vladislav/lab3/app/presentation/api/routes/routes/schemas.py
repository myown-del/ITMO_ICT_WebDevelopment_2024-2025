from datetime import time

from pydantic import BaseModel


class GetRouteSchema(BaseModel):
    id: int
    name: str
    start_point_name: str
    end_point_name: str
    start_time: time
    end_time: time
    interval_seconds: int
    duration_seconds: int


class AddRouteSchema(BaseModel):
    name: str
    start_point_name: str
    end_point_name: str
    start_time: time
    end_time: time
    interval_seconds: int
    duration_seconds: int
