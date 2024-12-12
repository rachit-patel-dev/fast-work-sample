from dataclasses import dataclass
from typing import Dict, Union

from typing_extensions import Literal

from configs import config_loader

ACTIVE_NESTJS_ENDPOINT = config_loader.endpoint_config.get("nestjs_endpoint")


@dataclass
class DBInfo:
    database: str = str(config_loader.mongo_db_config["database_name"])


@dataclass
class CollInfo:
    activity_joins: str = "club_activity_joins"
    activity_records: str = "club_activity_records"
    bookings: str = "club_bookings"
    chatchannels: str = "chatchannels"
    chatChannelMembers: str = "chatChannelMembers"
    clubs: str = "club_clubs"
    coaches: str = "club_coaches"
    courts: str = "club_courts"
    descriptions: str = "club_descriptions"
    discounts: str = "club_discounts"
    event_logs: str = "event_logs"
    favoritecenters: str = "favoritecenters"
    feedbacks: str = "feedbacks"
    followers: str = "club_followers"
    gameinterests: str = "gameinterests"
    guest_users: str = "club_guest_users"
    invites: str = "club_invites"
    locations: str = "locations"
    matches: str = "club_matches"
    membershipinfos: str = "club_membershipinfos"
    memberships: str = "club_memberships"
    notificationchannels: str = "notificationchannels"
    notification_settings: str = "notificationsettings"
    players: str = "club_players"
    prices: str = "club_prices"
    price_lists: str = "club_price_lists"
    rewards: str = "club_rewards"
    reward_histories: str = "club_reward_histories"
    slots: str = "club_slots"
    staffs: str = "club_staffs"
    subscriptions: str = "subscriptions"
    tournaments: str = "club_tournaments"
    tournament_matchmakings: str = "club_tournament_matchmakings"
    trainings: str = "club_trainings"
    transactions: str = "transactions"
    users: str = "users"
    league: str = "series_league"
    season: str = "series_season"
    division: str = "series_division"
    team: str = "series_team"
    match: str = "series_match"
    credits: str = "club_credits"
    club_credit_packages: str = "club_credit_packages"
    anonymous_user_data: str = "anonymous_user_data"


# firebaseUID of support@padelmates.se
SUPPORT_ACCOUNT_FB_ID = "gekABhDLi9YwbIG1Z28CVe3o9GA2"

SESSION_KEY = "session"

# ------------------------------------- ACTIVITY related Constants declared here ------------------------------------- #
ACTIVITY_INTERVAL = Literal["PAST", "PRESENT", "FUTURE"]
MATCH_TYPE = Literal["Single", "Double"]
TRAINING_TYPE = Literal["Group", "Personal"]
DIVISION_TYPE = Literal["Straight", "Tree-Style"]
SEASON_STATUS = Literal["Upcoming", "Playing", "Finished"]
PLAYER_ACTIVITY_TYPE = Literal["Match", "Tournament", "Training"]
SLOT_ORIGIN = Literal["Discount Code", "Price Slot", "Membership"]
GAME_TYPE = Literal["training", "tournament", "match", "series_match"]
ACTIVITY_TYPE = Literal["Book Court", "Match", "Tournament", "Training"]
EVENT_LOG_SOURCE_TYPE = Literal[
    "Book Court", "Match", "Tournament", "Training", "Credit"
]
DISCOUNT_ACTIVITY_TYPE = Literal["booking", "matches", "tournaments", "training"]
SPORTS_AVAILABLE = Literal["padel", "tennis", "badminton", "squash", "pickleball"]
TOURNAMENT_TYPE = Literal["Americano", "Team Americano", "Mexicano", "Team Mexicano"]
EVENT_LOG_TYPE = Literal[
    "PLAYER_ADD",
    "PLAYER_JOIN",
    "PLAYER_LEAVE",
    "GUEST_ADD",
    "ACTIVITY_CREATE",
    "ACTIVITY_EDIT",
    "ACTIVITY_REMOVE",
    "PLAYER_BOOKING",
    "CREDIT_ADDED",
    "CREDIT_UPDATED",
    "CREDIT_DELETED",
]
EVENT_LOG_SUP_TYPE = Literal["ACTIVITY", "PLAYER"]
EVENT_LOG_SUP_TYPE_TO_FIELD = {
    "ACTIVITY": "activity_record_id",
    "PLAYER": "user_mongo_id",
}
EVENT_LOG_SEARCH_KEYS = Literal[
    "",
    "source_id",
    "user_mongo_id",
    "user_firebase_id",
    "user_email",
    "user_phone",
    "user_name",
    "impacted_users_detail.user_mongo_id",
    "impacted_users_detail.user_firebase_id",
    "impacted_users_detail.user_email",
    "impacted_users_detail.user_phone",
    "impacted_users_detail.user_name",
]

