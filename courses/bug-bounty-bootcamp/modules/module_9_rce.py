def run():
    title = "Module 9: Remote Code Execution (RCE)"
    lesson = """
You learn:
- File upload attacks
- Command injection
- Template injection
"""
    challenge = """
Challenge:
Given:
os.system("ping " + user_input)
Explain how to exploit it.
"""
    print(title, lesson, challenge)
    return title
