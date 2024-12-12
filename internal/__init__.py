from bson import ObjectId
from pydantic.json import ENCODERS_BY_TYPE

from .activity.activity import (
    check_cancelation_time,
    create_activity,
    create_activity_helper,
    create_expiration_date,
    generate_time_list,
    get_activity_records_from_court_id_db,
    get_multiple_activitiesdb,
    get_one_activitydb,
    overlap_check,
    remove_one_activitydb,
    remove_player_db,
    remove_recurring_activitydb,
    share_activity_db,
    update_activity_record_db,
    update_participant_internal,
)
from .activity.booking import (
    add_player_to_activity_db,
    add_player_to_tournament_db,
    add_players_to_book_court_db,
    create_booking_db,
    create_booking_for_league,
    create_description_db,
    delete_booking_by_player,
    expire_at_check,
    get_all_activity_records_for_division,
    get_all_available_courts_db,
    get_all_description_db,
    get_booking_info_db,
    get_calender_notification_info_db,
    get_court_info,
    get_court_info_map_list,
    get_description_db,
    get_player_info,
    get_player_list_db,
    get_requests_list_db,
    get_tournament_notification_info_db,
    get_wait_list_db,
    invite_player_to_tournament,
    lock_slot_db,
    overlap_in_time_db,
    remove_bookings_activity_for_series_division,
    remove_bookings_for_series_division,
    remove_current_activity_overlap,
    send_notification_calender_db,
    send_notification_tournament_db,
    share_tournament_db,
    update_booking_db,
    update_join_request_db,
)
from .activity.matchmaking import (
    create_new_round_db,
    get_player_list_tournament_db,
    get_tournament_brackets_db,
    tournament_matchmaking_helper,
    update_court_db,
    update_participants_flag_db,
    update_score_db,
)
from .activity.participant import (
    get_activity_participants,
    get_activity_request_list,
    get_activity_waiting_list,
)
from .admin.cron_task import (
    periodic_task,
    qt_task,
    remove_expired_unscheduled_series_game_extra_bookings,
    send_reminder_notification_fo_series_match,
)
from .admin.log import download_log_file_from_log, get_all_log_files_from_log
from .authentication.forgot import forgot_password_with_email

# from .authentication.login import initialize_session_cookie, sign_in_user
from .authentication.login import sign_in_user
from .authentication.permission import get_permission_of_user_from_db
from .authentication.role_check import (
    allow_all_users_for_booking,
    player_check,
    staff_check_for_booking,
    staff_check_for_my_club,
)
from .authentication.signup import (
    create_new_account,
    create_new_account_without_password,
    insert_new_club,
    insert_new_player,
)

