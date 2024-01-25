"""
Some logic funtions needed by Gradio components
"""
import gradio as gr
from api import TTSMaker


def get_ttsmaker_languages(url: str, token: str) -> gr.Dropdown:
    """
    Get languages supported by TTSMaker

    :param url: URL of TTSMaker API
    :param token: developer token
    :return: list of languages
    """
    if not url:
        raise gr.Error("URL of TTSMaker API is empty!")
    if not token:
        raise gr.Error("Token of TTSMaker API is empty!")

    try:
        languages_list: list[str] = TTSMaker.get_languages(url, token)
        return gr.Dropdown(choices=languages_list)
    except RuntimeError as e:
        raise gr.Error(e)


def get_ttsmaker_voices(url: str, token: str, language: str) -> gr.Dropdown:
    """
    Get voices supported by TTSMaker based on user selected language.

    :param url: URL of TTSMaker API
    :param token: developer token
    :param language: user selected language
    :return: a list of multiple tuples consisting of names and ids
    """
    if not url:
        raise gr.Error("URL of TTSMaker API is empty!")
    if not token:
        raise gr.Error("Token of TTSMaker API is empty!")
    if not language:
        raise gr.Error("Language is not selected!")

    try:
        voices_list: list[tuple[str, int]] = TTSMaker.get_voices(url, token, language)
        return gr.Dropdown(choices=voices_list)
    except RuntimeError as e:
        raise gr.Error(e)


def get_ttsmaker_single_voice_info(
    url: str, token: str, voice_id: int
) -> tuple[gr.Textbox, gr.Textbox, gr.Textbox, gr.Audio]:
    """
    Get detailed voice information based on sepecific voice id.

    :param url: URL of TTSMaker API
    :param token: developer token
    :param voice_id: ID of voice selected by user
    :return: some visible gradio components
    """
    if not url:
        raise gr.Error("URL of TTSMaker API is empty!")
    if not token:
        raise gr.Error("Token of TTSMaker API is empty!")

    try:
        gender, queue, limit, sample_url = TTSMaker.get_detailed_voice_info(url, token, voice_id)
        return (
            gr.Textbox(value=gender, visible=True),
            gr.Textbox(value=queue, visible=True),
            gr.Textbox(value=limit, visible=True),
            gr.Audio(value=sample_url, visible=True),
        )
    except RuntimeError as e:
        raise gr.Error(e)


def clear_ttsmaker_info() -> tuple[gr.Textbox, gr.Textbox, gr.Textbox, gr.Audio]:
    """
    Clear all stored TTSMaker information
    """
    if TTSMaker.clear_info():
        gr.Warning("Clear all stored TTSMaker information")
        return (
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Audio(visible=False),
        )
    raise gr.Error("Fail to clear TTSMaker information")
