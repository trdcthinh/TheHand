def print_one_line(text: str) -> None:
    print(f"\r{' ' * 80}\r{text[-80:].ljust(80)}", end="", flush=True)
