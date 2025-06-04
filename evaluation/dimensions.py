import re

def check_format(story: str) -> bool:
    return bool(re.search(r"As a .*?, I want .*?, so that .*?", story, re.IGNORECASE))

def check_ambiguity(story: str) -> list[str]:
    vague_terms = ["handle", "support", "process", "etc.", "somehow", "thing"]
    found = [word for word in vague_terms if word in story.lower()]
    return found

def check_completeness(story: str) -> bool:
    has_who = "as a" in story.lower()
    has_what = "i want" in story.lower()
    has_why = "so that" in story.lower()
    return has_who and has_what and has_why