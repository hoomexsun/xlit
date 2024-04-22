import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union

from tqdm import tqdm

from src.lon_ import Bengali, MeeteiMayek


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


# Preparing default files for Glyph Correction & Machine Transliteration
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


#! Prepare transcribed files to run main_mt.py
def prepare_mt_transcription():
    original = Path("data/transcribed.txt").read_text(encoding="utf-8").strip()
    transcribed_dict = {
        line.split("\t")[0]: line.split("\t")[1] for line in original.split("\n")
    }
    words_bn = sorted(transcribed_dict.keys())
    transcribed = "\n".join(
        [f"{word_bn}\t{word_mm}" for word_bn, word_mm in transcribed_dict.items()]
    )
    Path("data/mt_/transcribed.txt").write_text(transcribed, encoding="utf-8")
    Path("data/mt_/words.txt").write_text("\n".join(words_bn), encoding="utf-8")
    Path("data/mt_base_/transcribed.txt").write_text(transcribed, encoding="utf-8")
    Path("data/mt_base_/words.txt").write_text("\n".join(words_bn), encoding="utf-8")


#! Fix the transcription here first -> examples/mt_/transcribed.txt
def prepare_corpus_transcription():
    # Extracting parallel words
    words_news = {
        line.split("\t")[1].strip()
        for line in Path("data/gc_/eval.txt")
        .read_text(encoding="utf-8")
        .strip()
        .split("\n")
    }
    words_literature = (
        Path("data/corpus/literature_subset/words.txt")
        .read_text(encoding="utf-8")
        .strip()
        .split("\n")
    )
    original = (
        Path("data/transcribed.txt").read_text(encoding="utf-8").strip().split("\n")
    )
    words_ind, words_exo = set(), set()
    for line in original:
        word_bn, _, dist_id = line.split("\t")
        dist_id = int(dist_id)
        if dist_id == 1:
            words_ind.add(word_bn)
        elif dist_id > 1:
            words_exo.add(word_bn)
    # Print details
    print(
        f"Details\n{len(original)=}\n"
        f"{len(words_ind)=} | {len(words_exo)=} | "
        f"{len(words_news)=} | {len(words_literature)=}"
    )

    words_dict: Dict[int, List[str]] = {
        0: [],  # Indigenous words
        1: [],  # Exotic words
        2: [],  # News subset
        3: [],  # Literature subset
    }
    # Start splitting
    for line in tqdm(original, desc="Extracting..."):
        word_bn, word_mm, _ = line.split("\t")
        new_line = f"{word_bn}\t{word_mm}"
        if word_bn in words_ind:
            words_dict[0].append(new_line)
        if word_bn in words_exo:
            words_dict[1].append(new_line)
        if word_bn in words_news:
            words_dict[2].append(new_line)
        if word_bn in words_literature:
            words_dict[3].append(new_line)

    Path("data/corpus/indigenous_words/transcribed.txt").write_text(
        "\n".join(words_dict[0]), encoding="utf-8"
    )
    Path("data/corpus/exotic_words/transcribed.txt").write_text(
        "\n".join(words_dict[1]), encoding="utf-8"
    )
    Path("data/corpus/news_subset/transcribed.txt").write_text(
        "\n".join(words_dict[2]), encoding="utf-8"
    )
    Path("data/corpus/literature_subset/transcribed.txt").write_text(
        "\n".join(words_dict[3]), encoding="utf-8"
    )


#! Text Cleaning "data/mt_/transcribed.txt"
def clean_transcribed() -> None:
    transcribed_file: Path = Path("data/mt_/transcribed.txt")
    new_lines = set()
    lines = transcribed_file.read_text(encoding="utf-8").strip().split("\n")
    for line in tqdm(lines, desc="Cleaning..."):
        word_bn, word_mm = line.split("\t")
        cleaned_word_bn = word_bn
        cleaned_word_mm = clean_mm(word_mm)
        new_lines.add(f"{cleaned_word_bn}\t{cleaned_word_mm}")
    transcribed_file.write_text("\n".join(sorted(new_lines)), encoding="utf-8")


#! Text Cleaning Meetei Mayek
def clean_mm(word_mm: str) -> str:
    mm = MeeteiMayek()
    bn = Bengali()
    the_map: Dict[str, str] = {
        #! Order is important
        # bn + mm error
        f"{bn.sign_nukta}{bn.sign_nukta}": f"{bn.sign_nukta}",
        f"{mm.vowel_inap}{bn.sign_nukta}": f"{bn.sign_nukta}{mm.vowel_inap}",
        f"{mm.vowel_yenap}{bn.sign_nukta}": f"{bn.sign_nukta}{mm.vowel_yenap}",
        f"{mm.letter_jil}{bn.sign_nukta}": f"{mm.letter_yang}",
        f"{mm.letter_dil}{bn.sign_nukta}": f"{mm.letter_rai}",
        # mm + mm error
        f"{mm.vowel_anap}{mm.vowel_nung}": f"{mm.vowel_anap}{mm.letter_ngou_lonsum}",
        f"{mm.vowel_onap}{mm.vowel_nung}": f"{mm.vowel_onap}{mm.letter_ngou_lonsum}",
        f"{mm.vowel_yenap}{mm.vowel_nung}": f"{mm.vowel_yenap}{mm.letter_ngou_lonsum}",
        f"{mm.vowel_cheinap}{mm.vowel_nung}": f"{mm.vowel_cheinap}{mm.letter_ngou_lonsum}",
        f"{mm.vowel_sounap}{mm.vowel_nung}": f"{mm.vowel_sounap}{mm.letter_ngou_lonsum}",
        f"{mm.vowel_inap}{mm.vowel_nung}": f"{mm.vowel_inap}{mm.letter_ngou_lonsum}",
        f"{mm.vowel_unap}{mm.vowel_nung}": f"{mm.vowel_unap}{mm.letter_ngou_lonsum}",
        f"{mm.vowel_yenap}{mm.vowel_anap}": f"{mm.vowel_onap}",
    }
    # Fix common error
    for key, value in the_map.items():
        word_mm = word_mm.replace(key, value)
    # Remove words not belonging to MM alphabet
    return "".join([char for char in word_mm if mm.has_char(char)])
