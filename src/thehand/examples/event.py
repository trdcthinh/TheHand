import threading
import time

import pygame as pg

import thehand as th


def audition_thread_function():
    time.sleep(2)
    pg.event.post(th.create_open_menu_event())
    time.sleep(2)
    pg.event.post(th.create_next_scene_event())
    time.sleep(2)
    pg.event.post(th.create_number_event(999))
    time.sleep(2)
    pg.event.post(th.create_vector_event((1, -1)))


def main():
    pg.init()

    screen = pg.display.set_mode((400, 300))
    clock = pg.time.Clock()

    running = True

    audition_thread = threading.Thread(target=audition_thread_function)
    audition_thread.daemon = True
    audition_thread.start()

    last_code = None
    last_value: str = ""

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == th.THEHAND_EVENT:
                print(f"TheHand event: {event}")
                last_code = event.code
                last_value = event.value

        screen.fill((0, 0, 0))
        font = pg.font.Font(None, 36)
        text = font.render(f"Last event: {last_code}\nLast value: {last_value}", True, (0, 255, 0))
        screen.blit(text, (50, 50))
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