# from .authentication.token import get_current_user, get_user_token
from .authentication.token import get_current_user
from .authentication.verify import verify_emaildb, verify_phonedb
from .club.account import (
    get_club_admin_emailFB,
    update_club_admin_emailFB,
    update_club_admin_passwordFB,
)
from .club.chat_channels import (
    create_chat_channel_for_series_match,
    create_chat_channel_from_record_db,
)
from .club.coach import (
    add_coach_in_db,
    get_a_coach_from_db,
    get_all_coaches_from_db,
    remove_coach_from_db,
    update_coach_in_db,
)
from .club.court import (
    add_court_in_db,
    get_a_court_from_db,
    get_a_court_from_ids_db,
    get_all_courts_from_db,
    remove_court_from_db,
    update_court_in_db,
)
from .club.discount_code import (
    add_discount_code_in_db,
    check_a_discount_code_in_db,
    get_a_discount_code_from_db,
    get_all_discount_codes_from_db,
    remove_discount_code_from_db,
    update_discount_code_in_db,
)
from .club.event_logs import (
    create_event_log_doc_from_activity_record_doc,
    create_event_logs_for_update_activity,
    create_event_logs_from_activity_record_id,
)
from .club.follower import (
    create_follower_db,
    get_all_club_subscribe_follower_ids,
    get_player_info_of_followers,
    get_valid_follower_ids,
    send_email_to_the_followers,
    unsubscribe_club_follower,
)
from .club.info import (
    get_club_info_detail_response,
    get_club_info_from_db,
    get_club_info_from_with_short_name,
    get_club_timezone,
    remove_club,
    restore_club,
    update_club_email_in_fb,
    update_club_info_in_db,
)
from .club.invite import (
    create_invite_id,
    get_invite_info,
    send_invite_with_apikey,
    update_invite_status,
)
from .club.member import (
    add_player_to_membershipdb,
    check_membership_exists,
    get_a_member_infodb,
    get_all_followers_and_members_db,
    remove_member_from_a_membershipdb,
    update_members_membership_infodb,
)
from .club.membership import (
    add_new_club_membership,
    get_all_club_membershipdb,
    get_all_membersdb,
    get_club_membershipdb,
    get_player_membership_discount_db,
    get_some_info_of_all_membershipsdb,
    remove_club_membershipdb,
    send_invite,
    update_club_membershipdb,
)
from .club.notification import (
    club_notification_filter,
    global_notification_filter,
    notification_filter,
    send_multicast_notification,
    send_one_notification,
)
from .club.price import (
    add_multiple_prices_in_db,
    add_price_in_db,
    get_a_price_from_db,
    get_all_prices_from_db,
    get_multiple_prices_from_db,
    remove_price_from_db,
    update_multiple_price_in_db,
    update_price_in_db,
)
from .club.price_list import (
    add_price_list_in_db,
    get_a_price_list_from_db,
    get_active_pricelist_from_db,
    get_all_price_lists_from_db,
    remove_price_list_from_db,
    update_price_list_in_db,
)
from .club.reward import (
    add_reward_in_db,
    get_a_reward_from_db,
    get_all_rewards_from_db,
    get_player_info_of_followers_for_reward,
    purchase_a_reward_from_db,
    remove_reward_from_db,
    update_reward_in_db,
)
from .club.reward_history import (
    get_all_reward_histories_from_db,
    get_player_reward_histories_from_db,
)
from .club.slot import (
    _overlap_check,
    add_slot_in_db,
    get_a_slot_from_db,
    get_all_slots_from_db,
    remove_slot_from_db,
    update_slot_in_db,
)
from .club.statistics import (
    count_statistics_for_specific_time_range_from_db,
    get_activity_transaction_history,
    get_online_payment_list_for_club,
)
from .mail import (
    generate_booking_cancel_mail,
    generate_booking_confirmation_mail,
    generate_cancelation_mail,
    send_mail,
)
from .player.player_activity import (
    get_all_activities_of_a_club_from_db,
    get_user_activity_history,
)
from .player.player_booking import (
    add_players_to_booking,
    create_player_booking_db,
    format_available_slots_for_response,
    get_all_bookings_by_player_from_db,
    get_available_slots_with_prices_from_db,
    get_filtered_clubs_from_db,
    get_searched_clubs_from_db,
    get_searched_clubs_without_radius_from_db,
    is_court_slot_available,
    remove_empty_courts_zero_slots,
    update_payment_status_db,
)
from .player.player_club_info import (
    get_clubs_followed_by_player_from_db,
    get_following_club_coins_info,
    get_next_reward_coins,
    get_searched_players,
    get_status_info_of_a_follower_from_db,
    get_status_info_of_all_followers_from_db,
    update_status_info_of_a_follower_in_db,
)
from .player.player_credit import buy_credit_by_player
from .player.player_membership import (
    add_membershipinfo_in_db,
    cancel_membership_by_player_in_db,
    get_all_memberships_of_a_player_from_db,
    get_all_membershipsdb,
    get_membershipinfo_from_db,
    subscripte_to_membership,
    update_membershipinfo_in_db,
)
from .series_games.division import (
    add_team_to_division,
    check_booking_slot_for_league_divisions,
    check_season_duration_for_round_schedule_matches,
    create_division_db,
    delete_division_from_db,
    delete_divisions_of_league,
    delete_team_from_division,
    generate_round_schedule_matches_for_division,
    get_division_info_from_db,
    get_division_info_list_for_season_from_db,
    get_division_info_list_from_db,
    get_payment_for_division_single_team,
    send_notification_to_division_single_team,
    send_notification_to_division_team,
    total_match,
    total_weeks_rounds,
    total_weeks_rounds_float,
    update_division_info,
    update_paid_status_of_the_team_in_division_from_db,
)
from .series_games.league import (
    create_league_db,
    get_league_full_info_from_db,
    get_league_list_full_info_from_db,
    update_league_and_division_db,
    update_league_info_db,
)
from .series_games.match import (
    check_all_match_played,
    check_round_schedule_match_exist,
    check_teams_admin_payment,
    create_series_match_db,
    get_all_round_schedule_matches,
    get_all_series_match_for_division,
    get_reschedule_options_from_db,
    reschedule_series_games_match,
    update_match_info,
)
from .series_games.season import (
    check_season_status,
    create_new_season,
    create_new_season_from_previous,
    create_season_db,
    delete_season_of_league,
    get_first_season_of_league,
    get_latest_season_of_league,
    get_season_end_date,
    get_season_end_datetime_utc,
    get_season_info_from_db,
    get_season_list_full_info_from_db,
    get_season_start_datetime_utc,
    update_season_info_db,
)
from .series_games.series import (
    create_draft_series_db,
    create_series_db,
    get_series_league_full_info_from_db,
    get_series_league_list_info_from_db,
    update_series_db,
)
from .series_games.team import (
    add_player_to_the_team_from_db,
    get_all_player_list_info_for_division_teams,
    get_team_info_from_db,
    get_team_list_by_id,
    get_team_list_from_db,
    remove_series_games_team_from_db,
)
from .staff.staff import (
    create_staff_db,
    get_a_staff_info_db,
    get_all_staff_infos_db,
    get_authorized_staffs_db,
    remove_staff_db,
    remove_staff_from_fb,
    update_staff_db,
    update_staff_email_in_fb,
)

ENCODERS_BY_TYPE[ObjectId] = str
