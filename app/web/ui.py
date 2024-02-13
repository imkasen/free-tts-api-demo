"""
User Interface
"""
import gradio as gr

# Gradio UI
with gr.Blocks(title="Free TTS API Demo") as ui:
    gr.HTML(value="""<h1 align="center">Free TTS API Demo</h1>""")

    # pylint: disable=W0611
    # Edge TTS
    from . import edge_tts  # isort: skip

    # ElevenLabs
    from . import elevenlabs  # isort: skip

    # TTS Maker
    from . import ttsmaker  # isort: skip
