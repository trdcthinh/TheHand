import threading
import time
from enum import Enum
from typing import TypedDict

import pygame as pg


class Event(Enum):
    COMMAND = pg.USEREVENT + 1
    VALUE = pg.USEREVENT + 2


class EventCode(Enum):
    COMMAND_OPEN_MENU = 101
    COMMAND_NEXT_SCENE = 105
    VALUE_NUMBER = 303
    VALUE_VECTOR = 300


class CommandEventData(TypedDict):
    code: EventCode
    message: str


class ValueVectorEventData(TypedDict):
    code: EventCode
    x: float
    y: float


class ValueNumberEventData(TypedDict):
    code: EventCode
    value: float


def create_quit_event() -> pg.event.Event:
    return pg.event.Event(pg.QUIT, {})


def create_open_menu_event(message: str = "") -> pg.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_OPEN_MENU,
        "message": message,
    }
    return pg.event.Event(Event.COMMAND.value, event_data)


def create_next_scene_event(message: str = "") -> pg.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_NEXT_SCENE,
        "message": message,
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


def audition_thread_function():
    time.sleep(2)
    pg.event.post(create_open_menu_event("Now, open menu"))
    time.sleep(2)
    pg.event.post(create_next_scene_event("Now, next scene"))
    time.sleep(2)
    pg.event.post(create_number_event(999))
    time.sleep(2)
    pg.event.post(create_vector_event(1, -1))


def main():
    pg.init()

    screen = pg.display.set_mode((400, 300))
    clock = pg.time.Clock()

    running = True

    audition_thread = threading.Thread(target=audition_thread_function)
    audition_thread.daemon = True
    audition_thread.start()

    last_event: str = ""
    message: str = ""

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == Event.COMMAND.value or event.type == Event.VALUE.value:
                print(f"Custom event: {event}")
                last_event = event.code.name

            if event.type == Event.COMMAND.value:
                message = event.message

            if event.type == Event.VALUE.value:
                if event.code == EventCode.VALUE_NUMBER:
                    message = f"{event.value}"
                if event.code == EventCode.VALUE_VECTOR:
                    message = f"({event.x}, {event.y})"

        screen.fill((0, 0, 0))
        font = pg.font.Font(None, 36)
        text = font.render(f"Last event:\n{last_event}\n{message}", True, (0, 255, 0))
        screen.blit(text, (50, 50))
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
