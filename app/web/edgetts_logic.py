"""
Some logic funtions needed by Gradio components
"""

import gradio as gr
from api import EdgeTTS
from loguru import logger


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
