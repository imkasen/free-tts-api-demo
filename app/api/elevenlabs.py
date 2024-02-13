"""
API requests of ElevenLabs
"""

from typing import Any, NoReturn

from elevenlabs.api import API, Subscription, Voices, api_base_url_v1
from loguru import logger
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


class ElevenLabs:
    """
    ElevenLabs class
    """

    voices_name_list: list[tuple[str, str]] = []
    voices_db = TinyDB(storage=MemoryStorage)

    @classmethod
    def get_voice_list(cls) -> NoReturn:
        """
        Get voice informations of ElevenLabs
        """
        assert not cls.voices_name_list
        assert not cls.voices_db.all()

        for voice in Voices.from_api():
            cls.voices_name_list.append((voice.name, voice.voice_id))
            cls.voices_db.insert(vars(voice))

    @classmethod
    def get_voices(cls) -> list[tuple[str, str]]:
        """
        Get a name list of voice speakers

        :return: a list containing voice names
        """
        if not cls.voices_name_list:
            cls.get_voice_list()
        return cls.voices_name_list

    @classmethod
    def get_detailed_voice_info(cls, voice_id: str) -> tuple[str, str, str, str, str, str]:
        """
        Get detailed voice information based on voice_id

        :param voice_id: id of voice
        :return: information of gender, accent, age, description, use case and sample url.
        """
        if not cls.voices_name_list:
            cls.get_voice_list()
        try:
            voice_info: list[dict[str, Any]] = cls.voices_db.search(where("voice_id") == voice_id)
            assert len(voice_info) == 1
            return (
                voice_info[0]["labels"]["gender"],
                voice_info[0]["labels"]["accent"],
                voice_info[0]["labels"]["age"],
                voice_info[0]["labels"]["description"],
                voice_info[0]["labels"]["use case"],
                voice_info[0]["preview_url"],
            )
        except KeyError as e:
            logger.error(e)
            raise RuntimeError(e) from e

    @classmethod
    def get_token_stauts(cls, token: str) -> tuple[int, int, int]:
        """
        Get token status

        :param token: API token
        :return: some token information.
        """
        url: str = f"{api_base_url_v1}/user/subscription"
        resp: dict[str, Any] = API.get(url=url, api_key=token).json()
        sub_info: Subscription = Subscription(**resp)
        return sub_info.character_count, sub_info.character_limit, sub_info.next_character_count_reset_unix

    @classmethod
    def clear_info(cls) -> bool:
        """
        Clear all stored information.
        """
        if cls.voices_name_list:
            cls.voices_name_list = []
        if cls.voices_db.all():
            cls.voices_db.truncate()
        return (not cls.voices_name_list) and (not cls.voices_db.all())
