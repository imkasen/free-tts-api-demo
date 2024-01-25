"""
API requests of TTSMaker
"""
from typing import NoReturn

import requests
from loguru import logger
from tinydb import Query, TinyDB
from tinydb.storages import MemoryStorage


class TTSMaker:
    """
    TTSMaker Class
    """

    language_list: list[str] = []
    voices_db = TinyDB(storage=MemoryStorage)

    @classmethod
    def insert_detailed_voices_list(cls, voices_detailed_list: list[dict[str, int | str | bool]]) -> NoReturn:
        """
        Store 'voices_detailed_list' into TinyDB.

        :param voices_detailed_list: list containing speaker infomations
        """
        cls.voices_db.insert_multiple(voices_detailed_list)

    @classmethod
    def get_voice_list(cls, url: str, token: str) -> NoReturn:
        """
        Get voice information of TTSMaker.

        :param url: URL of TTSMarker API
        :param token: developer token
        """
        try:
            params: dict[str, str] = {"token": token}
            res: requests.Response = requests.get(url=f"https://{url}/v1/get-voice-list", params=params, timeout=5)
            if res.status_code == 200:
                error_code: str = res.json()["error_code"]
                if not error_code:
                    cls.language_list = res.json()["support_language_list"]
                    if not cls.voices_db.all():
                        cls.insert_detailed_voices_list(res.json()["voices_detailed_list"])
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
        if not cls.language_list:
            cls.get_voice_list(url, token)
        return cls.language_list

    @classmethod
    def get_voices(cls, url: str, token: str, language: str) -> list[tuple[str, int]]:
        """
        return supported voices list

        :param url: URL of TTSMaker API
        :param token: developer token
        :param language: user selected language
        :return: a list of multiple tuples consisting of names and ids
        """
        if not cls.voices_db.all():
            cls.get_voice_list(url, token)
        voices_list: list[tuple[str, int]] = [
            (voice_info["name"], voice_info["id"]) for voice_info in cls.voices_db.search(Query().language == language)
        ]
        return voices_list

    @classmethod
    def clear_info(cls) -> bool:
        """
        Clear all stored information
        """
        if cls.language_list:
            cls.language_list = []
        if cls.voices_db.all():
            cls.voices_db.truncate()
        return (not cls.language_list) and (not cls.voices_db.all())
