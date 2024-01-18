"""
User Interface
"""
import gradio as gr

from .ui_logic import get_ttsmaker_languages

# Gradio UI
with gr.Blocks(title="Free TTS API Demo") as demo:
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
                ttsmaker_url_input = gr.Dropdown(
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
                    ttsmaker_queue = gr.Textbox(value="False", label="Queue", interactive=False)
                    ttsmaker_gender = gr.Textbox(value="Male", label="Gender", interactive=False)
                    ttsmaker_txt_limit = gr.Textbox(value="3000", label="Text characters limit", interactive=False)

                ttsmaker_sample_audio = gr.Audio(label="Voice Sample", interactive=False)

                with gr.Row():
                    ttsmaker_clear_button = gr.ClearButton(value="Clear")
                    ttsmaker_submit_button = gr.Button(value="Submit", variant="primary")

            with gr.Column():
                ttsmaker_audio_output = gr.Audio(label="TTS Result", interactive=False)

    ttsmaker_languages_input.focus(  # pylint: disable=E1101
        fn=get_ttsmaker_languages,
        inputs=[ttsmaker_url_input, ttsmaker_token_input],
        outputs=ttsmaker_languages_input,
    )
