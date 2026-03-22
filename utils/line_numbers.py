# utils/line_numbers.py
def add_line_numbers(raw_code: str) -> str:
    if raw_code is None:
        return ""
    lines = raw_code.splitlines()
    return "\n".join(f"{i+1} | {line}" for i, line in enumerate(lines))
