import datetime
from datetime import timezone as tz
from typing import Dict, List, Optional, Union

import pytz
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    PositiveInt,
    SecretStr,
    root_validator,
    validator,
)

import utils

from .staff import Permissions


class OperationalStatisticsResponse(BaseModel):
    bookings_count: List[Dict[str, Union[str, float]]]
    full_matches_count: List[Dict[str, Union[str, int]]]
    full_trainings_count: List[Dict[str, Union[str, int]]]
    full_tournaments_count: List[Dict[str, Union[str, int]]]
    hottest_time_slots: List[Dict[str, Union[str, int]]]

    class Config:
        schema_extra = {
            "bookings_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 0},
                {"x": "Sunday", "y": 0},
            ],
            "full_matches_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 4},
                {"x": "Sunday", "y": 0},
            ],
            "full_trainings_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 0},
                {"x": "Sunday", "y": 0},
            ],
            "full_tournaments_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 1},
                {"x": "Sunday", "y": 0},
            ],
            "hottest_time_slots": [
                {"x": "00:00", "y": 0},
                {"x": "00:30", "y": 0},
                {"x": "01:00", "y": 0},
                {"x": "01:30", "y": 0},
                {"x": "02:00", "y": 0},
                {"x": "02:30", "y": 0},
                {"x": "03:00", "y": 0},
                {"x": "03:30", "y": 0},
                {"x": "04:00", "y": 0},
                {"x": "04:30", "y": 0},
                {"x": "05:00", "y": 0},
                {"x": "05:30", "y": 0},
                {"x": "06:00", "y": 0},
                {"x": "06:30", "y": 0},
                {"x": "07:00", "y": 0},
                {"x": "07:30", "y": 0},
                {"x": "08:00", "y": 0},
                {"x": "08:30", "y": 0},
                {"x": "09:00", "y": 0},
                {"x": "09:30", "y": 0},
                {"x": "10:00", "y": 0},
                {"x": "10:30", "y": 0},
                {"x": "11:00", "y": 0},
                {"x": "11:30", "y": 1},
                {"x": "12:00", "y": 2},
                {"x": "12:30", "y": 2},
                {"x": "13:00", "y": 1},
                {"x": "13:30", "y": 0},
                {"x": "14:00", "y": 1},
                {"x": "14:30", "y": 0},
                {"x": "15:00", "y": 0},
                {"x": "15:30", "y": 0},
                {"x": "16:00", "y": 0},
                {"x": "16:30", "y": 0},
                {"x": "17:00", "y": 0},
                {"x": "17:30", "y": 0},
                {"x": "18:00", "y": 0},
                {"x": "18:30", "y": 0},
                {"x": "19:00", "y": 0},
                {"x": "19:30", "y": 0},
                {"x": "20:00", "y": 0},
                {"x": "20:30", "y": 0},
                {"x": "21:00", "y": 0},
                {"x": "21:30", "y": 0},
                {"x": "22:00", "y": 0},
                {"x": "22:30", "y": 0},
                {"x": "23:00", "y": 0},
            ],
        }


class FinancialStatisticsResponse(BaseModel):
    total_price: float
    bookings_total_price: float
    full_matches_total_price: float
    full_trainings_total_price: float
    full_tournaments_total_price: float
    total_price_percentage: str
    bookings_total_price_percentage: str
    full_matches_total_price_percentage: str
    full_trainings_total_price_percentage: str
    full_tournaments_total_price_percentage: str
    bookings_count: List[Dict[str, Union[str, float]]]
    full_matches_count: List[Dict[str, Union[str, float]]]
    full_trainings_count: List[Dict[str, Union[str, float]]]
    full_tournaments_count: List[Dict[str, Union[str, float]]]

    class Config:
        schema_extra = {
            "total_price": 600.0,
            "bookings_total_price": 0.0,
            "full_matches_total_price": 400,
            "full_trainings_total_price": 0,
            "full_tournaments_total_price": 200,
            "total_price_percentage": "1566.67%",
            "bookings_total_price_percentage": "0%",
            "full_matches_total_price_percentage": "40000.0%",
            "full_trainings_total_price_percentage": "0%",
            "full_tournaments_total_price_percentage": "455.56%",
            "bookings_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 0},
                {"x": "Sunday", "y": 0},
            ],
            "full_matches_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 4},
                {"x": "Sunday", "y": 0},
            ],
            "full_trainings_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 0},
                {"x": "Sunday", "y": 0},
            ],
            "full_tournaments_count": [
                {"x": "Monday", "y": 0},
                {"x": "Tuesday", "y": 0},
                {"x": "Wednesday", "y": 0},
                {"x": "Thursday", "y": 0},
                {"x": "Friday", "y": 0},
                {"x": "Saturday", "y": 1},
                {"x": "Sunday", "y": 0},
            ],
            "hottest_time_slots": [
                {"x": "00:00", "y": 0},
                {"x": "00:30", "y": 0},
                {"x": "01:00", "y": 0},
                {"x": "01:30", "y": 0},
                {"x": "02:00", "y": 0},
                {"x": "02:30", "y": 0},
                {"x": "03:00", "y": 0},
                {"x": "03:30", "y": 0},
                {"x": "04:00", "y": 0},
                {"x": "04:30", "y": 0},
                {"x": "05:00", "y": 0},
                {"x": "05:30", "y": 0},
                {"x": "06:00", "y": 0},
                {"x": "06:30", "y": 0},
                {"x": "07:00", "y": 0},
                {"x": "07:30", "y": 0},
                {"x": "08:00", "y": 0},
                {"x": "08:30", "y": 0},
                {"x": "09:00", "y": 0},
                {"x": "09:30", "y": 0},
                {"x": "10:00", "y": 0},
                {"x": "10:30", "y": 0},
                {"x": "11:00", "y": 0},
                {"x": "11:30", "y": 1},
                {"x": "12:00", "y": 2},
                {"x": "12:30", "y": 2},
                {"x": "13:00", "y": 1},
                {"x": "13:30", "y": 0},
                {"x": "14:00", "y": 1},
                {"x": "14:30", "y": 0},
                {"x": "15:00", "y": 0},
                {"x": "15:30", "y": 0},
                {"x": "16:00", "y": 0},
                {"x": "16:30", "y": 0},
                {"x": "17:00", "y": 0},
                {"x": "17:30", "y": 0},
                {"x": "18:00", "y": 0},
                {"x": "18:30", "y": 0},
                {"x": "19:00", "y": 0},
                {"x": "19:30", "y": 0},
                {"x": "20:00", "y": 0},
                {"x": "20:30", "y": 0},
                {"x": "21:00", "y": 0},
                {"x": "21:30", "y": 0},
                {"x": "22:00", "y": 0},
                {"x": "22:30", "y": 0},
                {"x": "23:00", "y": 0},
            ],
        }
