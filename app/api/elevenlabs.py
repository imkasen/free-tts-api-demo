"""
API requests of ElevenLabs
"""

from typing import Any, NoReturn

import numpy as np
from elevenlabs import API, Subscription, Voice, Voices, VoiceSettings, api_base_url_v1, generate
from loguru import logger
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


class ElevenLabs:
    """
    ElevenLabs class
    """

    voices_name_list: list[tuple[str, str]] = []
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
    def generate_audio(  # pylint: disable=R0913
        cls,
        token: str,
        text: str,
        voice_id: str,
        model: str = "eleven_multilingual_v2",
        stability: float = 0.71,
        similarity: float = 0.5,
        style: float = 0.0,
        speaker_boost: bool = True,
    ) -> tuple[int, Any]:
        """
        Generate audio

        :param token: API token
        :param text: text content
        :param model: elevenlabs model name
        :param voice_id: voice speaker id
        :param stability: stability value
        :param similarity: similarity value
        :param style: style value
        :param speaker_boost: use speaker boost value
        :return: sample rate, audio data
        """
        settings = VoiceSettings(
            stability=stability,
            similarity_boost=similarity,
            style=style,
            use_speaker_boost=speaker_boost,
        )
        voice = Voice(voice_id=voice_id, settings=settings)
        audio: bytes = generate(text=text, api_key=token, model=model, voice=voice)
        return (44100, np.frombuffer(cls.pad_buffer(audio), dtype=np.int16))

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
