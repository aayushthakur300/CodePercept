import json
import re

def extract_json_from_text(text: str):
    """
    Safely extract the FIRST valid JSON object from an AI response.
    Matches the behavior of your Node.js extractJSON() function.
    """

    if not text or not isinstance(text, str):
        return None

    # Remove markdown/fence style: ```json ... ```
    cleaned = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "")
    cleaned = cleaned.strip()

    # Find first '{'
    start = cleaned.find("{")
    if start == -1:
        return None

    depth = 0
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = cleaned[start:i+1]
                try:
                    return json.loads(candidate)
                except Exception:
                    return None

    return None
