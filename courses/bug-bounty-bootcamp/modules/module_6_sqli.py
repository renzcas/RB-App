def run():
    title = "Module 6: SQL Injection"
    lesson = """
You learn:
- Boolean-based SQLi
- UNION-based SQLi
- Error-based SQLi
"""
    challenge = """
Challenge:
Given vulnerable query:
"SELECT * FROM users WHERE id = '" + user_input + "'"
Write a payload to dump all users.
"""
    print(title, lesson, challenge)
    return title
