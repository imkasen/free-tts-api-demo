"""
User Interface
"""
import gradio as gr

from .edgetts_logic import clear_edgetts_info, get_edgetts_audio, get_edgetts_single_voice_info, get_edgetts_voices
from .ttsmaker_logic import (
    check_token_status,
    clear_ttsmaker_info,
    create_tts_order,
    get_ttsmaker_languages,
    get_ttsmaker_single_voice_info,
    get_ttsmaker_voices,
    refresh_characters_limit,
)

# pylint: disable=E1101

# Gradio UI
with gr.Blocks(title="Free TTS API Demo") as ui:
    gr.HTML(value="""<h1 align="center">Free TTS API Demo</h1>""")

    # ==========================================================================
    # Edge TTS
    with gr.Tab(label="Edge TTS"):
        with gr.Row():
            with gr.Column(variant="panel"):
                edgetts_lang_code = gr.Textbox(
                    label="Language Code",
                    info="Enter the language code you want to use, e.g. 'en' for English, 'en-US' for American English",
                    max_lines=1,
                )
                edgetts_voices_input = gr.Dropdown(
                    label="Voices",
                    info="Select a speaker voice you want to use.",
                    interactive=True,
                )
                with gr.Row():
                    edgetts_gender = gr.Textbox(
                        label="Gender",
                        interactive=False,
                        max_lines=1,
                        visible=False,
                        scale=1,
                    )
                    edgetts_content_categories = gr.Textbox(
                        label="Content Categories",
                        interactive=False,
                        max_lines=1,
                        visible=False,
                        scale=2,
                    )
                    edgetts_voice_personalities = gr.Textbox(
                        label="Voice Personalities",
                        interactive=False,
                        max_lines=1,
                        visible=False,
                        scale=1,
                    )

            with gr.Column():
                edgetts_text_input = gr.Textbox(
                    placeholder="Input text here...",
                    lines=7,
                    container=False,
                    interactive=True,
                )
                with gr.Row():
                    edgetts_clear_button = gr.ClearButton(value="Clear")
                    edgetts_submit_button = gr.Button(value="Submit", variant="primary")
                edgetts_audio_output = gr.Audio(label="TTS Result", type="numpy", format="mp3")

    edgetts_voices_input.focus(
        fn=get_edgetts_voices,
        inputs=edgetts_lang_code,
        outputs=edgetts_voices_input,
    )

    edgetts_voices_input.select(
        fn=get_edgetts_single_voice_info,
        inputs=edgetts_voices_input,
        outputs=[edgetts_gender, edgetts_content_categories, edgetts_voice_personalities],
    )

    edgetts_submit_button.click(
        fn=get_edgetts_audio, inputs=[edgetts_text_input, edgetts_voices_input], outputs=edgetts_audio_output
    )

    edgetts_clear_button.add(
        components=[
            edgetts_lang_code,
            edgetts_voices_input,
            edgetts_gender,
            edgetts_content_categories,
            edgetts_voice_personalities,
            edgetts_text_input,
            edgetts_audio_output,
        ]
    )

    edgetts_clear_button.click(
        fn=clear_edgetts_info,
        outputs=[edgetts_gender, edgetts_content_categories, edgetts_voice_personalities],
    )

    # ==========================================================================
    # TTS Maker
    with gr.Tab(label="TTSMaker"):
        with gr.Row():
            with gr.Column(variant="panel"):
                ttsmaker_url_input = gr.Radio(
                    label="API URL",
                    info="Select TTSMaker API url based on your localtion.",
                    choices=["api.ttsmaker.com", "api.ttsmaker.cn"],
                    value="api.ttsmaker.com",
                    interactive=True,
                )

                ttsmaker_token_input = gr.Textbox(
                    label="Token",
                    info="Press the Enter key to get token status",
                    value="ttsmaker_demo_token",
                    interactive=True,
                    max_lines=1,
                )

                ttsmaker_languages_input = gr.Dropdown(
                    label="languages",
                    info="Select the language you want to use.",
                    interactive=True,
                )
                ttsmaker_voices_input = gr.Dropdown(
                    label="Voices",
                    info="Select a speaker voice you want to use.",
                    interactive=True,
                )

                with gr.Row():
                    ttsmaker_gender = gr.Textbox(
                        label="Gender",
                        interactive=False,
                        visible=False,
                        max_lines=1,
                    )
                    ttsmaker_queue = gr.Textbox(
                        label="Queue",
                        interactive=False,
                        visible=False,
                        max_lines=1,
                    )
                    ttsmaker_text_limit = gr.Number(
                        label="Text Characters Limit",
                        value=0.0,
                        interactive=False,
                        visible=False,
                    )

                ttsmaker_sample_audio = gr.Audio(
                    label="Voice Sample",
                    interactive=False,
                    visible=False,
                )

                with gr.Accordion(label="Token Status"):
                    with gr.Row():
                        ttsmaker_token_max = gr.Textbox(
                            label="Max Characters",
                            info="in current cycle",
                            interactive=False,
                            max_lines=1,
                        )
                        ttsmaker_token_used = gr.Textbox(
                            label="Used Characters",
                            info="in current cycle",
                            interactive=False,
                            max_lines=1,
                        )
                        ttsmaker_token_available = gr.Textbox(
                            label="Available Characters",
                            info="in current cycle",
                            interactive=False,
                            max_lines=1,
                        )
                        ttsmaker_token_remaining_days = gr.Textbox(
                            label="Remaining Days",
                            info="to reset quota",
                            interactive=False,
                            max_lines=1,
                        )

                with gr.Accordion(label="Advanced Settings", open=False):
                    ttsmaker_audio_format = gr.Dropdown(
                        label="Audio Format",
                        choices=["mp3", "ogg", "acc", "opus", "wav"],
                        value="mp3",
                        interactive=True,
                    )

                    ttsmaker_audio_speed = gr.Slider(
                        label="Audio Speed",
                        info=r"0.5: 50% speed, 1.0: 100% speed, 2.0: 200% speed",
                        value=1.0,
                        minimum=0.5,
                        maximum=2.0,
                        step=0.5,
                        interactive=True,
                    )

                    ttsmaker_audio_volume = gr.Slider(
                        label="Audio Volume",
                        info="1: volume + 10%, 8: volume + 80%, 10: volume + 100%",
                        value=0.0,
                        minimum=0.0,
                        maximum=10.0,
                        step=1.0,
                        interactive=True,
                    )

                    ttsmaker_text_paragraph_pause_time = gr.Slider(
                        label="Text Paragraph Pause Time",
                        info="""Auto insert audio paragraph pause time. \
                            unit: millisecond, maximum 50 pauses can be inserted. \
                            If more than 50 pauses, all pauses will be canceled automatically. """,
                        value=0,
                        minimum=500,
                        maximum=5000,
                        step=1,
                        interactive=True,
                    )

            with gr.Column():
                ttsmaker_text_input = gr.Textbox(
                    placeholder="Input text here...",
                    lines=7,
                    container=False,
                )
                ttsmaker_left_characters = gr.Markdown(visible=False)
                with gr.Row():
                    ttsmaker_clear_button = gr.ClearButton(value="Clear")
                    ttsmaker_submit_button = gr.Button(value="Submit", variant="primary")
                ttsmaker_audio_output = gr.Audio(label="TTS Result", interactive=False)

    ttsmaker_clear_button.add(
        components=[
            ttsmaker_languages_input,
            ttsmaker_voices_input,
            ttsmaker_gender,
            ttsmaker_queue,
            ttsmaker_text_limit,
            ttsmaker_sample_audio,
            ttsmaker_text_input,
            ttsmaker_left_characters,
            ttsmaker_token_max,
            ttsmaker_token_used,
            ttsmaker_token_available,
            ttsmaker_token_remaining_days,
        ]
    )
    ttsmaker_clear_button.click(
        fn=clear_ttsmaker_info,
        outputs=[ttsmaker_gender, ttsmaker_queue, ttsmaker_text_limit, ttsmaker_sample_audio],
    )

    ttsmaker_token_input.submit(
        fn=check_token_status,
        inputs=[ttsmaker_url_input, ttsmaker_token_input],
        outputs=[ttsmaker_token_max, ttsmaker_token_used, ttsmaker_token_available, ttsmaker_token_remaining_days],
    )

    ttsmaker_languages_input.focus(
        fn=get_ttsmaker_languages,
        inputs=[ttsmaker_url_input, ttsmaker_token_input],
        outputs=ttsmaker_languages_input,
    )

    ttsmaker_voices_input.focus(
        fn=get_ttsmaker_voices,
        inputs=[ttsmaker_url_input, ttsmaker_token_input, ttsmaker_languages_input],
        outputs=ttsmaker_voices_input,
    )

    ttsmaker_voices_input.select(
        fn=get_ttsmaker_single_voice_info,
        inputs=[ttsmaker_url_input, ttsmaker_token_input, ttsmaker_voices_input, ttsmaker_text_input],
        outputs=[ttsmaker_gender, ttsmaker_queue, ttsmaker_text_limit, ttsmaker_sample_audio, ttsmaker_left_characters],
    )

    ttsmaker_text_input.input(
        fn=refresh_characters_limit,
        inputs=[ttsmaker_text_limit, ttsmaker_text_input],
        outputs=ttsmaker_left_characters,
    )

    ttsmaker_submit_button.click(
        fn=create_tts_order,
        inputs=[
            ttsmaker_url_input,
            ttsmaker_token_input,
            ttsmaker_text_input,
            ttsmaker_text_limit,
            ttsmaker_voices_input,
            ttsmaker_audio_format,
            ttsmaker_audio_speed,
            ttsmaker_audio_volume,
            ttsmaker_text_paragraph_pause_time,
        ],
        outputs=ttsmaker_audio_output,
    )
