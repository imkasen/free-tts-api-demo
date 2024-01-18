"""
Some logic funtions needed by Gradio components
"""
import gradio as gr
from api_requests import TTSMaker


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


def clear_ttsmaker_info():
    """
    Clear all stored TTSMaker information
    """
    if TTSMaker.clear_info():
        gr.Warning("Clear all stored TTSMaker information")
    else:
        raise gr.Error("Fail to clear TTSMaker information")
