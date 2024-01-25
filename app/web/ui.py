"""
User Interface
"""
import gradio as gr

from .ui_logic import clear_ttsmaker_info, get_ttsmaker_languages, get_ttsmaker_single_voice_info, get_ttsmaker_voices

# Gradio UI
with gr.Blocks(title="Free TTS API Demo") as ui:
    gr.HTML(value="""<h1 align="center">Free TTS API Demo</h1>""")
    # TTS Maker
    with gr.Tab(label="TTSMaker"):
        with gr.Row():
            with gr.Column(variant="panel"):
                ttsmaker_token_input = gr.Textbox(
                    label="Token",
                    value="ttsmaker_demo_token",
                    interactive=True,
                )
                ttsmaker_url_input = gr.Radio(
                    label="API URL",
                    info="Select TTSMaker API url based on your localtion.",
                    choices=["api.ttsmaker.com", "api.ttsmaker.cn"],
                    value="api.ttsmaker.com",
                    interactive=True,
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
                    )
                    ttsmaker_queue = gr.Textbox(
                        label="Queue",
                        interactive=False,
                        visible=False,
                    )
                    ttsmaker_txt_limit = gr.Textbox(
                        label="Text Characters Limit",
                        interactive=False,
                        visible=False,
                    )

                ttsmaker_sample_audio = gr.Audio(
                    label="Voice Sample",
                    interactive=False,
                    visible=False,
                )

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

                ttsmaker_text_pause_time = gr.Slider(
                    label="Text Paragraph Pause Time",
                    info="""Auto insert audio paragraph pause time. \
                        unit: second, maximum 50 pauses can be inserted. \
                        If more than 50 pauses, all pauses will be canceled automatically. """,
                    value=0.0,
                    minimum=0.5,
                    maximum=5.0,
                    step=0.1,
                    interactive=True,
                )

            with gr.Column():
                ttsmaker_text_input = gr.Textbox(placeholder="Input text here...", container=False)
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
            ttsmaker_txt_limit,
            ttsmaker_sample_audio,
        ]
    )
    ttsmaker_clear_button.click(  # pylint: disable=E1101
        fn=clear_ttsmaker_info,
        outputs=[ttsmaker_gender, ttsmaker_queue, ttsmaker_txt_limit, ttsmaker_sample_audio],
    )

    ttsmaker_languages_input.focus(  # pylint: disable=E1101
        fn=get_ttsmaker_languages,
        inputs=[ttsmaker_url_input, ttsmaker_token_input],
        outputs=ttsmaker_languages_input,
    )

    ttsmaker_voices_input.focus(  # pylint: disable=E1101
        fn=get_ttsmaker_voices,
        inputs=[ttsmaker_url_input, ttsmaker_token_input, ttsmaker_languages_input],
        outputs=ttsmaker_voices_input,
    )

    ttsmaker_voices_input.select(  # pylint: disable=E1101
        fn=get_ttsmaker_single_voice_info,
        inputs=[ttsmaker_url_input, ttsmaker_token_input, ttsmaker_voices_input],
        outputs=[ttsmaker_gender, ttsmaker_queue, ttsmaker_txt_limit, ttsmaker_sample_audio],
    )
