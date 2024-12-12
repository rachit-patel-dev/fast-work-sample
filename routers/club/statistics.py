from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

import internal
import schemas
import utils
from CONSTANTS import DEFAULT_LIMIT, DEFAULT_MAX_LIMIT, STATISTICS_INPUT_DURATION_TYPES
from log import LoggingRoute

# Initialize API Router
router = APIRouter(route_class=LoggingRoute)


@router.get(
    path="/operational",
    response_model=schemas.OperationalStatisticsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_operational_statistics_data(
    club_id: str = Query(example="rjLeihzwivTpZSYQ6QvbQdWYxG13"),
    selected_duration: STATISTICS_INPUT_DURATION_TYPES = Query(example="week"),
    start_time: int = Query(example=1690588800000),
    end_time: int = Query(example=1690675140000),
    user_timezone: str = Query(example="Europe/Stockholm"),
):
    """
    API endpoint to retrieve operational statistics data for a specific time range and club ID.

    Args:
        club_id (str): ID of the club for which statistics are to be retrieved.
        start_time (int): Start timestamp of the time range.
        end_time (int): End timestamp of the time range.

    Returns:
        dict: Operational statistics data for the specified time range and club ID.
    """

    # Call internal function to get operational statistics data
    data = await internal.count_statistics_for_specific_time_range_from_db(
        club_id=club_id,
        start_time=start_time,
        end_time=end_time,
        selected_duration=selected_duration,
        statistics_type="operational",
        user_timezone=user_timezone,
    )

    # Raise exception if no relevant bookings are found
    if data is None:
        utils.raise_exception(
            message="No relevant bookings found.",
            path=f"{utils.pathlib.Path(__file__).absolute()}:{utils.sys._getframe().f_lineno}",
        )

    return data


@router.get(
    path="/financial",
    response_model=schemas.FinancialStatisticsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_financial_statistics_data(
    club_id: str = Query(example="rjLeihzwivTpZSYQ6QvbQdWYxG13"),
    selected_duration: STATISTICS_INPUT_DURATION_TYPES = Query(example="week"),
    start_time: int = Query(example=1690588800000),
    end_time: int = Query(example=1690675140000),
    user_timezone: str = Query(example="Europe/Stockholm"),
):
    """
    API endpoint to retrieve financial statistics data for a specific time range and club ID.

    Args:
        club_id (str): ID of the club for which financial statistics are to be retrieved.
        start_time (int): Start timestamp of the time range.
        end_time (int): End timestamp of the time range.

    Returns:
        dict: Financial statistics data for the specified time range and club ID.
    """

    # Call internal function to get financial statistics data
    data = await internal.count_statistics_for_specific_time_range_from_db(
        club_id=club_id,
        start_time=start_time,
        end_time=end_time,
        selected_duration=selected_duration,
        statistics_type="financial",
        user_timezone=user_timezone,
    )

    # Raise exception if no relevant bookings are found
    if data is None:
        utils.raise_exception(
            message="No relevant bookings found.",
            path=f"{utils.pathlib.Path(__file__).absolute()}:{utils.sys._getframe().f_lineno}",
        )

    return data


@router.get(
    path="/online_payment_history",
    response_model=List[Optional[schemas.OnlinePaymentResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_online_payment_history(
    club_id: str = Query(example="rjLeihzwivTpZSYQ6QvbQdWYxG13"),
    start_datetime: int = Query(example=1706745600000, default=None, ge=0),
    end_datetime: int = Query(example=1707523200000, default=None, ge=0),
    limit: int = Query(
        default=0,
        example=DEFAULT_LIMIT,
        ge=0,
        le=DEFAULT_MAX_LIMIT,
    ),
    skip: int = Query(
        default=0,
        description="Skip the n limit results to get the next n results",
        example=DEFAULT_LIMIT,
        ge=0,
    ),
):
    """
    API endpoint to retrieve get online payment history a specific  club ID.

    Args:
        club_id (str): ID of the club for which financial statistics are to be retrieved.
        start_datetime (int): start datetime filter
        end_datetime (int): end datetime filter
        limit (int): limit for the pagination
        skip (int): skip fot the pagination

    Returns:
        dict: online payment history for the specified club ID.
    """
    return await internal.get_online_payment_list_for_club(
        club_id, start_datetime, end_datetime, limit, skip
    )


@router.get(
    path="/activity_transaction_history",
    response_model=List[Optional[schemas.ActivityTransactionHistory]],
    status_code=status.HTTP_200_OK,
)
async def get_activity_transaction_history(
    club_id: str = Query(example="rjLeihzwivTpZSYQ6QvbQdWYxG13"),
    start_datetime: int = Query(example=1706745600000, default=None, ge=0),
    end_datetime: int = Query(example=1707523200000, default=None, ge=0),
    limit: int = Query(
        default=0,
        example=20,
        ge=0,
        le=1000,
    ),
    skip: int = Query(
        default=0,
        description="Skip the n limit results to get the next n results",
        example=0,
        ge=0,
    ),
    user=Depends(internal.staff_check_for_my_club),
):
    """
    API endpoint to retrieve get online payment history a specific  club ID.

    Args:
        club_id (str): ID of the club for which financial statistics are to be retrieved.
        start_datetime (int): start datetime filter
        end_datetime (int): end datetime filter
        limit (int): limit for the pagination
        skip (int): skip fot the pagination
        user: user authentication for club
    Returns:
        dict: online payment history for the specified club ID.
    """

    return await internal.get_activity_transaction_history(
        club_id, start_datetime, end_datetime, limit, skip
    )
