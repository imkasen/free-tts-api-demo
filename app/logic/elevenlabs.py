"""
Some logic funtions needed by Gradio components
"""

import gradio as gr
from api import ElevenLabs
from loguru import logger


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
