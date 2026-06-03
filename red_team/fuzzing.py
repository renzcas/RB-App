import httpx, random, math

def fuzz_tokens():
    tokens = ["admin123", "null", "", "root", "' OR 1=1 --"]
    return random.choice(tokens)

def calc_entropy(s: str) -> float:
    if not s:
        return 0.0
    probs = [s.count(c)/len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probs)

def send_request(token):
    r = httpx.post("https://httpbin.org/post", json={"username": "admin", "password": token})
    return {
        "token": token,
        "status": r.status_code,
        "length": len(r.text),
        "entropy": calc_entropy(token)   # <-- always present now
    }