"""
Some logic funtions needed by Gradio components
"""
import gradio as gr
from api_requests import TTSMaker


def get_languages(url: str, token: str) -> gr.Dropdown:
    """
    Get languages supported by TTSMaker

    :param url: URL of TTSMaker API
    :param token: developer token
    :return: list of languages
    """
    languages_list: list[str] = TTSMaker.get_languages(url, token)
    return gr.Dropdown(choices=languages_list)
