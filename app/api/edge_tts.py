"""
API requests of edge-tts
"""

from typing import Any, NoReturn

import edge_tts
import numpy as np
import requests
from edge_tts.constants import VOICE_LIST
from loguru import logger
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


class EdgeTTS:
    """
    edge-tts class
    """

    language_code_list: list[str] = []
    voices_db = TinyDB(storage=MemoryStorage)

    @staticmethod
    def pad_buffer(audio: bytes) -> str:
        """
        Pad buffer to multiple of 2 bytes

        :param audio: original binary data of audio
        :return: binary data of audio after padding
        """
        buffer_size: int = len(audio)
        element_size: int = np.dtype(np.int16).itemsize
        if buffer_size % element_size != 0:
            audio = audio + b"\0" * (element_size - (buffer_size % element_size))
        return audio

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
                if not cls.language_code_list:
                    for voice in res.json():
                        language_code: str = voice["Locale"]
                        if language_code not in cls.language_code_list:
                            cls.language_code_list.append(language_code)
        except (requests.exceptions.RequestException, KeyError) as e:
            logger.critical(e)
            raise RuntimeError(e) from e

    @classmethod
    def get_language_code(cls) -> list[str]:
        """
        Get language code of edge-tts

        :return: a list of language code
        """
        if not cls.language_code_list:
            cls.get_voice_list()
        return cls.language_code_list

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
            for voice in cls.voices_db.search(where("Locale") == lang_code):
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
    async def generate_audio(cls, text: str, voice: str) -> tuple[int, Any]:
        """
        Generate temporary audio file using edge-tts

        :param text: audio content text
        :param voice: voice speaker name
        :return: sample rate, audio data
        """
        audio: bytes = b""
        communicate = edge_tts.Communicate(text, voice)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]
        return (44100, np.frombuffer(cls.pad_buffer(audio), dtype=np.int16))

    @classmethod
    def clear_info(cls) -> bool:
        """
        Clear all stored information.
        """
        if cls.language_code_list:
            cls.language_code_list = []
        if cls.voices_db.all():
            cls.voices_db.truncate()
        return (not cls.language_code_list) and (not cls.voices_db.all())