COURT_TYPES = Literal[
    "indoor_courts", "outdoor_courts", "single_courts", "double_courts"
]
ACTIVITY_RECORD_ACTIVITY_TYPE = {
    "Book Court": "booking",
    "Match": "match",
    "Tournament": "tournament",
    "Training": "training",
}
COLLECTION_ACTIVITY_TYPE = {
    "Book Court": CollInfo.bookings,
    "Match": CollInfo.matches,
    "Tournament": CollInfo.tournaments,
    "Training": CollInfo.trainings,
}
CATEGORY = Literal[
    "player booking",
    "booking",
    "not available",
    "subscription",
    "competition",
    "other activity",
    "facility",
    "series game ordinary",
    "series game extra",
]


# ------------------------------------- USER related Constants declared here ------------------------------------- #
LEAGUE_USER_TYPE = Literal["CLUB", "PLAYER"]
LOGGED_IN_USER_TYPE = Literal["CLUB", "PLAYER", "STAFF"]
USER_TYPE = Literal["clubs", "players", "staffs"]
EVENT_LOG_USER_TYPE = Literal["CLUB", "STAFF", "PLAYER", "GUEST"]
PROFILE_TYPE = Literal["club", "coach", "player", "staff"]
PREFERRED_PLAYTIME = Literal["morning", "lunchtime", "afternoon", "evening"]
RADIUS_IN_KM = Literal[
    "1", "2", "5", "10", "15", "20", "25", "30", "40", "50", "100", "200"
]
STAFF_PERMISSIONS = Literal[
    "booking", "statistics", "ai_analytics", "my_club", "community", "chat"
]
PERMISSION_USER_TYPE: Dict[str, USER_TYPE] = {
    "CLUB": "clubs",
    "PLAYER": "players",
    "STAFF": "staffs",
}
COLLECTION_USER_TYPE = {
    "clubs": CollInfo.clubs,
    "players": CollInfo.users,
    "staffs": CollInfo.staffs,
}
CHAT_TYPE = Literal["private", "single", "group"]


# ------------------------------------- PAYMENT related Constants declared here ------------------------------------- #
PAYMENT_SERVICE = Literal[
    "CREDIT", "CASH", "LINK", "KNET", "CARD", "APPLE PAY", "GOOGLE PAY"
]
PERIODS = Literal["Monthly", "Yearly"]
PAYMENT_TYPE = Literal["PAY DIRECT", "PAY LATER"]
MEMBERSHIP_TYPES = Literal["Public", "Private"]
PAYMENT_METHOD = Literal["PAY_DIRECT", "PAY_LATER"]
PAYMENT_STATUS = Literal[
    "PENDING",
    "PAYMENT_PROCESSING",
    "PAYMENT_HOLD",
    "PAYMENT_SUCCESS",
    "PAYMENT_FAILED",
]
REFUND_STATUS = Literal[
    "REFUND_REQUESTED", "REFUND_PROCESSING", "REFUND_SUCCESS", "REFUND_FAILED"
]
SUBSCRIPTION_STATUS = Literal[
    "SUBSCRIPTION_PENDING",
    "SUBSCRIPTION_SUCCESS",
    "SUBSCRIPTION_FAILED",
    "SUBSCRIPTION_CANCELED",
]
PAYMENT_AND_REFUND_STATUS = Union[PAYMENT_STATUS, REFUND_STATUS]
PAYMENT_AND_REFUND_AND_SUBSCRIPTION_STATUS = Union[
    PAYMENT_STATUS, REFUND_STATUS, SUBSCRIPTION_STATUS
]

