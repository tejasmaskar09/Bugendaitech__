import re
import math
from sympy import sympify
from sympy.core.sympify import SympifyError

_CONVERSATIONAL_PHRASES = {
    "hi", "hello", "how are you", "what's up", "good morning", "good evening",
    "good afternoon", "hey", "tell me about yourself", "who are you", "can you hear me",
    "how do you do", "what is your name", "are you there"
}

_BANNED_KEYWORDS = {
    "violence", "abuse", "hate", "racism", "sexism", "drugs", "alcohol", "porn",
    "nude", "kill", "murder", "gun", "knife", "bomb", "suicide", "rape", "molest",
    "nsfw", "onlyfans", "torture", "sniper", "snuff", "terror", "incest", "gore"
}

def filter_conversational_prompts(text: str) -> str:
    q = text.lower().strip()
    if q in _CONVERSATIONAL_PHRASES:
        return ""
    for phrase in _CONVERSATIONAL_PHRASES:
        if q.startswith(phrase) and len(q) < len(phrase) + 10:
            return ""
    return text

def safe_prompt_filter(prompt: str) -> str:
    if not prompt.strip():
        return "[BLOCKED EMPTY INPUT]"
    if any(word in prompt.lower() for word in _BANNED_KEYWORDS):
        return "[BLOCKED UNSAFE INPUT]"
    return prompt

def get_prompt_type(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["code", "function", "write a program of", "generate code", "script"]):
        return "code"
    if any(w in q for w in [
        "capital of", "currency of", "population of", "where is", "who is",
        "speed of", "length of", "when did", "founded in", "area of", "height of",
        "what is the time", "time in"
    ]):
        return "factual"
    if any(w in q for w in [
        "solve", "calculate", "evaluate", "find the value", "perimeter", "volume", "area",
        "lcm", "hcf", "add", "subtract", "multiply", "divide", "log", "mean", "median",
        "mode", "integral", "derivative", "matrix", "factorial", "equation", "square root",
        "probability", "%"
    ]):
        return "math"
    return "concept"

def solve_basic_math_expression(query: str) -> str | None:
    q = query.lower().strip()
    match = re.search(r"(\d+(\.\d+)?)%\s*(of)?\s*(\d+(\.\d+)?)", q)
    if match:
        percent = float(match.group(1))
        base = float(match.group(4))
        result = (percent / 100) * base
        return (
            f"{percent}% of {base}:\n"
            f"{percent} ÷ 100 = {percent / 100:.2f}\n"
            f"{percent / 100:.2f} × {base} = {result:.2f}"
        )
    return None

def solve_geometry_expression(query: str) -> str | None:
    q = query.lower().strip()

   
    # Square area
    if match := re.search(r"(?:area of )?square.*?(?:side|sides|length)\s*(?:is\s*)?(\d+(\.\d+)?)", q):
        s = float(match.group(1))
        area = s * s
        return f"Area of square = {s} × {s} = {area:.2f} square units"

    # Rectangle area (also catch 'bredth' typo)
    if match := re.search(
        r"area of rectangle.*?(?:length|side)\s*(\d+(\.\d+)?).*?(?:breadth|bredth|width)\s*(\d+(\.\d+)?)", q
    ):
        l, b = float(match.group(1)), float(match.group(3))
        return f"Area of rectangle = {l} × {b} = {l * b:.2f} square units"

    # Cube volume
    if match := re.search(r"volume of cube.*?(?:side|sides|length)\s*(\d+(\.\d+)?)", q):
        s = float(match.group(1))
        return f"Volume of cube = {s}³ = {s ** 3:.2f} cubic units"

    # Circle area
    if match := re.search(r"(?:area of )?circle.*?(?:radius|r)\s*(?:is\s*)?(\d+(\.\d+)?)", q):
        r = float(match.group(1))
        area = math.pi * r * r
        return f"Area of circle = π × {r}² = {area:.2f} square units"

    # Cylinder volume
    if match := re.search(
        r"volume of cylinder.*?(?:radius|r)\s*(\d+(\.\d+)?).*?(?:height|h)\s*(\d+(\.\d+)?)", q
    ) or re.search(
        r"volume of cylinder.*?whose.*?(?:radius|r)\s*is\s*(\d+(\.\d+)?).*?(?:height|h)\s*is\s*(\d+(\.\d+)?)", q
    ):
        r, h = float(match.group(1)), float(match.group(3))
        volume = math.pi * r * r * h
        return f"Volume of cylinder = π × {r}² × {h} = {volume:.2f} cubic units"



def solve_advanced_math_expression(query: str) -> str | None:
    try:
        expr = sympify(query, evaluate=True)
        result = expr.evalf()
        return f"{query} = {result}"
    except (SympifyError, TypeError, ValueError):
        return None

def get_age_based_prompt(age: int) -> str:
    if age <= 5:
        return "Use fun comparisons and very simple words. Keep it cheerful and short."
    elif age <= 8:
        return "Use clear, everyday examples and avoid big words. Think like school conversations."
    elif age <= 11:
        return "Give step-by-step explanations with real-life examples kids relate to."
    elif age <= 14:
        return "Speak like a middle school teacher. Use age-relevant words and make it practical."
    elif age <= 17:
        return "Teach like a high school teacher. Explain the logic clearly and give good examples."
    elif age <= 22:
        return "Sound like a college professor—use proper terminology but keep it concise."
    else:
        return "Explain like you're talking to an adult learner. Focus on clarity and real-world value."
