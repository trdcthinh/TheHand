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
    VALUE_BOOL = 301
    VALUE_STRING = 302
    VALUE_NUMBER = 303
    VALUE_VECTOR = 300


class CommandEventData(TypedDict):
    code: EventCode


class ChangeSceneEventData(TypedDict):
    code: EventCode
    scene: str


class VectorEventData(TypedDict):
    code: EventCode
    x: float
    y: float


class NumberEventData(TypedDict):
    code: EventCode
    value: float


class BoolEventData(TypedDict):
    code: EventCode
    value: bool


class StringEventData(TypedDict):
    code: EventCode
    value: str


def create_quit_event() -> pg.event.Event:
    return pg.event.Event(pg.QUIT, {})


def create_open_menu_event() -> pg.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_OPEN_MENU,
    }
    return pg.event.Event(Event.COMMAND.value, event_data)


def create_next_scene_event() -> pg.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_NEXT_SCENE,
    }
    return pg.event.Event(Event.COMMAND.value, event_data)


def create_change_scene_event(scene: str) -> pg.event.Event:
    event_data: ChangeSceneEventData = {
        "code": EventCode.COMMAND_CHANGE_SCENE,
        "scene": scene,
    }
    return pg.event.Event(Event.COMMAND.value, event_data)


def create_bool_event(value: bool) -> pg.event.Event:
    event_data: BoolEventData = {
        "code": EventCode.VALUE_BOOL,
        "value": value,
    }
    return pg.event.Event(Event.VALUE.value, event_data)


def create_string_event(value: str) -> pg.event.Event:
    event_data: StringEventData = {
        "code": EventCode.VALUE_BOOL,
        "value": value,
    }
    return pg.event.Event(Event.VALUE.value, event_data)


def create_number_event(value: float) -> pg.event.Event:
    event_data: NumberEventData = {
        "code": EventCode.VALUE_NUMBER,
        "value": value,
    }
    return pg.event.Event(Event.VALUE.value, event_data)


def create_vector_event(x: float, y: float) -> pg.event.Event:
    event_data: VectorEventData = {
        "code": EventCode.VALUE_VECTOR,
        "x": x,
        "y": y,
    }
    return pg.event.Event(Event.VALUE.value, event_data)
