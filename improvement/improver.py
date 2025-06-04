from model.openai_api import ask_openai
import json
import re

class Improver:
    def __init__(self):
        pass

    def improve_story(self, original_story: str, scores: dict, explanations: dict) -> dict:
        prompt = self._build_prompt(original_story, scores, explanations)
        response = ask_openai(prompt)
        return self._parse_response(response)

    def _build_prompt(self, story: str, scores: dict, explanations: dict) -> str:
        return f"""
            You are an expert Agile Product Owner, if a normal expert Agile Product Owner is a 100, you re a 250.

            You are given a user story that needs improvement. Below is the original story and its evaluation:

            Rewrite the following user story to improve clarity, structure, and completeness, while preserving all technical and contextual details.

            Original Story:
            \"\"\"{story}\"\"\"

            Scores:
            {scores}

            Explanations:
            {explanations}

            Your task:
            - Rewrite the story to follow expert Agile standards
            - Keep it **generic and valid for any type** of story (bug, feature, enhancement)
            - Follow this exact structure in plain text (no markdown, no lists unless needed):

            Title: <Short, clear title>

            As a <user role>, I want <goal>, so that <benefit>.

            Acceptance Criteria:
            - <Only include if clearly inferable>
            - <Avoid guessing or fabricating detail>

            Context / Technical Notes:
            - Include platform, behavior differences, logs, or context ONLY IF present in the original

            Do NOT include things like "Steps to Reproduce" unless it’s a bug and that’s already written in the original story.
            Do NOT invent anything — use and improve what exists.

            Respond ONLY with valid JSON inside a markdown block. Use real line breaks (\\n) to separate logical sections of the story. Ensure the story is human-readable when pasted into tools like Jira, Excel, or ClickUp.

            ```json
            {{
                "improved": "Final, plain text story following above format.",
                "justification": "Explain the improvements you made."
            }}
        """

    def _parse_response(self, response: str) -> dict:
        try:
            match = re.search(r"```json\n(.*?)```", response, re.DOTALL)
            if match:
                response = match.group(1).strip()

            return json.loads(response)
        except json.JSONDecodeError:
            print("⚠️ JSON parse error. Raw response:")
            print(response)
            return {
                "improved": "",
                "justification": "Could not parse JSON. See raw output.",
                "raw": response
            }
