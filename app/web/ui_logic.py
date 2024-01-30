"""
Some logic funtions needed by Gradio components
"""
import gradio as gr
from api import TTSMaker
from loguru import logger


def get_ttsmaker_languages(url: str, token: str) -> gr.Dropdown:
    """
    Get languages supported by TTSMaker

    :param url: URL of TTSMaker API
    :param token: developer token
    :return: list of languages
    """
    if not url:
        logger.error("URL of TTSMaker API is empty!")
        raise gr.Error("URL of TTSMaker API is empty!")
    if not token:
        logger.error("Token of TTSMaker API is empty!")
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
        logger.error("URL of TTSMaker API is empty!")
        raise gr.Error("URL of TTSMaker API is empty!")
    if not token:
        logger.error("Token of TTSMaker API is empty!")
        raise gr.Error("Token of TTSMaker API is empty!")
    if not language:
        logger.error("Language is not selected!")
        raise gr.Error("Language is not selected!")

    try:
        voices_list: list[tuple[str, int]] = TTSMaker.get_voices(url, token, language)
        return gr.Dropdown(choices=voices_list)
    except RuntimeError as e:
        raise gr.Error(e)


def get_ttsmaker_single_voice_info(
    url: str, token: str, voice_id: int, text: str
) -> tuple[gr.Textbox, gr.Textbox, gr.Textbox, gr.Audio, gr.Markdown]:
    """
    Get detailed voice information based on sepecific voice id.

    :param url: URL of TTSMaker API
    :param token: developer token
    :param voice_id: ID of voice selected by user
    :param text: text content
    :return: some visible gradio components
    """
    if not url:
        logger.error("URL of TTSMaker API is empty!")
        raise gr.Error("URL of TTSMaker API is empty!")
    if not token:
        logger.error("Token of TTSMaker API is empty!")
        raise gr.Error("Token of TTSMaker API is empty!")

    try:
        gender, queue, limit, sample_url = TTSMaker.get_detailed_voice_info(url, token, voice_id)
        return (
            gr.Textbox(value=gender, visible=True),
            gr.Textbox(value=queue, visible=True),
            gr.Textbox(value=limit, visible=True),
            gr.Audio(value=sample_url, visible=True),
            refresh_characters_limit(limit, text),
        )
    except RuntimeError as e:
        raise gr.Error(e)


def refresh_characters_limit(limit: int, text: str) -> gr.Markdown:
    """
    Count remaining characters

    :param limit: maximum allowed characters
    :param text: current text content
    :return: Markdown component
    """
    left: int = limit - len(text) if (limit - len(text)) >= 0 else 0
    return gr.Markdown(
        f"Maximum {limit} input characters, {len(text)} characters already entered, {left} characters remaining.",
        visible=True,
    )


def create_tts_order(  # pylint: disable=R0913
    url: str,
    token: str,
    text: str,
    text_limit: float,
    voice_id: int,
    audio_format: str = "mp3",
    audio_speed: float = 1.0,
    audio_volume: float = 0.0,
    text_paragraph_pause_time: int = 0,
) -> gr.Audio:
    """
    Ready to send post request to generate audio.

    :param url: URL of TTSMaker API
    :param token: developer token
    :param text: text content of audio
    :param voice_id: ID of speaker voice
    :param audio_format: mp3/ogg/aac/opus/wav, defaults to "mp3"
    :param audio_speed: range 0.5-2.0, 0.5: 50% speed, 1.0: 100% speed, 2.0: 200% speed, defaults to 1.0
    :param audio_volume: range 0-10, 1: volume+10%, 8: volume+80%, 10: volume+100%, defaults to 0.0
    :param text_paragraph_pause_time: auto insert audio paragraph pause time, range 500-5000, unit: millisecond,
                                        maximum 50 pauses can be inserted. If more than 50 pauses,
                                        all pauses will be canceled automatically, defaults to 0
    :return: URL of generated audio
    """
    if len(text) > int(text_limit):
        logger.error("The length of the text content exceeds the character limit!")
        raise gr.Error("The length of the text content exceeds the character limit!")
    try:
        generated_audio_url: str = TTSMaker.create_tts_order(
            url,
            token,
            text,
            voice_id,
            audio_format,
            audio_speed,
            audio_volume,
            text_paragraph_pause_time * 1000,  # convert seconds to millisecond
        )
        return gr.Audio(value=generated_audio_url, interactive=True)
    except RuntimeError as e:
        raise gr.Error(e)


def check_token_status(url: str, token: str):
    """
    Check and get token status

    :param url: URL of TTSMaker API
    :param token: developer token
    :return: some visiable gradio components
    """
    if not url:
        logger.error("URL of TTSMaker API is empty!")
        raise gr.Error("URL of TTSMaker API is empty!")
    if not token:
        logger.error("Token of TTSMaker API is empty!")
        raise gr.Error("Token of TTSMaker API is empty!")

    try:
        max_chars, used_chars, avail_chars, left_days = TTSMaker.get_token_status(url, token)
        return (
            gr.Textbox(value=max_chars),
            gr.Textbox(value=used_chars),
            gr.Textbox(value=avail_chars),
            gr.Textbox(value=left_days),
        )
    except RuntimeError as e:
        raise gr.Error(e)


def clear_ttsmaker_info() -> tuple[gr.Textbox, gr.Textbox, gr.Textbox, gr.Audio, gr.Markdown]:
    """
    Clear all stored TTSMaker information
    """
    if TTSMaker.clear_info():
        logger.warning("Clear all stored TTSMaker information")
        gr.Warning("Clear all stored TTSMaker information")
        return (
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Textbox(visible=False),
            gr.Audio(visible=False),
            gr.Markdown(visible=False),
        )
    logger.error("Fail to clear TTSMaker information")
    raise gr.Error("Fail to clear TTSMaker information")
