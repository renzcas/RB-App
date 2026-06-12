def run():
    title = "Module 1: Recon & Target Profiling"
    lesson = """
You learn:
- Passive recon
- WHOIS lookups
- DNS enumeration
- Identifying attack surface
"""
    challenge = """
Challenge:
Pick a domain (real or fictional).
List:
- WHOIS org
- Nameservers
- Tech stack (guess)
- 3 possible attack surfaces
"""
    print(title, lesson, challenge)
    return title
