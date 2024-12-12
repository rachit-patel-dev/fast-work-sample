from .activity import activity, book_court, description, match, tournament, training
from .admin import log
from .authentication import forgot, login, logout, permission, signup, token
from .club import (
    account,
    coach,
    court,
    credit,
    credit_package,
    discount_code,
    event_logs,
    follower,
    info,
    member,
    membership,
    notification,
    payment,
    price,
    price_list,
    reward,
    slot,
    statistics,
    verify,
)
from .club_non_reg import location
from .guest import guest_user
from .player import (
    player,
    player_activity,
    player_booking,
    player_club_info,
    player_membership,
)
from .series_games import division, league, season, series_games_match, team
from .staff import staff
from .support import chat_channels
