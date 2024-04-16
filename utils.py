import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union


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


# 0. Preparing default files for Glyph Correction & Machine Transliteration
# For gc: default_root_dir="examples/gc_"
# For mt: default_root_dir="examples/mt_"
def prepare_files(
    filename: Union[str, Path],
    output_dir: Union[str, Path],
    output_files: List[Union[str, Path]],
    default_root_dir: str,
    use_root_for_input: bool = False,
) -> Tuple[Path]:
    root_dir = Path(default_root_dir)
    filename = filename if not use_root_for_input else root_dir / filename
    data_file = root_dir / "words.txt" if not filename else Path(filename)
    output_files = [
        root_dir / file if not output_dir else Path(output_dir) / file
        for file in output_files
    ]

    all_files = [data_file] + output_files
    return tuple(all_files)
