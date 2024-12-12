from typing import List, Optional

import utils
from CONSTANTS import LOGGED_IN_USER_TYPE, USER_TYPE

from .bookings import get_booking_details_db
from .clubs import get_club_id_name_photo_db, get_clubs_names_db, get_user_club_info_db
from .matches import get_match_details_db
from .staffs import (
    get_staff_id_name_photo_db,
    get_staff_names_db,
    get_user_staff_info_db,
)
from .tournaments import get_tournament_details_db
from .trainings import get_training_details_db
from .users import (
    get_player_user_id_name_photo_db,
    get_player_user_info_db,
    get_player_users_mongo_id_name_photo,
    get_user_player_info_db,
)


async def get_users_id_name_photo(user_id: str):
    """Get user's id, name and photo_url.

    Args:
        id (str): User ID.

    Returns:
        Dict[str, str]: Dictionary of _id, name and photo_url.
        None: If user is not found.
    """

    user_info = await get_club_id_name_photo_db(user_id)
    if user_info:
        return user_info

    user_info = await get_staff_id_name_photo_db(user_id)
    if user_info:
        return user_info

    user_info = await get_player_user_info_db(user_id)
    if user_info:
        return user_info

    return {
        "_id": user_id,
        "name": "USER_DOES_NOT_EXIST",
        "photo_url": None,
        "email": None,
        "phone_number": None,
    }


async def get_user_types_id_name_photo(user_id: str, user_type: USER_TYPE):
    """Get user's id, name and photo_url with user_type.

    Args:
        user_id (str): User ID.
        user_type (Literal["clubs", "staffs", "players"]): User type.

    Returns:
        Dict[str, str]: Dictionary of _id, name and photo_url.
    """

    if user_type == "clubs":
        user_info = await get_club_id_name_photo_db(user_id)
        if user_info:
            return user_info

    elif user_type == "staffs":
        user_info = await get_staff_id_name_photo_db(user_id)
        if user_info:
            return user_info

    elif user_type == "players":
        user_info = await get_player_user_id_name_photo_db(user_id)
        if user_info:
            return user_info

    return {"_id": user_id, "name": "USER_DOES_NOT_EXIST", "photo_url": None}


async def get_basic_user_info(user_id: str, user_type: Optional[USER_TYPE]):
    """Get basic user information.

    Args:
        user_id (str): User ID.
        user_type (USER_TYPE): User type.

    Returns:
        Dict[str, str]: Dictionary of _id, name and photo_url.
    """

    if user_type:
        return await get_user_types_id_name_photo(user_id, user_type)

    return await get_users_id_name_photo(user_id)


async def generate_title_with_activity_and_users_name(activity: str, user_id: str):
    """Generate title with activity and user's name.

    Args:
        activity (str): Activity.
        users (List[Dict[str, str]]): List of users.

    Returns:
        str: Title.
    """

    user_info = await get_users_id_name_photo(user_id)

    try:
        assert user_info is not None, "User not found"
        return f"{activity} by {user_info.get('name')}"

    except Exception as e:
        utils.raise_exception(e=e)


async def get_activity_info_db(activity_id, activity_type):
    """Get activity info from database.

    Args:
        activity_id (str): Activity ID.
        activity_type (str): Activity type.

    Returns:
        Dict[str, Any]: Activity info.
    """

    if activity_type == "Book Court":
        return await get_booking_details_db(activity_id)
    elif activity_type == "Match":
        return await get_match_details_db(activity_id)
    elif activity_type == "Tournament":
        return await get_tournament_details_db(activity_id)
    elif activity_type == "Training":
        return await get_training_details_db(activity_id)

    return None


async def get_users_id_names(user_ids: List[str]):
    """Get user's id and name.

    Args:
        id List[str]: User ID.

    Returns:
        Dict[str, str]: Dictionary of _id, name.
        []: If user is not found.
    """

    try:
        user_info = await get_clubs_names_db(user_ids)
        if len(user_info):
            return user_info

        user_info = await get_staff_names_db(user_ids)
        if len(user_info):
            return user_info

        user_info = await get_player_users_mongo_id_name_photo(user_ids)
        if len(user_info):
            return user_info

        return []
    except Exception as e:
        utils.raise_exception(e=e)


async def get_user_info_for_event_db(user_id: str, user_type: LOGGED_IN_USER_TYPE):
    """Get user related ino for event

    Args:
        user_id (str): User ID.
        user_type (LOGGED_IN_USER_TYPE): User type.

    Returns:
        Dict[str, str]: Dictionary of user_mongo_id, user_firebase_id, user_email, user_name, user_photo.
    """

    if user_type == "CLUB":
        user_info = await get_user_club_info_db(club_id=user_id)

    elif user_type == "STAFF":
        user_info = await get_user_staff_info_db(staff_id=user_id)

    elif user_type == "PLAYER":
        user_info = await get_user_player_info_db(player_id=user_id)

    return user_info or {
        "user_mongo_id": None,
        "user_firebase_id": user_id,
        "user_email": None,
        "user_name": user_id,
        "user_photo": None,
        "user_phone": None,
    }
