# app/services/task_breakdown.py
from anthropic import Anthropic
import json
import os

# TODO: Create the Anthropic client
# Hint: anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
# Store it as a module-level variable so it's created once
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def generate_subtasks(task_title: str) -> list[str]:
    """
    Calls the Claude API to break a task into subtasks.
    Returns a list of subtask strings.
    """
    
    # TODO: Write a system prompt that tells Claude:
    # 1. Its role ("You are a task breakdown expert...")
    # 2. What to return (a JSON object with a "subtasks" key — a list of strings)
    # 3. Strict formatting rules: NO markdown, NO explanation, ONLY the JSON object
    # WHY strict formatting? Because you'll parse this with json.loads() — any extra
    # text will cause a crash
    system_prompt = """
                    You are a task breakdown expert. When given a task or goal,
                    decompose it into clear, actionable subtasks.
                    You MUST respond with ONLY a valid JSON object in exactly this format:
                    {"subtasks": ["subtask 1", "subtask 2", "subtask 3"]}
                    Each subtask must be a plain string. No objects, no ids, no descriptions.
                    No markdown, no explanation, no code fences — just the raw JSON object.
                    """

    # TODO: Write the user message
    # Keep it simple: tell Claude the task title and ask it to break it down
    # Hint: f-strings let you embed the task_title variable
    user_message = f"Please breakdown the task into a smaller subtasks: {task_title}"
    
    # TODO: Call client.messages.create()
    # - model: "claude-haiku-4-5-20251001"  ← fast and cheap, perfect for this
    # - max_tokens: 1000
    # - system: your system_prompt
    # - messages: [{"role": "user", "content": user_message}]
    response = client.messages.create(
        model= "claude-haiku-4-5-20251001",
        max_tokens = 200,
        system = system_prompt,
        messages = [
            {"role": "user", "content": user_message}
        ]
    )
    
    # TODO: Extract the text from the response
    # Hint: response.content[0].text
    raw_text = response.content[0].text
    # TODO: Parse the JSON
    # Hint: json.loads(raw_text)
    # Hint: The result is a dict — how do you get the "subtasks" key from a dict?
    # TODO: Wrap in try/except — if parsing fails, return a fallback list
    # Hint: ["Could not parse AI response"]
    try:
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]  # remove first line (```json)
            cleaned = cleaned.rsplit("```", 1)[0]  # remove trailing ```
        parsed_response = json.loads(cleaned)
        return parsed_response["subtasks"]
    except (json.JSONDecodeError, KeyError):
        return ["Could not parse AI response"]
    

def suggest_priority(
    task_title: str,
    description: str | None = None,
    due_date: str | None = None  # pass as string e.g. "2025-02-14"
) -> dict:
    """
    Calls the Claude API to suggest a priority level for a task.
    Returns a dict: {"priority": "low|medium|high", "reasoning": "..."}
    """

    # TODO: Write a system prompt that:
    # 1. Defines Claude's role as a task prioritization expert
    # 2. Lists the THREE criteria Claude should evaluate:
    #    - Urgency (due date proximity, urgent keywords)
    #    - Impact (how important/critical does this seem)
    #    - Effort (complexity implied by the description)
    # 3. Defines valid priority values: ONLY "low", "medium", or "high"
    # 4. Specifies the EXACT output format — a JSON object with two keys:
    #    "priority" (string) and "reasoning" (one sentence max)
    # 5. Bans all markdown, all extra text, only raw JSON
    system_prompt = """
                    You are a task prioritization expert.
                    You need to evaluate a task based on the following criteria:
                    1. Urgency(due date proximity, urgent keywords)
                    2. Impact (how important/critical does this seem)
                    3. Effort (complexity iimplied by the description)
                    The valid priority values are only: "low", "medium", or "high"
                    your output should be in the following json format:
                    {"priority": "low"|"medium"|"high", "reasoning": "Could not identify priority"}
                    Ban all markdown extras, only raw JSON
                    """  

    # TODO: Build the user message
    # Include: task title, description (if provided), due_date (if provided)
    # Hint: Build it conditionally — don't include "Description: None"
    # Think about what information a human prioritizer would want to see
    user_message = f"Task: {task_title}"
    if due_date:
        user_message += f"\nDue date: {due_date}"
    if description:
        user_message += f"\nDescription: {description}"

    # TODO: Call client.messages.create()
    # Same pattern as generate_subtasks — model, max_tokens, system, messages
    # Hint: 200 max_tokens is enough for a short JSON response
    response = client.messages.create(
        model= "claude-haiku-4-5-20251001",
        max_tokens = 200,
        system = system_prompt,
        messages = [
            {"role": "user", "content": user_message}
        ]
    )

    # TODO: Extract raw_text from response.content[0].text
    raw_text = response.content[0].text

    # TODO: Defensively parse the JSON (same strip pattern as generate_subtasks)
    # Return the parsed dict on success
    # On failure, return a fallback: {"priority": "medium", "reasoning": "Could not parse AI response"}
    try:
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]  # remove first line (```json)
            cleaned = cleaned.rsplit("```", 1)[0]  # remove trailing ```
        parsed_response = json.loads(cleaned)
        return parsed_response
    except (json.JSONDecodeError, KeyError):
        return {"priority": "medium", "reasoning": "Could not parse AI response"}