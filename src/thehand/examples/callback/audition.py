import pygame as pg

import thehand as th


def sr_next_scene_callback(text: str) -> None:
    th.print_inline(text)

    if "next" in text.lower():
        pg.event.post(th.create_next_scene_event())


def sr_close_callback(text: str) -> None:
    th.print_inline(text)

    if "close" in text.lower():
        pg.event.post(pg.event.Event(pg.QUIT, {}))
