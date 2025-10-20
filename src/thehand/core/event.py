from enum import Enum
from typing import TypedDict

import pygame as pg


class Event(Enum):
    COMMAND = pg.USEREVENT + 1
    VALUE = pg.USEREVENT + 2


class EventCode(Enum):
    COMMAND_OPEN_MENU = 101
    COMMAND_NEXT_SCENE = 105
    COMMAND_CHANGE_SCENE = 106
    VALUE_NUMBER = 303
    VALUE_VECTOR = 300


class CommandEventData(TypedDict):
    code: EventCode
    value: str


class ValueVectorEventData(TypedDict):
    code: EventCode
    x: float
    y: float


class ValueNumberEventData(TypedDict):
    code: EventCode
    value: float


def create_quit_event() -> pg.event.Event:
    return pg.event.Event(pg.QUIT, {})


def create_open_menu_event() -> pg.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_OPEN_MENU,
        "value": "",
    }
    return pg.event.Event(Event.COMMAND.value, event_data)


def create_next_scene_event() -> pg.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_NEXT_SCENE,
        "value": "",
    }
    return pg.event.Event(Event.COMMAND.value, event_data)


def create_change_scene_event(value: str = "") -> pg.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_CHANGE_SCENE,
        "value": value,
    }
    return pg.event.Event(Event.COMMAND.value, event_data)


def create_vector_event(x: float, y: float) -> pg.event.Event:
    event_data: ValueVectorEventData = {
        "code": EventCode.VALUE_VECTOR,
        "x": x,
        "y": y,
    }
    return pg.event.Event(Event.VALUE.value, event_data)


def create_number_event(value: float) -> pg.event.Event:
    event_data: ValueNumberEventData = {
        "code": EventCode.VALUE_NUMBER,
        "value": value,
    }
    return pg.event.Event(Event.VALUE.value, event_data)
