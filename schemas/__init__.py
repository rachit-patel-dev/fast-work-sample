from typing import Any, Dict

from fastapi import status
from pydantic import BaseModel

from .activity_join import ActivityParticipants
from .anonymous_user_data import AnonymousUser
from .booking import (
    Activity,
    ActivityHistory,
    BookCourt,
    BookMatch,
    BookTournament,
    BookTraining,
    DescriptionMenu,
    GetBookCourt,
    GetBookedByPlayers,
    GetBookMatch,
    GetBookTournament,
    GetBookTraining,
    GetFrontendDescription,
    GetFrontendDescriptions,
    GetMultipleActivities,
    MatchPlayerInfo,
    NewActivity,
    PlayerInfo,
    PostFrontendDescription,
    Recurrent,
    RequestList,
    ShareActivity,
    ShareTournament,
    TournamentBracket,
    TournamentParticipants,
    UpdateActivityRecord,
    UpdateBookCourt,
    UpdateBookMatch,
    UpdateBookTournament,
    UpdateBookTraining,
    UpdateParticipantFlag,
    UserInfo,
)
from .chatchannel import ChatChannel, ChatChannelMembers
from .club import (
    Club,
    ClubBasic,
    ClubCourtsNumber,
    ClubLocation,
    ClubPermissions,
    ClubSignup,
    ClubSportsAvailable,
    ClubSummaryFields,
    FavouriteCenter,
    FinancialStatisticsResponse,
    GetClubInfo,
    OnlinePaymentResponse,
    OperationalStatisticsResponse,
    UpdateClubInfo,
)
from .club_credits import (
    ClubCredits,
    CreateClubCredits,
    GetClubCredits,
    UpdateClubCredits,
)
from .coach import Coach, GetCoach, UpdateCoach
from .court import (
    Court,
    GetCourt,
    GetCourtForAvailableSlots,
    GetSingleCourt,
    UpdateCourt,
)
from .credit_package import (
    CreateCreditPackage,
    CreditPackage,
    GetCreditPackage,
    UpdateCreditPackage,
)
from .database_schema.club_activity_joins import (
    InsertActivityJoins,
    UpdateActivityJoins,
    UpdateActivityJoinsPaymentInfo,
)
from .database_schema.event_logs import INSERTEventLog
from .discount_code import (
    CheckDiscountCode,
    DiscountCode,
    GetDiscountCode,
    UpdateDiscountCode,
)
from .event_logs import (
    ClubEventLogsSchema,
    ClubEventLogsSchemaResponse,
    UpdateDetail,
    UserDetails,
)
from .follower import (
    CreateFollower,
    EmailClubFollowers,
    GetFollowers,
    InsertFollowerDoc,
    Notification,
)
from .guest_user import GuestUserInfo, GuestUserSearch
from .invite import InviteIn
from .league import (
    AddDeleteTeamDivision,
    BaseCrudLeague,
    BookedCourtsTimes,
    CreateDraftLeague,
    CreateLeague,
    CreateLeagueDivision,
    CreateSeason,
    Division,
    DivisionPointTable,
    DivisionTeam,
    DraftDivision,
    DraftLeague,
    DraftLeagueSeason,
    GetDivision,
    GetLeague,
    GetLeagueList,
    GetTeamList,
    League,
    LeagueSeason,
    NewSeason,
    RoundScheduleTeam,
    RoundScheduleTeamPlayer,
    SeriesMatch,
    UpdateDivision,
    UpdateLeague,
    UpdateLeagueAndDivision,
    UpdateLeagueSeason,
    UpdateTeamPaidStatusInDivision,
)
from .location import GETNonRegClubLocations
from .login import LoginCred
from .member import (
    CreateMember,
    GetFollowersAndMembers,
    GetFollowersAndMembersInfo,
    GetMembershipMembers,
    InsertFollowerAndMember,
    UpdateMember,
)
from .membership import (
    CreateMembership,
    GetAllPlayerMemberships,
    GetMembership,
    GetMembershipInfo,
    GetMemberships,
    GetPlayerMemberships,
    InsertMembership,
    InsertPrivateMembership,
    InsertPublicMembership,
    PlayerMembershipDiscount,
    UpdateMembership,
)
from .notificationchannels import NotificationChannel, NotificationChannelSeriesGame
from .player import (
    AddCreditsPostRequest,
    GetPlayerReward,
    GetPlayersReward,
    PlayerCredit,
    SearchedPlayer,
)
from .player_booking import (
    AllActivityPlayerResponse,
    AllCourtsSlotPricesResponse,
    AvailableSlots,
    AvailableSlotsResponses,
    ClubFilters,
    FilteredClubResponses,
    PlayerBookCourt,
    PlayerBookCourtResponses,
    SearchedClubResponse,
    SearchedClubResponses,
    SearchedNearbyClubResponses,
    SlotAvailable,
)
from .player_club_info import (
    Follower,
    FollowingClubCoinInfo,
    PlayerClubInfo,
    PlayerFollowingClubList,
    UpdatePlayerClubStatus,
)
from .player_membership import (
    AddPlayerToMembership,
    GetPlayerMembershipInfo,
    MembershipInvite,
    PlayerMembershipInfo,
    UpdatePlayerMembershipInfo,
)
from .player_user import GetUserActivityHistory, PlayerUserSignup
from .price import (
    GetMultiplePriceFrontend,
    GetPrice,
    MultiplePriceFrontend,
    Price,
    Prices,
    UpdatePrice,
)
from .price_list import GetPriceList, PriceList, UpdatePriceList
from .response_schema.activity_transaction_history import ActivityTransactionHistory
from .response_schema.club_clubs import GETClubResponse
from .response_schema.event_logs import GETEventLogResponse
from .reward import (
    GetReward,
    GetRewardHistories,
    GetRewardHistory,
    GetRewards,
    Reward,
    RewardPurchaseHistoryList,
    UpdateReward,
)
from .series_games_match import GetRescheduleoptions, POSTReScheduleMatch
from .slot import GetSlot, Slot, SlotInterval, UpdateSlot
from .staff import (
    CreateStaff,
    GetAllStaff,
    GetStaff,
    GetStaffNames,
    Permissions,
    Staff,
    StaffSignup,
    UpdateStaff,
)
from .team import PostAddPlayerInTeam
from .translation import TranslationDict


class CUDResponse(BaseModel):
    """Genearal CUD Response Model"""

    status_code: int
    success: bool
    message: str
    detail: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": status.HTTP_200_OK,
                "success": True,
                "message": "Task performed successfully",
                "detail": {"string": "any"},
            }
        }


class POSTResponse(BaseModel):
    """Global POST Response Model"""

    status_code: int
    success: bool
    message: str
    user: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": status.HTTP_201_CREATED,
                "success": True,
                "message": "Task performed successfully",
                "user": {"_id": "60e6b5b9b9b9b9b9b9b9b9b9"},
            }
        }
