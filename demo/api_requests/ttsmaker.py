"""
API requests of TTSMaker
"""
from typing import Any, NoReturn

import requests
from loguru import logger


class TTSMaker:
    """
    TTSMaker Class
    """

    voice_info: dict[str, int | str | dict[str, list[dict[str, int | str | bool]]]] = {}

    @staticmethod
    def process_detailed_voices_list(
        voices_detailed_list: list[dict[str, int | str | bool]]
    ) -> dict[str, list[dict[str, int | str | bool]]]:
        """
        Turn 'voices_detailed_list' into a dictionary based on different languages,
        the dictionary contains speaker informations.

        e.g.
        {
            "he":
            [
                {
                "id": 116,
                "name": "🔥Alina-🇮🇱 Israel FeMale (Hot + Unlimited)",
                "gender": 2,
                "is_need_queue": false,
                "audio_sample_file_url": "https://s2.tts-file.com/samples/116.mp3",
                "text_characters_limit": 9000
                },
                ...
            ],
            ...
        }

        :param voices_detailed_list: list containing speaker infomations
        :return: dict based on languages
        """
        tmp_dict: dict[str, list[dict[str, int | str | bool]]] = {}
        for speaker_info_dict in voices_detailed_list:
            try:
                lang: str = speaker_info_dict.pop("language")
                if lang not in tmp_dict:
                    tmp_dict[lang] = []
                tmp_dict[lang].append(speaker_info_dict)
            except KeyError as e:  # if key "language" is missing
                logger.critical(e)
                raise KeyError(e) from e
        return tmp_dict

    @classmethod
    def get_voice_list(cls, url: str, token: str) -> NoReturn:
        """
        Get voice information of TTSMaker.

        :param url: URL of TTSMarker API
        :param token: developer token
        """
        if not cls.voice_info:
            try:
                params: dict[str, str] = {"token": token}
                res: requests.Response = requests.get(url=f"https://{url}/v1/get-voice-list", params=params, timeout=5)
                if res.status_code == 200:
                    error_code: str = res.json()["error_code"]
                    if not error_code:
                        res_dict: dict[str, Any] = res.json()
                        cls.voice_info["support_language_list"] = res_dict["support_language_list"]
                        cls.voice_info["voices_id_list"] = res_dict["voices_id_list"]
                        cls.voice_info["voices_detailed_list"] = cls.process_detailed_voices_list(
                            res_dict["voices_detailed_list"]
                        )
                    elif error_code in ["TOKEN_ERROR", "LANGUAGE_NOT_FOUND"]:
                        logger.error(res.json()["error_details"])
                    else:
                        logger.critical(f"Unknown error code: {error_code}")
                        raise RuntimeError(f"Unknown error code: {error_code}")
            except requests.exceptions.RequestException as e:
                logger.critical(e)
                raise RuntimeError(e) from e

    @classmethod
    def get_languages(cls, url: str, token: str) -> list[str]:
        """
        return supported languages list

        :param url: URL of TTSMaker API
        :param token: developer token
        :return: list of languages
        """
        if (not cls.voice_info) or (not cls.voice_info["support_language_list"]):
            cls.get_voice_list(url, token)
        return cls.voice_info["support_language_list"]
