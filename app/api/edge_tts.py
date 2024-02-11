"""
API requests of edge-tts
"""

import os
import re
import tempfile
from typing import NoReturn

import edge_tts
import requests
from edge_tts.constants import VOICE_LIST
from loguru import logger
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


class EdgeTTS:
    """
    edge-tts class
    """

    audio_file_name: str = "tmp_edge_tts_audio.mp3"
    audio_file_path: str = os.path.join(tempfile.gettempdir(), audio_file_name)
    voices_db = TinyDB(storage=MemoryStorage)

    @classmethod
    def get_voice_list(cls) -> NoReturn:
        """
        Get voice list supported by Edge, this pulls data from the URL used by Microsoft Edge to return a list of
        all available voices.
        """
        try:
            headers: dict[str, str] = {
                "Authority": "speech.platform.bing.com",
                "Sec-CH-UA": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
                "Sec-CH-UA-Mobile": "?0",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41",
                "Accept": "*/*",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
            }
            res: requests.Response = requests.get(VOICE_LIST, headers=headers, timeout=5)
            if res.status_code == 200:
                if not cls.voices_db.all():
                    cls.voices_db.insert_multiple(res.json())
        except requests.exceptions.RequestException as e:
            logger.critical(e)
            raise RuntimeError(e) from e

    @classmethod
    def get_voices(cls, lang_code: str) -> list[tuple[str, str]]:
        """
        Get a list of voices based on the specified language code.

        :param lang_code: The language code to filter the voices.
        :return: A list of tuples containing the friendly name and short name of the voices.
        """
        if not cls.voices_db.all():
            cls.get_voice_list()
        try:
            voices_list: list[tuple[str, str]] = []
            reg_str: str = f"(.)*{lang_code}(.)*"
            for voice in cls.voices_db.search(where("Locale").matches(reg_str, flags=re.IGNORECASE)):
                voices_list.append((voice["FriendlyName"], voice["ShortName"]))
            return voices_list
        except KeyError as e:
            logger.error(e)
            raise RuntimeError(e) from e

    @classmethod
    def get_voice_info(cls, short_name: str) -> tuple[str, str, str]:
        """
        Get voice information based on short name

        :param short_name: short name of voice
        :return: a tuple of gender, content categories, voice personalities
        """
        if not cls.voices_db.all():
            cls.get_voice_list()
        try:
            voice_info: list[dict[str, str | dict[str, list[str]]]] = cls.voices_db.search(
                where("ShortName") == short_name
            )
            assert len(voice_info) == 1
            return (
                voice_info[0]["Gender"],
                ", ".join(voice_info[0]["VoiceTag"]["ContentCategories"]),
                ", ".join(voice_info[0]["VoiceTag"]["VoicePersonalities"]),
            )
        except KeyError as e:
            logger.error(e)
            raise RuntimeError(e) from e

    @classmethod
    async def generate_audio(cls, text: str, voice: str) -> str:
        """
        Generate temporary audio file using edge-tts

        :param text: audio content text
        :param voice: voice speaker name
        :return: audio file path name
        """
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(cls.audio_file_path)
        return cls.audio_file_path

    @classmethod
    def clear_info(cls) -> bool:
        """
        Clear all stored information.
        """
        if cls.voices_db.all():
            cls.voices_db.truncate()
        if os.path.exists(cls.audio_file_path):
            os.remove(cls.audio_file_path)
        return (not cls.voices_db.all()) and (not os.path.exists(cls.audio_file_path))
