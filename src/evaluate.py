import json, csv
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
tests = [json.loads(l) for l in open("data/test.jsonl", encoding="utf-8")]

def ask(model, msgs):
    r = client.chat.completions.create(model=model, messages=msgs,
                                       temperature=0.2, max_tokens=250)
    return r.choices[0].message.content

def rule_checks(reply):
    return {
        "short": len(reply.split()) < 80,
        "no_phone_leak": not any(c.isdigit() for c in reply.replace(" ", ""))
                         or len([c for c in reply if c.isdigit()]) < 8,
    }

with open("outputs/eval_results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["question", "base_reply", "tuned_reply", "short", "no_phone_leak"])
    for t in tests:
        msgs = t["messages"][:2]                 # system + user
        base = ask("llama3.1", msgs)
        tuned = ask("shopkart", msgs)
        checks = rule_checks(tuned)
        w.writerow([msgs[1]["content"], base, tuned, *checks.values()])
print("Saved outputs/eval_results.csv")