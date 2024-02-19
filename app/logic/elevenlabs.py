"""
Some logic funtions needed by Gradio components
"""

import datetime
from typing import Any

import gradio as gr
import numpy as np
from api import ElevenLabs
from loguru import logger


def pad_buffer(audio: bytes) -> bytes:
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


def get_elevenlabs_voices() -> gr.Dropdown:
    """
    Get a list of voices used by gradio dropdown component.

    :return: a gradio dropdown component
    """
    voices_list: list[tuple[str, str]] = ElevenLabs.get_voices()
    return gr.Dropdown(choices=voices_list)


def get_elevenlabs_single_voice_info(
    voice_id: str,
) -> tuple[gr.Textbox, gr.Textbox, gr.Textbox, gr.Textbox, gr.Textbox, gr.Audio]:
    """
    Get detailed voice information.

    :param voice_id: id of voice
    :return: some gradio components
    """
    if not voice_id:
        logger.error("Voice is not selected!")
        raise gr.Error("Voice is not selected!")

    try:
        gender, accent, age, desc, use_case, url = ElevenLabs.get_detailed_voice_info(voice_id)
        return (
            gr.Textbox(value=gender, visible=True),
            gr.Textbox(value=accent, visible=True),
            gr.Textbox(value=age, visible=True),
            gr.Textbox(value=desc, visible=True),
            gr.Textbox(value=use_case, visible=True),
            gr.Audio(value=url, visible=True),
        )
    except RuntimeError as e:
        raise gr.Error(e)


def get_elevenlabs_token_status(token: str) -> tuple[gr.Textbox, gr.Textbox, gr.Textbox, gr.Textbox]:
    """
    Get token status

    :param token: API token
    :return: some gradio components
    """
    if not token:
        logger.error("API token is empty!")
        raise gr.Error("API token is empty!")

    count, limit, unix_timestamp = ElevenLabs.get_token_stauts(token)
    left: int = limit - count
    reset_time: str = datetime.datetime.utcfromtimestamp(unix_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    return (
        gr.Textbox(value=count),
        gr.Textbox(value=left),
        gr.Textbox(value=limit),
        gr.Textbox(value=reset_time),
    )


def get_elevenlabs_audio(  # pylint: disable=R0913
    token: str,
    text: str,
    voice_id: str,
    model: str,
    stability: float,
    similarity: float,
    style: float,
    speaker_boost: bool,
) -> tuple[int, Any]:
    """
    Get audio data

    :param token: API token
    :param text: text content
    :param voice_id: voice speaker id
    :param model: model name
    :param stability: stability value
    :param similarity: similarity value
    :param style: style value
    :param speaker_boost: use speaker boost value
    :return: sample rate, audio data
    """
    if not token:
        logger.error("Token is empty!")
        raise gr.Error("Token is empty!")
    if not text:
        logger.error("Text content is empty!")
        raise gr.Error("Text content is empty!")
    if not voice_id:
        logger.error("Voice speaker is not selected!")
        raise gr.Error("Voice speaker is not selected!")

    audio_data: bytes = ElevenLabs.generate_audio(
        token,
        text,
        voice_id,
        model,
        stability,
        similarity,
        style,
        speaker_boost,
    )
    return 44100, np.frombuffer(pad_buffer(audio_data), dtype=np.int16)


def clear_elevenlabs_info() -> tuple[gr.Textbox, gr.Textbox, gr.Textbox, gr.Textbox, gr.Textbox, gr.Audio]:
    """
    Clear all stored ElevenLabs information.
    """
    if ElevenLabs.clear_info():
        logger.warning("Clear all stored ElevenLabs information")
        gr.Warning("Clear all stored ElevenLabs information")
        return (
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Audio(visible=False),
        )
    logger.error("Fail to clear ElevenLabs information")
    raise gr.Error("Fail to clear ElevenLabs information")
