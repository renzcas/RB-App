def run():
    title = "Module 7: IDOR"
    lesson = """
You learn:
- Broken object-level authorization
- Predictable IDs
- Horizontal privilege escalation
"""
    challenge = """
Challenge:
Given endpoint:
GET /invoice?id=1001
Explain how you'd test for IDOR.
"""
    print(title, lesson, challenge)
    return title
