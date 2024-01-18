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


def clear_ttsmaker_info():
    """
    Clear all stored TTSMaker information
    """
    if TTSMaker.clear_info():
        gr.Warning("Clear all stored TTSMaker information")
    else:
        raise gr.Error("Fail to clear TTSMaker information")
