import pygame as pg

from .types import TheHandEventData

THEHAND_EVENT = pg.USEREVENT + 79

C_OPEN_MENU = 101
C_NEXT_SCENE = 105
C_CHANGE_SCENE = 106
C_BOOL = 301
C_STRING = 302
C_NUMBER = 303
C_VECTOR = 300


def create_quit_event() -> pg.event.Event:
    return pg.event.Event(pg.QUIT, {})


def create_open_menu_event() -> pg.event.Event:
    event_data: TheHandEventData = {"code": C_OPEN_MENU, "value": ""}
    return pg.event.Event(THEHAND_EVENT, event_data)


def create_next_scene_event() -> pg.event.Event:
    event_data: TheHandEventData = {"code": C_NEXT_SCENE, "value": ""}
    return pg.event.Event(THEHAND_EVENT, event_data)


def create_change_scene_event(scene: str) -> pg.event.Event:
    event_data: TheHandEventData = {
        "code": C_CHANGE_SCENE,
        "value": scene,
    }
    return pg.event.Event(THEHAND_EVENT, event_data)


def create_bool_event(value: bool) -> pg.event.Event:
    event_data: TheHandEventData = {
        "code": C_BOOL,
        "value": value,
    }
    return pg.event.Event(THEHAND_EVENT, event_data)


def create_string_event(value: str) -> pg.event.Event:
    event_data: TheHandEventData = {
        "code": C_STRING,
        "value": value,
    }
    return pg.event.Event(THEHAND_EVENT, event_data)


def create_number_event(value: float) -> pg.event.Event:
    event_data: TheHandEventData = {
        "code": C_NUMBER,
        "value": value,
    }
    return pg.event.Event(THEHAND_EVENT, event_data)


def create_vector_event(vec: tuple[float, float]) -> pg.event.Event:
    event_data: TheHandEventData = {"code": C_VECTOR, "value": vec}
    return pg.event.Event(THEHAND_EVENT, event_data)
