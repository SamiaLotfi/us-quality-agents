from model.openai_api import ask_openai
import json

class Evaluator:
    def __init__(self):
        pass

    def evaluate_story(self, story: str) -> dict:
        prompt = self._build_prompt(story)
        response = ask_openai(prompt)
        result = self._parse_response(response)

        # Flag story if any INVEST score is low
        if "scores" in result:
            invest_keys = [k for k in result["scores"].keys() if k.startswith("INVEST_")]
            low_scores = [s for k, s in result["scores"].items() if k in invest_keys and s < 2]
            result["needs_review"] = len(low_scores) > 0

        result["original"] = story
        return result

    def _build_prompt(self, story: str) -> str:
        return f"""
            You are an expert Agile coach. Evaluate the following user story:

            \"\"\"{story}\"\"\"

            Score it from 1 to 5 on each of these dimensions:
            1. INVEST — score each letter (I, N, V, E, S, T) separately
            2. Ambiguity (lower = more ambiguous)
            3. Completeness (does it clearly state who, what, and why?)
            4. Format (does it follow "As a..., I want..., so that..."?)
            5. Actionability (can a developer take action on it?)
            6. Scope Tightness (is it small and focused?)

            Return ONLY a valid JSON in this format:
            {{
                "scores": {{
                    "INVEST_I": int,
                    "INVEST_N": int,
                    "INVEST_V": int,
                    "INVEST_E": int,
                    "INVEST_S": int,
                    "INVEST_T": int,
                    "Ambiguity": int,
                    "Completeness": int,
                    "Format": int,
                    "Actionability": int,
                    "Scope": int
                }},
                "explanations": {{
                    "INVEST_I": "Explanation for Independent",
                    "INVEST_N": "...",
                    "INVEST_V": "...",
                    "INVEST_E": "...",
                    "INVEST_S": "...",
                    "INVEST_T": "...",
                    "Ambiguity": "...",
                    "Completeness": "...",
                    "Format": "...",
                    "Actionability": "...",
                    "Scope": "..."
                }}
            }}
        """

    def _parse_response(self, response: str) -> dict:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print("⚠️ Could not parse GPT response:")
            print(response)
            return {
                "scores": {},
                "explanations": {},
                "error": "Could not parse OpenAI response",
                "raw": response
            }
