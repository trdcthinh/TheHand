import threading
import time
from enum import Enum
from typing import TypedDict

import pygame


class Event(Enum):
    COMMAND = pygame.USEREVENT + 1
    CONTROL = pygame.USEREVENT + 2


class EventCode(Enum):
    COMMAND_OPEN_MENU = 101
    COMMAND_NEXT_SCENE = 105
    CONTROL_NUMBER = 303
    CONTROL_VECTOR = 300


class CommandEventData(TypedDict):
    code: EventCode
    message: str


class ControlVectorEventData(TypedDict):
    code: EventCode
    x: float
    y: float


class ControlIntEventData(TypedDict):
    code: EventCode
    value: float


def create_open_menu_event(message: str = "") -> pygame.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_OPEN_MENU,
        "message": message,
    }
    return pygame.event.Event(Event.COMMAND.value, event_data)


def create_next_scene_event(message: str = "") -> pygame.event.Event:
    event_data: CommandEventData = {
        "code": EventCode.COMMAND_NEXT_SCENE,
        "message": message,
    }
    return pygame.event.Event(Event.COMMAND.value, event_data)


def create_vector_event(x: float, y: float) -> pygame.event.Event:
    event_data: ControlVectorEventData = {
        "code": EventCode.CONTROL_VECTOR,
        "x": x,
        "y": y,
    }
    return pygame.event.Event(Event.CONTROL.value, event_data)


def create_number_event(value: float) -> pygame.event.Event:
    event_data: ControlIntEventData = {
        "code": EventCode.CONTROL_NUMBER,
        "value": value,
    }
    return pygame.event.Event(Event.CONTROL.value, event_data)


def audition_thread_function():
    time.sleep(2)
    pygame.event.post(create_open_menu_event("Now, open menu"))
    time.sleep(2)
    pygame.event.post(create_next_scene_event("Now, next scene"))
    time.sleep(2)
    pygame.event.post(create_number_event(999))
    time.sleep(2)
    pygame.event.post(create_vector_event(1, -1))


def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()

    running = True

    audition_thread = threading.Thread(target=audition_thread_function)
    audition_thread.daemon = True
    audition_thread.start()

    last_event: str = ""
    message: str = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == Event.COMMAND.value or event.type == Event.CONTROL.value:
                print(f"Custom event: {event}")
                last_event = event.code.name

            if event.type == Event.COMMAND.value:
                message = event.message

            if event.type == Event.CONTROL.value:
                if event.code == EventCode.CONTROL_NUMBER:
                    message = f"{event.value}"
                if event.code == EventCode.CONTROL_VECTOR:
                    message = f"({event.x}, {event.y})"

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Last event:\n{last_event}\n{message}", True, (0, 255, 0))
        screen.blit(text, (50, 50))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
