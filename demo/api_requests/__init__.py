"""
API requests module
"""
import os
from pathlib import Path

from loguru import logger

from .ttsmaker import TTSMaker

PROJ_ROOT: str = Path().resolve()

logger.add(
    sink=os.path.join(PROJ_ROOT, "logs", "{time}.log"),
    format="{time:YYYY-MM-DD HH:mm::ss} | {level} | {message}",
    encoding="utf-8",
    enqueue=True,
    rotation="00:00",
    retention="1 week",
)
