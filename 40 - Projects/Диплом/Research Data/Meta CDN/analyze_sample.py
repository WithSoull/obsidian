"""Проверка фрагмента трассы; результат не является оценкой эффективности СППР."""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "trace_sample.csv"
rows = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
times = [int(row["timestamp"]) for row in rows]
start, end = min(times), max(times)
cutoff = start + 180_000
history_ms, horizon_ms = 120_000, 60_000
assert end >= cutoff + horizon_ms, "Неполное окно целевой переменной"
assert all(a <= b for a, b in zip(times, times[1:])), "Нарушен порядок времени"
assert all(row["OpType"] == "1" for row in rows), "Неожиданный тип операции"

past = defaultdict(list)
future = Counter()
sizes = defaultdict(set)
for row in rows:
    timestamp = int(row["timestamp"])
    key = row["cacheKey"]
    if int(row["objectSize"]) > 0:
        sizes[key].add(int(row["objectSize"]))
    if timestamp < cutoff:
        past[key].append(row)
    elif timestamp < cutoff + horizon_ms:
        future[key] += 1

features = []
for key, events in sorted(past.items()):
    known_sizes = {int(row["objectSize"]) for row in events if int(row["objectSize"]) > 0}
    if len(known_sizes) != 1:
        continue
    window_events = [row for row in events if int(row["timestamp"]) >= cutoff - history_ms]
    features.append({
        "object_id": key,
        "cutoff_ms": cutoff,
        "object_size_bytes": next(iter(known_sizes)),
        "recency_ms": cutoff - int(events[-1]["timestamp"]),
        "requests_past_120s": len(window_events),
        "range_requests_past_120s": sum(int(row["rangeStart"]) >= 0 for row in window_events),
        "observed_requests_next_60s": future[key],
        "observed_access_next_60s": int(future[key] > 0),
    })

assert features
with (ROOT / "sample_features.csv").open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(features[0]))
    writer.writeheader()
    writer.writerows(features)

summary = {
    "rows": len(rows),
    "unique_keys": len({row["cacheKey"] for row in rows}),
    "start_ms": start,
    "end_ms": end,
    "duration_seconds": (end - start) / 1000,
    "unknown_size_rows": sum(int(row["objectSize"]) < 0 for row in rows),
    "range_rows": sum(int(row["rangeStart"]) >= 0 for row in rows),
    "keys_with_size_changes": sum(len(values) > 1 for values in sizes.values()),
    "cutoff_ms": cutoff,
    "history_seconds": history_ms // 1000,
    "label_horizon_seconds": horizon_ms // 1000,
    "feature_rows": len(features),
    "positive_labels": sum(row["observed_access_next_60s"] for row in features),
    "sample_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "features_sha256": hashlib.sha256((ROOT / "sample_features.csv").read_bytes()).hexdigest(),
}
(ROOT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
