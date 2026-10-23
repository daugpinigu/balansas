#!/usr/bin/env python3
"""Surenka entries/*.json i _site/data.json ir nukopijuoja index.html.

Iraso failas: {"date": "YYYY-MM-DD" arba "", "from": "R" | "V", "amount": 4955.39, "note": "", "seq": 1 (tik pradinei istorijai)}
"""
import glob, json, os, shutil, sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")
errors, entries = [], []

for path in sorted(glob.glob(os.path.join(ROOT, "entries", "*.json"))):
    name = os.path.basename(path)
    try:
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{name}: netinkamas JSON ({exc})")
        continue
    side = str(raw.get("from", "")).strip().upper()
    if side not in ("R", "V"):
        errors.append(f'{name}: "from" turi buti "R" arba "V"')
        continue
    try:
        amt = raw.get("amount")
        if isinstance(amt, str):
            amt = amt.replace(" ", "").replace(" ", "").replace(",", ".")
        cents = round(float(amt) * 100)
    except Exception:  # noqa: BLE001
        errors.append(f'{name}: "amount" turi buti skaicius, pvz. 4955.39')
        continue
    if cents <= 0:
        errors.append(f"{name}: suma turi buti teigiama")
        continue
    date = str(raw.get("date", "") or "").strip()
    if date and (len(date) != 10 or date[4] != "-" or date[7] != "-"):
        errors.append(f'{name}: "date" formatas YYYY-MM-DD arba tuscias')
        continue
    seq = raw.get("seq")
    entry = {"id": name[:-5], "file": name, "date": date, "from": side, "cents": cents,
             "note": str(raw.get("note", "") or "").strip()[:200]}
    if isinstance(seq, int) and seq > 0:
        entry["seq"] = seq
    entries.append(entry)

if errors:
    print("KLAIDOS irasuose:", file=sys.stderr)
    for e in errors:
        print(" -", e, file=sys.stderr)
    sys.exit(1)

tot_r = sum(e["cents"] for e in entries if e["from"] == "R")
tot_v = sum(e["cents"] for e in entries if e["from"] == "V")
now = datetime.now(ZoneInfo("Europe/Vilnius"))
data = {"generated": now.strftime("%Y-%m-%d %H:%M"), "count": len(entries),
        "totalR": tot_r, "totalV": tot_v, "balance": tot_r - tot_v, "entries": entries}

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "data.json"), "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)
shutil.copy(os.path.join(ROOT, "index.html"), os.path.join(OUT, "index.html"))
print(f"{len(entries)} irasu | R->V {tot_r/100:.2f} | V->R {tot_v/100:.2f} | balansas {(tot_r-tot_v)/100:.2f}")
