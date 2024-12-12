import json
from os import path
from typing import Any, Dict

import utils

# Config file paths
translation_file = path.join("utils", "translation.json")


class WebPortalTranslation:
    """Translation for Web Portal"""

    def __init__(self):
        """Initialize the WebPortalTranslation class."""

        self.translation_doc = self.load_file(translation_file)

    def load_file(self, translation_file_path) -> Dict[str, Any]:
        """Load the translation file.

        Args:
            config_path (str): Path to the translation file

        Returns:
            Dict[str, str]: Translations

        """

        with open(
            file=translation_file_path, mode="r", encoding="utf-8"
        ) as translation_file:
            translations: Dict[str, Any] = json.load(translation_file)

        return translations

    def translate(self, translation_dict):
        """Get translation given proper information.

        Args:
            translation_dict (str): dictionary containing keys.
            dictKeys: CLUB_NAME
                      ACTIVITY_TYPE
                      NUMBER_1
                      JOIN_REQUEST
                      translation_type

            JsonKeys: ACTIVITY_TYPE -> match, training, tournament, booking, activity
                      JOIN_REQUEST -> accepted, rejected
                      REMOVE_PLAYER_FROM_ACTIVITY -> CLUB_NAME, ACTIVITY_TYPE
                      PLAYER_REFUNDED_SUCCESSFULLY
                      SPOT_AVAILABLE -> NUMBER_1, ACTIVITY_TYPE
                      UPDATE_JOIN_REQUEST -> CLUB_NAME, JOIN_REQUEST, ACTIVITY_TYPE
                      ACTIVITY_FULL -> ACTIVITY_TYPE
                      INVITE_PLAYER -> CLUB_NAME, ACTIVITY_TYPE

        Returns:
            str

        """
        try:
            info = self.translation_doc[translation_dict["translation_type"]]

            if translation_dict["translation_type"] == "default":
                return self.translation_doc["ERROR"]
            message = info[translation_dict["lang"]]
            for item in info["variables"]:
                if item == "NUMBERS":
                    for number in translation_dict[item.lower()]:
                        message = message.replace(f"${item}$", str(number), 1)
                if item in ["ACTIVITY_TYPE", "JOIN_REQUEST"]:
                    temp = translation_dict[item.lower()].lower()
                    if temp in self.translation_doc[item]:
                        translation_dict[item.lower()] = self.translation_doc[item][
                            temp
                        ][translation_dict["lang"]]
                    else:
                        temp = list(self.translation_doc[item].keys())[-1]
                        translation_dict[item.lower()] = self.translation_doc[item][
                            temp
                        ][translation_dict["lang"]]

                if item.lower() not in translation_dict.keys() or translation_dict[
                    item.lower()
                ] in ["default"]:
                    return self.translation_doc["ERROR"]

                message = message.replace(
                    f"${item}$", str(translation_dict[item.lower()])
                )
                message = message.replace(message[0], message[0].upper(), 1)

            return message
        except Exception as e:
            utils.raise_exception(e=e)


translator = WebPortalTranslation()


if __name__ == "__main__":
    translator
    print(translation_file)
