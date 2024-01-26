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


def create_tts_order(  # pylint: disable=R0913
    url: str,
    token: str,
    text: str,
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
