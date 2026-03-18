"""Split chat_epvo.json into smaller files by half-year periods."""
import json
import os
from collections import defaultdict

INPUT = r"g:\Мой диск\Google AI Studio\ЕПВО\instructions\chat_epvo.json"
OUT_DIR = r"g:\Мой диск\Google AI Studio\ЕПВО\instructions\chat_parts"

os.makedirs(OUT_DIR, exist_ok=True)

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data.get("messages", [])
print(f"Total messages: {len(messages)}")

buckets = defaultdict(list)
no_date = []

for msg in messages:
    date_str = msg.get("date", "")
    if not date_str:
        no_date.append(msg)
        continue
    year = date_str[:4]
    month = int(date_str[5:7])
    half = "H1" if month <= 6 else "H2"
    key = f"{year}-{half}"
    buckets[key].append(msg)

if no_date:
    buckets["no_date"] = no_date

for key in sorted(buckets.keys()):
    msgs = buckets[key]
    out_path = os.path.join(OUT_DIR, f"chat_epvo_{key}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=1)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"  {key}: {len(msgs)} messages, {size_kb:.0f} KB -> {os.path.basename(out_path)}")

print("Done.")
