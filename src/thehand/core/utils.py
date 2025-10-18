import random
import os

NOISE_CHARS = "#@$%█▓▒░■—–︱●○◆▪…?|aeiou"


def asset_path(rel_path: str) -> str:
    return os.path.join("data", rel_path)


def print_inline(text: str) -> None:
    print(f"\r{' ' * 80}\r{text[-80:].ljust(80)}", end="", flush=True)


def generate_noise_string(length: int = 15) -> str:
    random_chars = random.choices(NOISE_CHARS, k=length)

    noise = "".join(random_chars)

    return noise


def main():
    print(f"Length 8: {generate_noise_string(8)}")
    print(f"Length 15: {generate_noise_string()}")
    print(f"Length 30: {generate_noise_string(length=30)}")


if __name__ == "__main__":
    main()