# ------------------------------------- TIME DURATION related Constants declared here ------------------------------------- #
INTERVAL = Literal[1, 2, 3, 4]
MINIMUM_AVAILABLE_INTERVAL_IN_MILLISECONDS = 0
WEEKDAYS_IN_SHORT = ["SA", "SU", "MO", "TU", "WE", "TH", "FR"]
WEEKDAY = Literal["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
STATISTICS_INPUT_DURATION_TYPES = Literal["day", "week", "month", "year"]
MONTHS = Literal[
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
]


# ------------------------------------- NOTIFICATION related Constants declared here ------------------------------------- #
MAX_NOTIFICATIONS_MONTH = {
    "Training": 2,
    "Match": 4,
}
NOTIFICATION_TYPE = Literal[
    "chat", "community", "user", "Game", "booking", "tournament", "club"
]
NOTIFICATION_ROUTE = Literal[
    "chat", "booking", "match", "tournament", "profile", "group", "community"
]
NOTIFICATION_MATCH_TYPE = Literal[
    "americano", "team_americano", "mexicano", "training", "booking", "Single", "Double"
]
NOTIFICATION_PAYLOAD_MATCH_TYPE = {
    "Americano": "americano",
    "Team Americano": "team_americano",
    "Mexicano": "mexicano",
    "Training": "training",
}
NOTIFICATION_PAYLOAD_ACTIVITY_TYPE = {
    "Tournament": "tournament",
    "Training": "tournament",
    "Match": "Game",
    "Book Court": "booking",
}
SECTION = Literal[
    "activities",
    "booking",
    "match",
    "training",
    "tournament",
    "profile",
    "membership",
    "community",
    "rewards",
]


# ------------------------------------- PAGINATION related Constants declared here ------------------------------------- #
DEFAULT_LIMIT = 20
DEFAULT_MAX_LIMIT = 100
DEFAULT_SKIP = 0


# ------------------------------------- STATUS related Constants declared here ------------------------------------- #
DISCOUNT_STATUS = {"Active": True, "Inactive": False}
CREDIT_HISTORY_STATUS = Literal["PURCHASED", "SPENT"]
ACTIVE_INACTIVE_STATUS = Literal["Active", "Inactive"]
JOIN_REQUEST_STATUS = Literal["PENDING", "ACCEPTED", "REJECTED"]


# ------------------------------------- TRANSLATION related Constants declared here ------------------------------------- #
TRANSLATION_TYPE = Literal[
    "ACTIVITY_TYPE",
    "JOIN_REQUEST",
    "REMOVE_PLAYER_FROM_ACTIVITY",
    "PLAYER_REFUNDED_SUCCESSFULLY",
    "SPOT_AVAILABLE",
    "UPDATE_JOIN_REQUEST",
    "ACTIVITY_FULL",
    "INVITE_PLAYER",
    "ADD_PLAYER_BOOK_COURT",
    "CANCELED_MEMBERSHIP",
]


# ------------------------------------- CURRENCY related Constants declared here ------------------------------------- #
CANCELLATION_FEE = {
    "AED": 10,
    "BDT": 100,
    "EUR": 1,
    "GBP": 1,
    "KWD": 0,
    "NOK": 12.50,
    "SEK": 12.5,
    "SGD": 1.8,
    "THB": 70,
    "USD": 1,
}
SPLIT_PAYMENT_FEE = {
    "AED": 2,
    "BDT": 1,
    "EUR": 0.3,
    "GBP": 0.3,
    "KWD": 0,
    "NOK": 3,
    "SEK": 3,
    "SGD": 0.4,
    "THB": 0,
    "USD": 0.3,
}

# ------------------------------------- CLUB CREDITS related Constants declared here ------------------------------------- #

CLUB_CREDITS_TYPE = Literal["PURCHASED", "CLUB_CREDITS"]
