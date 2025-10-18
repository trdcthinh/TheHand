# GEMINI.md - Project Overview

This document provides an overview of the project structure and key components for the Gemini CLI.

## Project Context

This project is a Pygame-based game that integrates speech recognition and computer vision to create a unique gameplay experience.

*   **Game Engine:** Pygame
*   **Speech Recognition:** Moonshine ONNX
*   **Computer Vision:** MediaPipe (Hand, Face, and Pose Landmarkers)

## Project Structure

The project is organized into the following main directories:

*   `data/`: Contains all game assets.
    *   `audio/`: Sound effects and music.
    *   `fonts/`: Font files for in-game text.
    *   `imgs/`: Images and graphics used in the game.
*   `models/`: Stores the machine learning models.
    *   `face_landmarker.task`: MediaPipe model for face landmark detection.
    *   `hand_landmarker.task`: MediaPipe model for hand landmark detection.
    *   `pose_landmarker.task`: MediaPipe model for pose landmark detection.
*   `showcase/`: Scripts for demonstrating project features.
    *   `development.py`: Script for development and testing purposes.
    *   `production.py`: Script for running the production version of the game.
*   `src/`: Contains the main source code for the project.
    *   `thehand/`: The main Python package.
        *   `core/`: Core functionalities of the game engine.
            *   `audition/`: Speech recognition components.
            *   `scene/`: Scene management system.
            *   `vision/`: Computer vision components (camera, landmarkers).
        *   `examples/`: Standalone examples for different project modules.
        *   `game/`: The main game logic and scenes.
            *   `scene/`: Game-specific scenes.
                *   `common/`: Scenes like main menu and tutorials.
                *   `decor/`: Decorative or transitional scenes (splash, credits).
                *   `level/`: The actual game levels.

## Development Status

The core framework for the game is in place. However, some features are still under development:

*   **Completed:**
    *   Speech Recognition integration.
    *   Hand Landmarker utility.
*   **In Progress:**
    *   Pose Landmarker utility.
    *   Face Landmarker utility.

This structure is designed to be modular, allowing for easy extension and maintenance.
