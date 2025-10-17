import pygame as pg

from thehand.core.event import create_next_scene_event


def sr_hello_callback(text: str) -> None:
    print(f"\r{' ' * 80}\r{text.ljust(80)}", end="", flush=True)

    if "hello" in text.lower():
        print(f"\r{' ' * 80}\rRequest next scene", end="", flush=True)
        pg.event.post(create_next_scene_event())


def sr_close_callback(text: str) -> None:
    print(f"\r{' ' * 80}\r{text.ljust(80)}", end="", flush=True)

    if "close" in text.lower():
        print(f"\r{' ' * 80}\rRequest next scene", end="", flush=True)
        pg.event.post(create_next_scene_event())
