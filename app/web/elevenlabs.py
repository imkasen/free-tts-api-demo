"""
ElevenLabs Gradio UI
"""
import gradio as gr
from logic.elevenlabs import (
    clear_elevenlabs_info,
    get_elevenlabs_audio,
    get_elevenlabs_single_voice_info,
    get_elevenlabs_token_status,
    get_elevenlabs_voices,
)

# pylint: disable=E1101

with gr.Tab(label="ElevenLabs"):
    with gr.Row():
        with gr.Column(variant="panel"):
            elevenlabs_token_input = gr.Textbox(
                label="API Token",
                info="Fill in your xi-api-key here. Press Enter to get token status.",
                interactive=True,
                max_lines=1,
                type="password",
            )

            elevenlabs_model = gr.Radio(
                label="Model",
                choices=["eleven_multilingual_v2"],
                value="eleven_multilingual_v2",
                interactive=False,
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

            with gr.Accordion(label="Token Status", open=True):
                with gr.Row():
                    elevenlabs_used_characters = gr.Textbox(
                        label="Count",
                        info="used characters",
                        max_lines=1,
                        interactive=False,
                    )
                    elevenlabs_characters_left = gr.Textbox(
                        label="Available",
                        info="remaining characters",
                        max_lines=1,
                        interactive=False,
                    )
                    elevenlabs_characters_limit = gr.Textbox(
                        label="Limit",
                        info="character limit",
                        max_lines=1,
                        interactive=False,
                    )
                    elevenlabs_characters_reset_time = gr.Textbox(
                        label="Time",
                        info="quota reset time (UTC)",
                        max_lines=1,
                        interactive=False,
                    )

            with gr.Accordion(label="Voice Settings", open=False):
                elevenlabs_stability = gr.Slider(
                    label="Stability",
                    info="""How stable the voice is.
                        Lowering this slider introduces a broader emotional range for the voice.
                        Setting it too high can lead to a monotonous voice with limited emotion.""",
                    value=0.71,
                    minimum=0.0,
                    maximum=1.0,
                    interactive=True,
                )
                elevenlabs_similarity = gr.Slider(
                    label="Similarity",
                    info="How closely the AI should adhere to the original voice when attempting to replicate it.",
                    value=0.5,
                    minimum=0.0,
                    maximum=1.0,
                    interactive=True,
                )
                elevenlabs_style = gr.Slider(
                    label="Style Exaggeration",
                    info="""It attempts to amplify the style of the original speaker.
                        It does consume additional computational resources and
                        might increase latency if set to anything other than 0.
                        In general, we recommend keeping this setting at 0 at all times.""",
                    value=0.0,
                    minimum=0.0,
                    maximum=1.0,
                    interactive=True,
                )
                elevenlabs_spaker_boost = gr.Radio(
                    label="Speaker Boost",
                    info="""It boosts the similarity to the original speaker.
                        It requires a slightly higher computational load,
                        which in turn increases latency.""",
                    choices=["True", "False"],
                    value="True",
                    interactive=True,
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

elevenlabs_token_input.submit(
    fn=get_elevenlabs_token_status,
    inputs=elevenlabs_token_input,
    outputs=[
        elevenlabs_used_characters,
        elevenlabs_characters_left,
        elevenlabs_characters_limit,
        elevenlabs_characters_reset_time,
    ],
)

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

elevenlabs_submit_button.click(
    fn=get_elevenlabs_audio,
    inputs=[
        elevenlabs_token_input,
        elevenlabs_text_input,
        elevenlabs_voices_input,
        elevenlabs_model,
        elevenlabs_stability,
        elevenlabs_similarity,
        elevenlabs_style,
        elevenlabs_spaker_boost,
    ],
    outputs=elevenlabs_audio_output,
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
        elevenlabs_used_characters,
        elevenlabs_characters_left,
        elevenlabs_characters_limit,
        elevenlabs_characters_reset_time,
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
