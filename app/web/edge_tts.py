"""
Edge TTS Gradio UI
"""
import gradio as gr
from logic.edgetts import (
    clear_edgetts_info,
    get_edgetts_audio,
    get_edgetts_language_code,
    get_edgetts_single_voice_info,
    get_edgetts_voices,
)

# pylint: disable=E1101

with gr.Tab(label="Edge TTS"):
    with gr.Row():
        with gr.Column(variant="panel"):
            edgetts_language_code = gr.Dropdown(
                label="Language Code",
                info="Select the language code you want to use.",
                interactive=True,
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

edgetts_language_code.focus(
    fn=get_edgetts_language_code,
    outputs=edgetts_language_code,
)

edgetts_voices_input.focus(
    fn=get_edgetts_voices,
    inputs=edgetts_language_code,
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
        edgetts_language_code,
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
