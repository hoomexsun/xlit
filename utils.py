import csv
import json
from pathlib import Path
from typing import Dict


def save_wordmap(wordmap: Dict[str, str], wordmap_file: str | Path):
    # Save in txt format
    txt_path = Path(wordmap_file).with_suffix(".txt")
    txt_path.write_text(
        "\n".join([f"{word}\t{corrected}" for word, corrected in wordmap.items()]),
        encoding="utf-8",
    )

    # Save in json format
    json_path = Path(wordmap_file).with_suffix(".json")
    json_path.write_text(json.dumps(wordmap, ensure_ascii=False), encoding="utf-8")

    # Save in csv format
    csv_path = Path(wordmap_file).with_suffix(".csv")
    with csv_path.open(mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=("lang1", "lang2"))
        writer.writeheader()
        for word1, word2 in wordmap.items():
            writer.writerow({"lang1": word1, "lang2": word2})
