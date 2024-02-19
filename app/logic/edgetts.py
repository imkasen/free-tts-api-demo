"""
Some logic funtions needed by Gradio components
"""

import asyncio
from typing import Any

import gradio as gr
import numpy as np
from api import EdgeTTS
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


def get_edgetts_language_code() -> gr.Dropdown:
    """
    Get language list of edge-tts

    :return: a gradio dropdown component
    """
    try:
        language_list: list[str] = EdgeTTS.get_language_code()
        return gr.Dropdown(choices=language_list)
    except RuntimeError as e:
        raise gr.Error(e)


def get_edgetts_voices(lang_code: str) -> gr.Dropdown:
    """
    Get the list of voices available for the specified language code.

    :param lang_code: The language code for which to retrieve the voices.
    :return: A Gradio Dropdown object containing the choices of voices.
    """
    if not lang_code:
        logger.error("Language code is empty!")
        raise gr.Error("Language code is empty!")

    try:
        voices_list: list[tuple[str, str]] = EdgeTTS.get_voices(lang_code)
        return gr.Dropdown(choices=voices_list)
    except RuntimeError as e:
        raise gr.Error(e)


def get_edgetts_single_voice_info(short_name: str) -> tuple[gr.Textbox, gr.Textbox, gr.Textbox]:
    """
    Get voice information based on voice name

    :param short_name: voice short name
    :return: visiable gradio conponents
    """
    if not short_name:
        logger.error("Voice is not selected!")
        raise gr.Error("Voice is not selected!")

    try:
        gender, categories, personalities = EdgeTTS.get_voice_info(short_name)
        return (
            gr.Textbox(value=gender, visible=True),
            gr.Textbox(value=categories, visible=True),
            gr.Textbox(value=personalities, visible=True),
        )
    except RuntimeError as e:
        raise gr.Error(e)


def get_edgetts_audio(text: str, voice: str) -> tuple[int, Any]:
    """
    Get audio result from edge-tts

    :param text: content text
    :param voice: voice speaker name
    :return: sample rate, audio data
    """
    if not text:
        logger.error("Audio content text is empty!")
        raise gr.Error("Audio content text is empty!")
    if not voice:
        logger.error("Voice speaker is not selected!")
        raise gr.Error("Voice speaker is not selected!")

    audio_data: bytes = asyncio.run(EdgeTTS.generate_audio(text, voice))
    return 44100, np.frombuffer(pad_buffer(audio_data), dtype=np.int16)


def clear_edgetts_info() -> tuple[gr.Textbox, gr.Textbox, gr.Textbox]:
    """
    Clear all stored edge-tts information.
    """
    if EdgeTTS.clear_info():
        logger.warning("Clear all edge-tts information")
        gr.Warning("Clear all edge-tts information")
        return gr.Textbox(visible=False), gr.Textbox(visible=False), gr.Textbox(visible=False)
    logger.error("Fail to clear edge-tts information")
    raise gr.Error("Fail to clear edge-tts information")
