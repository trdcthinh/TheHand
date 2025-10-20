import threading
import time

import pygame as pg

from thehand.core import Event, EventCode
from thehand.core.event import (
    create_next_scene_event,
    create_number_event,
    create_open_menu_event,
    create_vector_event,
)


def audition_thread_function():
    time.sleep(2)
    pg.event.post(create_open_menu_event())
    time.sleep(2)
    pg.event.post(create_next_scene_event())
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
    value: str = ""

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == Event.COMMAND.value or event.type == Event.VALUE.value:
                print(f"Custom event: {event}")
                last_event = event.code.name

            if event.type == Event.COMMAND.value:
                value = event.value

            if event.type == Event.VALUE.value:
                if event.code == EventCode.VALUE_NUMBER:
                    value = f"{event.value}"
                if event.code == EventCode.VALUE_VECTOR:
                    value = f"({event.x}, {event.y})"

        screen.fill((0, 0, 0))
        font = pg.font.Font(None, 36)
        text = font.render(f"Last event:\n{last_event}\n{value}", True, (0, 255, 0))
        screen.blit(text, (50, 50))
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
