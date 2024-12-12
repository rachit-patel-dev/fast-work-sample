import json
from typing import List

import requests

from CONSTANTS import ACTIVE_NESTJS_ENDPOINT


async def club_refund_activity_with_auth(
    jwt: str,
    activity_record_id: str,
    activity_type: str,
    player_ids: List[str],
    reason: str,
):
    """Club Refund a player for an activity with auth | WRAP IN TRY/EXCEPT

    Args:
        jwt: str
        activity_record_id: str
        activity_type: str
        player_ids: List[str]
        reason: str

    Returns:
        "refundResponse": [
            {
                "message": "Amount refunded successfully for the player with id: 63ed9f7fd6c3dbd1ba886acf",
                "playerId": "63ed9f7fd6c3dbd1ba886acf",
                "refundStatus": "REFUND_SUCCESS",
                "transactionId": "6480c9460eab3370587d4c0e"
            },
            {
                "message": "Amount refunded successfully for the player with id: 6396ec5c5661e4309299ce73",
                "playerId": "6396ec5c5661e4309299ce73",
                "refundStatus": "REFUND_SUCCESS",
                "transactionId": "6480c90402be2158d7c2f1b5"
            }
        ]

    """

    # Headers for stripe API with JWT
    header = {
        "Authorization": jwt,  # .replace("Bearer", "PadelMates", 1),
        "Content-Type": "application/json",
    }

    data = {
        "requestedFor": activity_type.lower(),
        "idOfRequestedFor": activity_record_id,  # activity_record_id for match/tournament/training/booking and memebership id for membership
        "reason": reason,
        "playerIds": player_ids,  # mongo ids of players
    }

    response = requests.post(
        url=f"{ACTIVE_NESTJS_ENDPOINT}/club/refund",
        headers=header,
        data=json.dumps(data),
    )

    assert response.status_code == 201, response.text
    response_dict = response.json()
    assert response_dict["success"] is True, response.text

    return response_dict


def club_auto_refund_activity_without_auth(
    club_id: str,
    activity_record_id: str,
    activity_type: str,
    player_ids: List[str],
    reason: str,
):
    """Club Refund a player for an auto cancelled activity without auth | WRAP IN TRY/EXCEPT

    Args:
        club_id: str
        activity_record_id: str
        activity_type: str
        player_ids: List[str]
        reason: str

    Returns:
        "refundResponse": [
            {
                "message": "Amount refunded successfully for the player with id: 63ed9f7fd6c3dbd1ba886acf",
                "playerId": "63ed9f7fd6c3dbd1ba886acf",
                "refundStatus": "REFUND_SUCCESS",
                "transactionId": "6480c9460eab3370587d4c0e"
            },
            {
                "message": "Player with id: 648b8ed3168ae8d434574a22 may not have any payment for this tournament",
                "playerId": "648b8ed3168ae8d434574a22",
                "refundStatus": "REFUND_SUCCESS",
                "transactionId": "6480c9460eab3370587d4c0e"
            }
        ]
    """

    # Headers for stripe API with JWT
    header = {"Content-Type": "application/json"}
    data = {
        "clubId": club_id,
        "requestedFor": activity_type.lower(),
        "idOfRequestedFor": activity_record_id,
        "reason": reason,
        "playerIds": player_ids,
    }

    response = requests.post(
        url=f"{ACTIVE_NESTJS_ENDPOINT}/club/refundWithoutAuthToken",
        headers=header,
        data=json.dumps(data),
    )

    assert response.status_code == 201, response.text
    response_dict = response.json()
    assert response_dict["success"] is True, response.text

    return response_dict


def club_auto_refund_activity_with_transaction_ids_without_auth(
    transaction_ids: List[str],
):
    """Club Refund a player for an auto cancelled activity without auth | WRAP IN TRY/EXCEPT

    Args:
        transaction_ids: List[str]

    Returns:
        "refundResponse": [
            {
                "message": "Amount refunded successfully for the player with id: 63ed9f7fd6c3dbd1ba886acf",
                "playerId": "63ed9f7fd6c3dbd1ba886acf",
                "refundStatus": "REFUND_SUCCESS",
                "transactionId": "6480c9460eab3370587d4c0e"
            },
            {
                "message": "Player with id: 648b8ed3168ae8d434574a22 may not have any payment for this tournament",
                "playerId": "648b8ed3168ae8d434574a22",
                "refundStatus": "REFUND_SUCCESS",
                "transactionId": "6480c9460eab3370587d4c0e"
            }
        ]
    """

    # Headers for stripe API with JWT
    header = {"Content-Type": "application/json"}
    data = {
        "transactionIds": transaction_ids,
    }

    response = requests.post(
        url=f"{ACTIVE_NESTJS_ENDPOINT}/club/refundWithTransactionId",
        headers=header,
        data=json.dumps(data),
    )

    assert response.status_code == 201, response.text
    response_dict = response.json()
    assert response_dict["success"] is True, response.text

    return response_dict


async def player_refund_for_cancelling_activity_with_auth(
    jwt: str, activity_type: str, activity_records_id: str
):
    """Refund a player instantly for cancelling an activity with auth | WRAP IN TRY/EXCEPT

    Args:
        jwt (str) : JWT of player.
        activity_records_id (str) : Activity record ID.

    Returns:
        response_dict (dict) : Response dictionary.
    """

    header = {
        "Authorization": jwt.replace("Bearer", "PadelMates", 1),
        "Content-Type": "application/json",
    }
    data = {
        "requestedFor": activity_type.lower(),
        "idOfRequestedFor": activity_records_id,
        "reason": "Player cancelled the booking",
    }

    response = requests.post(
        url=f"{ACTIVE_NESTJS_ENDPOINT}/payment/refund",
        headers=header,
        data=json.dumps(data),
    )

    assert response.status_code == 201, response.text
    response_dict = response.json()
    assert response_dict["success"] is True, response.text

    return response_dict
