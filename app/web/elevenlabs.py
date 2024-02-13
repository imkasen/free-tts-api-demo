"""
ElevenLabs Gradio UI
"""
import gradio as gr
from logic.elevenlabs import clear_elevenlabs_info, get_elevenlabs_single_voice_info, get_elevenlabs_voices

# pylint: disable=E1101

with gr.Tab(label="ElevenLabs"):
    with gr.Row():
        with gr.Column(variant="panel"):
            elevenlabs_token_input = gr.Textbox(
                label="API Token",
                info="Enter your xi-api-key here.",
                interactive=True,
                max_lines=1,
                type="password",
            )
            elevenlabs_voices_input = gr.Dropdown(
                label="Voices",
                info="Select a speaker voice you want to use.",
                interactive=True,
            )

            with gr.Row():
                elevenlabs_gender = gr.Textbox(
                    label="Gender",
                    interactive=False,
                    max_lines=1,
                    visible=False,
                )
                elevenlabs_accent = gr.Textbox(
                    label="Accent",
                    interactive=False,
                    max_lines=1,
                    visible=False,
                )
                elevenlabs_age = gr.Textbox(
                    label="Age",
                    interactive=False,
                    max_lines=1,
                    visible=False,
                )
            with gr.Row():
                elevenlabs_description = gr.Textbox(
                    label="Description",
                    interactive=False,
                    max_lines=1,
                    visible=False,
                )
                elevenlabs_usecase = gr.Textbox(
                    label="Use Case",
                    interactive=False,
                    max_lines=1,
                    visible=False,
                )
            with gr.Row():
                elevenlabs_sample_audio = gr.Audio(
                    label="Preview Sample",
                    interactive=False,
                    visible=False,
                )

        with gr.Column():
            elevenlabs_text_input = gr.Textbox(
                placeholder="Input text here...",
                lines=7,
                container=False,
                interactive=True,
            )
            with gr.Row():
                elevenlabs_clear_button = gr.ClearButton(value="Clear")
                elevenlabs_submit_button = gr.Button(value="Submit", variant="primary")
            elevenlabs_audio_output = gr.Audio(label="TTS Result", type="numpy", format="mp3", interactive=False)

elevenlabs_voices_input.focus(
    fn=get_elevenlabs_voices,
    outputs=elevenlabs_voices_input,
)

elevenlabs_voices_input.select(
    fn=get_elevenlabs_single_voice_info,
    inputs=elevenlabs_voices_input,
    outputs=[
        elevenlabs_gender,
        elevenlabs_accent,
        elevenlabs_age,
        elevenlabs_description,
        elevenlabs_usecase,
        elevenlabs_sample_audio,
    ],
)

elevenlabs_clear_button.add(
    components=[
        elevenlabs_voices_input,
        elevenlabs_gender,
        elevenlabs_accent,
        elevenlabs_age,
        elevenlabs_description,
        elevenlabs_usecase,
        elevenlabs_sample_audio,
        elevenlabs_text_input,
        elevenlabs_audio_output,
    ]
)

elevenlabs_clear_button.click(
    fn=clear_elevenlabs_info,
    outputs=[
        elevenlabs_gender,
        elevenlabs_accent,
        elevenlabs_age,
        elevenlabs_description,
        elevenlabs_usecase,
        elevenlabs_sample_audio,
    ],
)
