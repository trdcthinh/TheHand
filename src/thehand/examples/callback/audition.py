import pygame as pg

from thehand.core.event import create_next_scene_event
from thehand.core.utils import print_inline


def sr_next_scene_callback(text: str) -> None:
    print_inline(text)

    if "next" in text.lower():
        pg.event.post(create_next_scene_event())


def sr_close_callback(text: str) -> None:
    print_inline(text)

    if "close" in text.lower():
        pg.event.post(pg.event.Event(pg.QUIT, {}))
