import random
from datetime import datetime

import requests
from bson.objectid import ObjectId

import utils
from CONSTANTS import COLLECTION_ACTIVITY_TYPE, CollInfo, DBInfo
from database import mongodb_client


async def qt_system_check(club_id: str):
    """Checks if qt_system exists for this club. If so returns qt_info.
    Args:
        club_id (str) : ID of club.

    Returns:
        Dict[str, str]: qt_info.
    """
    try:
        qt_info = mongodb_client[DBInfo.database][CollInfo.clubs].find_one(
            {"_id": club_id},
            {"_id": 0, "qt_system": 1},
        )

        if qt_info is not None:  # type: ignore
            qt_info = qt_info.get("qt_system")  # type: ignore
            return qt_info
        else:
            return None

    except Exception as e:
        utils.raise_exception(e=e)


async def generate_access_code():
    return str(random.randint(1000, 9999)) + "#"


def qt_post_request_helper(
    url,
    headers,
    payload,
    activity_record_id,
    access_code_required,
    access_code,
    session=None,
):
    # response = requests.post(url, headers=headers, json=payload)
    if access_code_required:
        updated_doc = mongodb_client[DBInfo.database][
            CollInfo.activity_records
        ].find_one_and_update(
            {"_id": ObjectId(activity_record_id)},
            {"$set": {"code": access_code}},
            session=session,
        )
        mongodb_client[DBInfo.database][
            COLLECTION_ACTIVITY_TYPE[updated_doc["activity_type"]]  # type: ignore
        ].update_one(
            {"_id": ObjectId(updated_doc["activity_id"])},  # type: ignore
            {
                "$set": {"qt_requests": 1},
                "$push": {
                    "qt_tasks": {
                        "action": "CREATE",
                        "url": url,
                        "headers": headers,
                        "payload": payload,
                    }
                },
            },
            session=session,
        )
    elif access_code_required is False:
        updated_doc = mongodb_client[DBInfo.database][
            CollInfo.activity_records
        ].find_one_and_update(
            {"_id": ObjectId(activity_record_id)},
            {"$set": {"code": ""}},
            return_document=True,
            session=session,
        )

        mongodb_client[DBInfo.database][
            COLLECTION_ACTIVITY_TYPE[updated_doc["activity_type"]]
        ].update_one(
            {"_id": ObjectId(updated_doc["activity_id"])},
            {
                "$set": {"qt_requests": 1},
                "$push": {
                    "qt_tasks": {
                        "action": "CREATE",
                        "url": url,
                        "headers": headers,
                        "payload": payload,
                    }
                },
            },
            session=session,
        )
    # elif response.status_code == 200 and access_code_required:
    #     updated_doc = mongodb_client[DBInfo.database][CollInfo.activity_records].find_one_and_update(
    #         {"_id": ObjectId(activity_record_id)},
    #         {"$set":{"qt_requests": 0}},
    #         return_document=True
    #     )

    #     mongodb_client[DBInfo.database][COLLECTION_ACTIVITY_TYPE[updated_doc["activity_type"]]].update_one(
    #         {"_id": ObjectId(updated_doc["activity_id"])},
    #         {"$set":{"qt_requests": 0}},
    #     )
    # TODO Send notification


async def qt_instant_post(
    url,
    headers,
    payload,
    activity_record_id,
    access_code_required,
    access_code,
    session=None,
):
    return requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20,
    )


async def qt_post_request(
    qt_info,
    activity_record_id,
    court_ids,
    start_seconds,
    end_seconds,
    instant=False,
    session=None,
):
    """Book a court in qt.
    Args:
        qt_info from club_clubs.
        activity_record_id: str

    Returns:
        HTTP status code.
    """
    headers = {
        "Authorization": f"Bearer {qt_info['jwtToken']}",
        "Content-Type": "application/json",
    }
    start = (
        "T".join(str(datetime.utcfromtimestamp(start_seconds)).split(" ")) + "+00:00"
    )
    end = "T".join(str(datetime.utcfromtimestamp(end_seconds)).split(" ")) + "+00:00"
    access_code_required = False
    for court_id in court_ids:
        if court_id in qt_info["objects"].keys():
            if "door" in qt_info["objects"][court_id]["object_names"]:
                access_code_required = True
    for court_id in court_ids:
        if court_id in qt_info["objects"].keys():
            object_id = qt_info["objects"][court_id]["object_id"]
        else:
            continue

        url = f"https://api.qt-systems.se/v1/objects/{object_id}/bookings"
        external_id = (
            str(activity_record_id) + "-" + str(object_id) + "-" + str(court_id)[-3:]
        )
        payload = {
            "time": {
                "from": start,
                "to": end,
            },
            "external": {"id": external_id},
            "transform": {},
            "execution": {"transport": {"mode": "direct"}},
        }

        for obj in qt_info["objects"][court_id]["object_names"]:
            if obj == "facility":
                payload["transform"] = {"output": {"included": 0}}
                continue
            if obj == "door" or access_code_required:
                payload["user"] = {"access_code": qt_info["access_code"][:-1]}
            payload["transform"][obj] = {  # type: ignore
                "time_offset": {
                    "from": qt_info["offset"][obj]["from"],
                    "to": qt_info["offset"][obj]["to"],
                }
            }
        cron_status = 400
        if instant:
            response = await qt_instant_post(
                url,
                headers,
                payload,
                str(activity_record_id),
                access_code_required,
                qt_info["access_code"],
                session=session,
            )
            cron_status = response.status_code
        if cron_status != 200:
            qt_post_request_helper(
                url,
                headers,
                payload,
                str(activity_record_id),
                access_code_required,
                qt_info["access_code"],
                session=session,
            )


async def qt_delete_request(
    qt_info, booking_id, court_ids, activity_id, activity_type, update=False
):
    # try:
    headers = {
        "Authorization": f"Bearer {qt_info['jwtToken']}",
        "Content-Type": "application/json",
    }

    # response = requests.delete(url, headers=headers, timeout=20)
    # if response.status_code != 200:
    # updated_doc = mongodb_client[DBInfo.database][CollInfo.activity_records].find_one(
    #             {"_id": ObjectId(booking_id)},
    #             {"activity_id": 1, "activity_type": 1},
    #         )
    for court_id in court_ids:
        if court_id not in qt_info["objects"].keys():
            continue
        idx = qt_info["objects"][court_id]["object_id"]
        external_id = f"{str(booking_id)}-{str(idx)}-{str(court_id)[-3:]}"
        url = f"https://api.qt-systems.se/v1/bookings/x{external_id}"
        mongodb_client[DBInfo.database][
            COLLECTION_ACTIVITY_TYPE[activity_type]
        ].update_one(
            {"_id": ObjectId(activity_id)},
            {
                "$set": {"qt_requests": 1},
                "$push": {
                    "qt_tasks": {
                        "action": "DELETE",
                        "url": url,
                        "headers": headers,
                        "booking_id": external_id,
                    }
                },
            },
        )


# except Exception as e:
#     utils.raise_exception(e=e)


# @dataclass
# class QtUrls:
#     delete: str = "https://api.qt-systems.se/v1/bookings/x" # {booking_id}
#     post: str = "https://api.qt-systems.se/v1/objects/" # {object}/bookings
#     objects: str = "https://api.qt-systems.se/v1/objects"
