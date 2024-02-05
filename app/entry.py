"""
Project entry file
"""
import os
from pathlib import Path

from loguru import logger
from web import ui

logger.add(
    sink=os.path.join(Path().resolve(), "logs", "{time:YYYY-MM-DD}.log"),
    format="{time:YYYY-MM-DD HH:mm::ss} | {level} | {name} | {file.path}:{line} | {function} | {message}",
    encoding="utf-8",
    enqueue=True,
    rotation="00:00",
    retention="1 week",
)

if __name__ == "__main__":
    ui.queue().launch(
        inbrowser=True,
        show_api=False,
        share=False,
    )
