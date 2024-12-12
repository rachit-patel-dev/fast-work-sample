import pathlib
import sys

from .currency import CURRENCY
from .translation import translator
from .util import (
    UTC_to_milliseconds,
    UTC_to_ms,
    calculate_total_hours_difference,
    chop_overlapping_intervals,
    convert_timezone_datetime_to_utc_datetime,
    convert_utc_ms_to_timezone_datetime,
    convert_utc_ms_to_timezone_ms,
    create_expiration_date_for_training_tournament,
    current_utc_timestamp_in_milliseconds,
    distance_between_two_coordinates,
    find_overlapping_intervals,
    find_weekday_time_occurrences,
    generate_time_slots_fixture_for_provided_time_with_hours_and_minutes,
    get_club_id_from_club_staff_user,
    get_current_datetime_in_utc,
    get_dict_of_datetime_with_30_miutes_slots_between_provided_epoch,
    get_overlap_mins,
    get_user_id_for_player,
    is_current_time_within_a_slot_interval,
    make_rule,
    milliseconds_to_UTC,
    ms_to_day_of_the_week,
    ms_to_UTC,
    raise_exception,
    raise_non_http_exception,
    slot_interval_to_ms,
    user_auth,
)
