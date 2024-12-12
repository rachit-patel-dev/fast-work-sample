import datetime
from typing import Any, Dict, List, Union

import pytz
from bson import ObjectId

import database
import utils
from CONSTANTS import STATISTICS_INPUT_DURATION_TYPES, CollInfo, DBInfo
from database import (
    get_club_full_info_from_db,
    get_courts_for_club_id_db,
    mongodb_client,
)


async def count_statistics_for_specific_time_range_from_db(
    club_id: str,
    start_time: int,
    end_time: int,
    selected_duration: STATISTICS_INPUT_DURATION_TYPES,
    statistics_type: str,
    user_timezone: str,
):
    """
    Count statistics for a specific time range from the database.

    Args:
        club_id (str): The ID of the club for which statistics are calculated.
        start_time (int): The start timestamp of the time range.
        end_time (int): The end timestamp of the time range.
        selected_duration (STATISTICS_INPUT_DURATION_TYPES): The duration type for which statistics are calculated.
        statistics_type (str): The type of statistics to be calculated.

    Returns:
        dict or None: Calculated statistics for the specified time range, or None if an error occurs.
    """

    try:
        # Retrieve club information and timezone
        club_info = await get_club_full_info_from_db(club_id)
        club_timezone = pytz.timezone(club_info["timezone"])

        user_timezone_obj = pytz.timezone(user_timezone)

        # Create a fixed time for comparison
        fixed_time = datetime.datetime(2023, 1, 1, 12, 0, 0)

        # Convert the fixed time to both time zones
        user_timezone_fixed_time = user_timezone_obj.localize(fixed_time)
        club_timezone_fixed_time = club_timezone.localize(fixed_time)

        # Calculate the time difference in minutes
        time_difference_seconds = int(
            (club_timezone_fixed_time - user_timezone_fixed_time).total_seconds()
        )

        start_time = start_time + (time_difference_seconds * 1000)
        end_time = (end_time - 1000) + (time_difference_seconds * 1000)

        # Calculate time duration and the start time of the previous period
        time_duration = end_time - start_time
        previous_period_start_time = start_time - time_duration

        # Retrieve activity records from the database for the specified time range
        records = list(
            mongodb_client[DBInfo.database][CollInfo.activity_records].find(
                {
                    "club_id": club_id,
                    "start_datetime": {"$gte": previous_period_start_time},
                    "end_datetime": {"$lte": end_time + 1000},
                }
            )
        )

        # Convert timestamps to user's timezone and add formatted datetime fields to records
        for record in records:
            utc_start_datetime = datetime.datetime.utcfromtimestamp(
                record["start_datetime"] / 1000
            )
            utc_end_datetime = datetime.datetime.utcfromtimestamp(
                record.get("end_datetime") / 1000
            )
            user_timezone_start_datetime = utc_start_datetime.replace(
                tzinfo=pytz.utc
            ).astimezone(club_timezone)
            user_timezone_end_datetime = utc_end_datetime.replace(
                tzinfo=pytz.utc
            ).astimezone(club_timezone)
            record["formatted_start_datetime"] = user_timezone_start_datetime
            record["formatted_end_datetime"] = user_timezone_end_datetime

        # Separate records for the previous period and the current period
        previous_period_records = list(
            filter(lambda record: record["start_datetime"] < start_time, records)
        )

        # Initialize variables for calculating previous period total prices
        previous_period_total_price = 0
        previous_period_bookings_total_price = 0
        previous_period_matches_total_price = 0
        previous_period_trainings_total_price = 0
        previous_period_tournaments_total_price = 0

        # Calculate previous period total prices if there are previous period records
        if len(previous_period_records):
            previous_activity_type_records = await get_filtered_activity_type_records(
                previous_period_records
            )
            (
                previous_period_total_price,
                previous_period_bookings_total_price,
                previous_period_matches_total_price,
                previous_period_trainings_total_price,
                previous_period_tournaments_total_price,
            ) = await get_previous_period_activities_details(
                previous_activity_type_records, club_timezone=club_timezone
            )

        # Separate records for the current period
        current_period_records = list(
            filter(lambda record: record["start_datetime"] >= start_time, records)
        )

        # Continue processing for the current period if there are current period records
        if len(current_period_records):
            # Retrieve and organize activity type records for the current period
            activity_type_records = await get_filtered_activity_type_records(
                current_period_records
            )

            # Retrieve detailed information for each type of activity
            bookings_records = activity_type_records.get("Book Court")
            bookings = await get_bookings(
                booking_records=bookings_records, club_timezone=club_timezone
            )

            match_records = activity_type_records.get("Match")

            full_matches_records = await get_full_matches_records(
                activity_type_records.get("Match")
            )

            (
                training_records,
                trainings,
                full_trainings_records,
                full_trainings,
            ) = await get_full_trainings_records(
                full_trainings_records=activity_type_records.get("Training"),
                club_timezone=club_timezone,
            )

            (
                tournaments_records,
                tournaments,
                full_tournaments_records,
                full_tournaments,
            ) = await get_full_tournaments_records(
                full_tournaments_records=activity_type_records.get("Tournament"),
                club_timezone=club_timezone,
            )

            # Generate time slots for the entire day
            time_slots_fixture = await utils.generate_time_slots_fixture_for_provided_time_with_hours_and_minutes(
                "00:00", "23:31"
            )

            # Retrieve club courts and their IDs
            club_courts = await get_courts_for_club_id_db(club_id)
            club_courts_ids = [str(court["_id"]) for court in club_courts]

            # Calculate and return operational statistics if the type is "operational"
            if statistics_type == "operational":
                # Calculate bookings count and the hottest time slots for the current period
                bookings_count, hottest_time_slots_fixture = await get_counts_per_day(
                    time_slots_fixture=time_slots_fixture,
                    data_list=current_period_records,
                    start_time=start_time,
                    end_time=end_time,
                    is_bookings=True,
                )

                # Calculate full matches count and the hottest time slots for the current period
                (
                    full_matches_count,
                    hottest_time_slots_fixture,
                ) = await get_counts_per_day(
                    time_slots_fixture=time_slots_fixture,
                    data_list=full_matches_records,
                    start_time=start_time,
                    end_time=end_time,
                )

                # Calculate full trainings count and the hottest time slots for the current period
                (
                    full_trainings_count,
                    hottest_time_slots_fixture,
                ) = await get_counts_per_day(
                    time_slots_fixture=time_slots_fixture,
                    data_list=full_trainings_records,
                    start_time=start_time,
                    end_time=end_time,
                    is_trainings=True,
                )

                # Calculate full tournaments count and the hottest time slots for the current period
                (
                    full_tournaments_count,
                    hottest_time_slots_fixture,
                ) = await get_counts_per_day(
                    time_slots_fixture=time_slots_fixture,
                    data_list=full_tournaments_records,
                    start_time=start_time,
                    end_time=end_time,
                    is_tounaments=True,
                )

                # Organize the calculated counts into a dictionary
                data = {
                    "bookings_count": bookings_count,
                    "full_matches_count": full_matches_count,
                    "full_trainings_count": full_trainings_count,
                    "full_tournaments_count": full_tournaments_count,
                }

                # Format the data for the selected duration and obtain additional information
                formatted_data = await format_data_for_selected_duration(
                    club_id=club_id,
                    club_courts_ids=club_courts_ids,
                    club_timezone=club_timezone,
                    start_time=start_time,
                    end_time=end_time,
                    selected_duration=selected_duration,
                    data=data,
                    hottest_time_slots=hottest_time_slots_fixture,
                )

                # Return the formatted data for operational statistics
                return formatted_data
            else:
                # Calculate and return operational statistics if the type is "financial"

                # Retrieve full match records and calculate counts and total price
                matches = await get_full_matches(
                    full_match_records=match_records, club_timezone=club_timezone
                )
                (
                    full_matches_count,
                    full_matches_total_price,
                ) = await get_bookings_and_matches_total_price(data_list=matches)

                # Retrieve and calculate counts and total price for full trainings
                (
                    full_trainings_count,
                    full_trainings_total_price,
                ) = await get_trainings_and_tournaments_total_price(data_list=trainings)

                # Retrieve and calculate counts and total price for full tournaments
                (
                    full_tournaments_count,
                    full_tournaments_total_price,
                ) = await get_trainings_and_tournaments_total_price(
                    data_list=tournaments
                )

                # Retrieve and calculate counts and total price for bookings
                (
                    bookings_count,
                    bookings_total_price,
                ) = await get_bookings_and_matches_total_price(data_list=bookings)

                # Calculate the total price for all activities
                total_price = round(
                    bookings_total_price
                    + full_matches_total_price
                    + full_trainings_total_price
                    + full_tournaments_total_price,
                    1,
                )

                # Calculate percentage changes for total prices and individual activities
                total_price_percentage = await calculate_percentage_change(
                    previous_period_total_price, total_price
                )

                bookings_total_price_percentage = await calculate_percentage_change(
                    previous_period_bookings_total_price, bookings_total_price
                )

                full_matches_total_price_percentage = await calculate_percentage_change(
                    previous_period_matches_total_price, full_matches_total_price
                )

                full_trainings_total_price_percentage = (
                    await calculate_percentage_change(
                        previous_period_trainings_total_price,
                        full_trainings_total_price,
                    )
                )

                full_tournaments_total_price_percentage = (
                    await calculate_percentage_change(
                        previous_period_tournaments_total_price,
                        full_tournaments_total_price,
                    )
                )

                # Organize counts into a dictionary for further processing
                data = {
                    "bookings_count": bookings_count,
                    "full_matches_count": full_matches_count,
                    "full_trainings_count": full_trainings_count,
                    "full_tournaments_count": full_tournaments_count,
                }

                # Format data for the selected duration and obtain additional information
                formatted_data = await format_data_for_selected_duration(
                    club_id=club_id,
                    club_courts_ids=club_courts_ids,
                    club_timezone=club_timezone,
                    start_time=start_time,
                    end_time=end_time,
                    total_price=total_price,
                    selected_duration=selected_duration,
                    data=data,
                )

                # Return a dictionary containing various statistics for non-operational type
                return {
                    "total_price": total_price,
                    "bookings_total_price": bookings_total_price,
                    "full_matches_total_price": full_matches_total_price,
                    "full_trainings_total_price": full_trainings_total_price,
                    "full_tournaments_total_price": full_tournaments_total_price,
                    "total_price_percentage": (
                        f"{total_price_percentage}%"
                        if total_price_percentage
                        else "N/A"
                    ),
                    "bookings_total_price_percentage": (
                        f"{bookings_total_price_percentage}%"
                        if bookings_total_price_percentage
                        else "N/A"
                    ),
                    "full_matches_total_price_percentage": (
                        f"{full_matches_total_price_percentage}%"
                        if full_matches_total_price_percentage
                        else "N/A"
                    ),
                    "full_trainings_total_price_percentage": (
                        f"{full_trainings_total_price_percentage}%"
                        if full_trainings_total_price_percentage
                        else "N/A"
                    ),
                    "full_tournaments_total_price_percentage": (
                        f"{full_tournaments_total_price_percentage}%"
                        if full_tournaments_total_price_percentage
                        else "N/A"
                    ),
                    "bookings_count": formatted_data.get("bookings_count", {}),
                    "full_matches_count": formatted_data.get("full_matches_count", {}),
                    "full_trainings_count": formatted_data.get(
                        "full_trainings_count", {}
                    ),
                    "full_tournaments_count": formatted_data.get(
                        "full_tournaments_count", {}
                    ),
                }
        return None
    except Exception as e:
        utils.raise_exception(e=e)
