import random

import pygame as pg
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult

from thehand.core import HandLandmarker, Scene, State, Store, asset_path
from thehand.core.event import Event, EventCode, create_vector_event
from thehand.core.store import COLOR_MOCHA_BASE, COLOR_MOCHA_GREEN
from thehand.core.vision import get_hand_position_on_screen
from thehand.game.widgets.toast import Toast


class Collectible(pg.sprite.Sprite):
    def __init__(self, image_path, pos, points, size=(50, 50)):
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=pos)
        self.points = points


class Apple(Collectible):
    def __init__(self, pos):
        size_points = random.choices(
            [(50, 1), (80, 10), (120, 50), (150, 200), (300, 1000)], [50, 20, 10, 5, 1]
        )
        size = size_points[0][0]
        points = size_points[0][1]
        super().__init__(asset_path("imgs", "apple.png"), pos, points, (size, size))


class Strawberry(Collectible):
    def __init__(self, pos):
        size_points = random.choices(
            [(50, 5), (80, 50), (120, 200), (150, 1000), (300, 5000)],
            [50, 20, 10, 5, 1],
        )
        size = size_points[0][0]
        points = size_points[0][1] * 2
        super().__init__(
            asset_path("imgs", "strawberry.png"), pos, points, (size, size)
        )


class PacmanScene(Scene):
    def __init__(
        self,
        name: str,
        state: State,
        store: Store,
        hand: HandLandmarker,
    ):
        super().__init__(name, state, store)

        self.hand = hand

        self.pacman = pg.image.load(
            asset_path("imgs", "pacman_right.png")
        ).convert_alpha()
        self.pacman = pg.transform.scale(self.pacman, (150, 150))

        self.pacman_pos = pg.Vector2(
            self.store.screen.get_width() / 2, self.store.screen.get_height() / 2
        )
        self.pacman_target_pos = pg.Vector2(
            self.store.screen.get_width() / 2, self.store.screen.get_height() / 2
        )
        self.easing = 0.1

        self.score = 0
        self.collectibles = pg.sprite.Group()
        self._spawn_margin = int(0.2 * self.state.window_size[1])
        self._spawn_initial_collectibles()

        self.toasts: list[Toast] = []

    def _spawn_collectible(self, collectible_type):
        pos = (
            random.randint(
                self._spawn_margin, self.state.window_size[0] - self._spawn_margin
            ),
            random.randint(
                self._spawn_margin, self.state.window_size[1] - self._spawn_margin
            ),
        )
        collectible = collectible_type(pos)
        self.collectibles.add(collectible)

    def _spawn_initial_collectibles(self):
        for _ in range(5):
            self._spawn_collectible(Apple)
        for _ in range(2):
            self._spawn_collectible(Strawberry)

    def setup(self):
        self.hand.set_result_callback(self._hand_result_callback)

    def handle_events(self):
        for event in self.state.events:
            if event.type == Event.VALUE.value:
                if event.code == EventCode.VALUE_VECTOR:
                    self.pacman_target_pos.x = event.x
                    self.pacman_target_pos.y = event.y

    def update(self):
        self.pacman_pos.x += (
            self.pacman_target_pos.x - self.pacman_pos.x
        ) * self.easing
        self.pacman_pos.y += (
            self.pacman_target_pos.y - self.pacman_pos.y
        ) * self.easing

        pacman_sprite = pg.sprite.Sprite()
        pacman_sprite.rect = self.pacman.get_rect(center=self.pacman_pos)

        collided_collectibles = pg.sprite.spritecollide(
            pacman_sprite, self.collectibles, True
        )
        for collectible in collided_collectibles:
            self.score += collectible.points
            toast = Toast(
                collectible.rect.centerx,
                collectible.rect.centery,
                100,
                50,
                self.state,
                f"+ {collectible.points}",
                1000,
                color=COLOR_MOCHA_BASE,
                bg_color=COLOR_MOCHA_GREEN,
            )
            toast.show()
            self.toasts.append(toast)
            self._spawn_collectible(type(collectible))

        for toast in self.toasts:
            toast.update()
        self.toasts = [
            toast for toast in self.toasts if toast.animation_state != "HIDDEN"
        ]

    def render(self):
        self.store.screen.fill((25, 25, 25))

        self.collectibles.draw(self.store.screen)

        self.store.screen.blit(
            self.pacman, self.pacman.get_rect(center=self.pacman_pos)
        )

        score_text = self.store.font_text_24.render(
            f"Score: {self.score}", True, (240, 240, 240)
        )
        self.store.screen.blit(score_text, (10, 10))

        for toast in self.toasts:
            toast.render(self.store.screen)

        pg.display.flip()

    def _hand_result_callback(self, result: HandLandmarkerResult) -> None:
        if not result.hand_world_landmarks or len(result.hand_world_landmarks) <= 0:
            return

        hand_landmarks = result.hand_landmarks

        for i, normalized_landmarks in enumerate(hand_landmarks):
            if len(normalized_landmarks) < 21:
                continue

            pos = get_hand_position_on_screen(
                normalized_landmarks,
                self.state.window_size[0],
                self.state.window_size[1],
            )

            if pos is None:
                continue

            pg.event.post(create_vector_event(pos[0], pos[1]))
