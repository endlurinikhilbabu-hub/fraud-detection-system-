import os
# pyrefly: ignore [missing-import]
from google import genai
import json
from typing import List, Dict, Optional

def get_client() -> Optional[object]:
    """Returns a Gemini client if GEMINI_API_KEY is available, else None."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not set. AI features will use fallback responses.")
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"WARNING: Could not create Gemini client: {e}")
        return None

def suggest_task_priority(tasks: List[Dict], current_energy: int) -> List[int]:
    """
    Takes a list of tasks and the user's current energy level,
    and returns an AI-optimized prioritization.
    """
    client = get_client()
    if not client:
        # Fallback: sort by priority descending if no AI available
        return [t['id'] for t in sorted(tasks, key=lambda x: x.get('priority', 1), reverse=True)]

    prompt = f"""
    You are PeakMind AI, an expert performance coach.
    The user has an energy level of {current_energy}/100.
    Here are their current pending tasks:
    {json.dumps(tasks, indent=2)}

    Based on their energy level, re-order these tasks to maximize productivity.
    High energy (80-100): Suggest hard/complex tasks first.
    Medium energy (40-79): Suggest moderate tasks first.
    Low energy (0-39): Suggest easy/administrative tasks first, or recommend resting.

    Return the task IDs in the optimal order as a JSON list of integers. Example: [3, 1, 2]
    Only return the JSON list, no other text.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text_response = response.text.strip()
        if text_response.startswith('```json'):
            text_response = text_response[7:-3]
        return json.loads(text_response.strip())
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return [t['id'] for t in tasks]

def get_energy_suggestion(energy_score: int, mood: str = None) -> str:
    """
    Provides a real-time actionable suggestion based on energy log.
    Falls back to a rule-based suggestion if Gemini is unavailable.
    """
    client = get_client()
    if not client:
        # Rule-based fallback
        if energy_score >= 80:
            return "You're at peak energy — tackle your hardest task right now!"
        elif energy_score >= 60:
            return "Good energy! Focus on your medium-priority work for best results."
        elif energy_score >= 40:
            return "Moderate energy — try a short walk then dive into lighter tasks."
        else:
            return "You seem drained. Take a 20-minute break and drink some water."

    prompt = f"""
    You are PeakMind AI, an expert performance coach.
    The user just logged their energy level at {energy_score}/100.
    Their current mood is: {mood if mood else 'Unknown'}.

    Provide ONE short, actionable, and encouraging sentence (max 15 words) on what they should do right now.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        if energy_score < 40:
            return "You seem drained. Take a 20-minute break and drink some water."
        return "You're doing great. Keep up the momentum!"
