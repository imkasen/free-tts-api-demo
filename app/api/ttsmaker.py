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
                if res.json()["status"] == "success":
                    cls.language_list = res.json()["support_language_list"]
                    if not cls.voices_db.all():
                        cls.insert_detailed_voices_list(res.json()["voices_detailed_list"])
                else:
                    err_msg: str = f"{res.json()['error_code']}: {res.json()['error_details']}"
                    logger.error(err_msg)
                    raise RuntimeError(err_msg)
        except requests.exceptions.RequestException as e:
            logger.critical(e)
            raise RuntimeError(e) from e

    @classmethod
    def get_languages(cls, url: str, token: str) -> list[str]:
        """
        Get supported languages list

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
        Get supported voices list

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
    def get_detailed_voice_info(cls, url: str, token: str, voice_id: int) -> tuple[str, bool, int, str]:
        """
        Get gender, queue, characters list and audio sample url based on voice id.

        :param url: URL of TTSMaker API
        :param token: developer token
        :param voice_id: ID of voice selected by user
        :return: a tuple of informations
        """
        if not cls.voices_db.all():
            cls.get_voice_list(url, token)
        voice_info: list[dict[str, int | str | bool]] = cls.voices_db.search(Query().id == voice_id)
        assert len(voice_info) == 1
        return (
            "Male" if voice_info[0]["gender"] == 1 else "Female",
            voice_info[0]["is_need_queue"],
            voice_info[0]["text_characters_limit"],
            voice_info[0]["audio_sample_file_url"],
        )

    @classmethod
    def create_tts_order(  # pylint: disable=R0913
        cls,
        url: str,
        token: str,
        text: str,
        voice_id: int,
        audio_format: str = "mp3",
        audio_speed: float = 1.0,
        audio_volume: float = 0.0,
        text_paragraph_pause_time: int = 0,
    ) -> str | None:
        """
        Send post request to generate audio.

        :param url: URL of TTSMaker API
        :param token: developer token
        :param text: text content of audio
        :param voice_id: ID of speaker voice
        :param audio_format: mp3/ogg/aac/opus/wav, defaults to "mp3"
        :param audio_speed: range 0.5-2.0, 0.5: 50% speed, 1.0: 100% speed, 2.0: 200% speed, defaults to 1.0
        :param audio_volume: range 0-10, 1: volume+10%, 8: volume+80%, 10: volume+100%, defaults to 0.0
        :param text_paragraph_pause_time: auto insert audio paragraph pause time, range 500-5000, unit: millisecond,
                                          maximum 50 pauses can be inserted. If more than 50 pauses,
                                          all pauses will be canceled automatically, defaults to 0
        :return: URL of generated audio
        """
        try:
            headers: dict[str, str] = {"Content-Type": "application/json; charset=utf-8"}
            params: dict[str, int | float | str] = {
                "token": token,
                "text": text,
                "voice_id": voice_id,
                "audio_format": audio_format,
                "audio_speed": audio_speed,
                "audio_volume": audio_volume,
                "text_paragraph_pause_time": text_paragraph_pause_time,
            }
            res: requests.Response = requests.post(
                url=f"https://{url}/v1/create-tts-order",
                headers=headers,
                json=params,
                timeout=5,
            )
            if res.status_code == 200:
                if res.json()["status"] == "success":
                    return res.json()["audio_file_url"]
                err_msg: str = f"{res.json()['error_code']}: {res.json()['error_details']}"
                logger.error(err_msg)
                raise RuntimeError(err_msg)
        except requests.exceptions.RequestException as e:
            logger.critical(e)
            raise RuntimeError(e) from e
        return None

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
