import json, random

random.seed(42)
rows = [json.loads(l) for l in open("data/raw_chats.jsonl", encoding="utf-8")]

# remove duplicates
seen, clean = set(), []
for r in rows:
    key = r["messages"][1]["content"].strip().lower()
    if key not in seen:
        seen.add(key)
        clean.append(r)

random.shuffle(clean)
cut = int(len(clean) * 0.9)

for name, subset in [("train", clean[:cut]), ("test", clean[cut:])]:
    with open(f"data/{name}.jsonl", "w", encoding="utf-8") as f:
        for r in subset:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"train={cut}, test={len(clean)-cut}")