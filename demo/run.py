"""
Project entry file
"""
from web import demo

if __name__ == "__main__":
    demo.queue().launch(
        inbrowser=True,
        show_api=False,
        share=False,
    )
