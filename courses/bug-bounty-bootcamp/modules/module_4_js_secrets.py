def run():
    title = "Module 4: JavaScript Secret Hunting"
    lesson = """
You learn:
- How frontend leaks API keys
- Hardcoded tokens
- Hidden endpoints in JS
"""
    challenge = """
Challenge:
Given a JS snippet:
fetch("https://api.example.com/v1/user?key=ABC123")
Identify:
- The secret
- The endpoint
- The risk
"""
    print(title, lesson, challenge)
    return title
