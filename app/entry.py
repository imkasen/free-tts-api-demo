"""
Project entry file
"""
from web import ui

if __name__ == "__main__":
    ui.queue().launch(
        inbrowser=True,
        show_api=False,
        share=False,
    )
