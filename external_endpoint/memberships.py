import json
from typing import Dict, Union

import requests

from CONSTANTS import ACTIVE_NESTJS_ENDPOINT


async def club_create_stripe_product_for_membership_with_auth(
    jwt: str, club_info: Dict[str, str], membership_info: Dict[str, Union[str, int]]
):
    """Create a stripe product for a membership by club | WRAP IN TRY/EXCEPT

    Args:
        jwt (str) : JWT of club.
        club_info (dict) : Club information, including name and currency.
        membership_info (dict) : Membership information, including name, price and period.

    Returns:
        stripe_product_id (str) : ID of stripe product.
        stripe_price_id (str) : ID of stripe price.
    """

    # Headers for stripe API with JWT
    header = {
        "Authorization": jwt,
        "Content-Type": "application/json",
    }

    data = {
        "clubName": club_info["name"],
        "packageName": membership_info["name"],
        "amount": membership_info["price"] * 100,  # Convert to cents for stripe
        "currency": club_info["currency"].lower(),  # Convert to lowercase for stripe
        "interval": "month"
        if membership_info["period"] == "Monthly"
        else "year",  # Convert to stripe format month/year
    }

    response = requests.post(
        url=f"{ACTIVE_NESTJS_ENDPOINT}/subscription/clubMembershipPackages",
        headers=header,
        data=json.dumps(data),
    )
    assert response.status_code == 201, response.text
    response_dict = response.json()
    assert response_dict["success"] is True, response.text

    return response_dict["productId"], response_dict["priceId"]


async def player_cancel_stripe_subscription_for_membership_with_auth(
    jwt: str, stripe_price_id: str, player_mongo_id: str, club_id: str
):
    """Cancel a stripe subscription for a membership by player | WRAP IN TRY/EXCEPT

    Args:
        jwt (str) : JWT of the user.
        stripe_price_id (str) : ID of stripe price.
        player_id (str) : ID of player.
        club_id (str) : ID of club.

    Returns:
        response_dict (dict) : Response from stripe API.
    """

    # Headers for stripe API with JWT
    header = {
        "Authorization": jwt.replace("Bearer", "PadelMates", 1),
        "Content-Type": "application/json",
    }

    data = {
        "planId": stripe_price_id,
        "userId": player_mongo_id,
        "clubId": club_id,
    }

    response = requests.delete(
        url=f"{ACTIVE_NESTJS_ENDPOINT}/subscription/cancelClubMembershipSubscription",
        headers=header,
        data=json.dumps(data),
    )
    assert response.status_code == 200, response.text
    response_dict = response.json()
    assert response_dict["success"] is True, response.text

    return response_dict


async def club_cancel_stripe_subscription_for_membership_with_auth(
    jwt: str, stripe_price_id: str, player_mongo_id: str, club_id: str
):
    """Cancel a stripe subscription for a membership by club | WRAP IN TRY/EXCEPT

    Args:
        jwt (str) : JWT of the user.
        stripe_price_id (str) : ID of stripe price.
        player_id (str) : ID of player.
        club_id (str) : ID of club.

    Returns:
        response_dict (dict) : Response from stripe API.
    """

    # Headers for stripe API with JWT
    header = {
        "Authorization": jwt,
        "Content-Type": "application/json",
    }

    data = {
        "planId": stripe_price_id,
        "userId": player_mongo_id,
        "clubId": club_id,
    }

    response = requests.delete(
        url=f"{ACTIVE_NESTJS_ENDPOINT}/subscription/cancelClubMembershipSubscription/club",
        headers=header,
        data=json.dumps(data),
    )

    assert response.status_code == 200, response.text
    response_dict = response.json()
    assert response_dict.get("success", False) is True, response.text

    return response_dict
