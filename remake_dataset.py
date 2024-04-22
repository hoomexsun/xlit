import os
from pathlib import Path
from typing import Dict, List, Set, Tuple

from tqdm import tqdm

from src.lon_ import MeeteiMayek, Bengali


#! 21/04/2024
#! Check in examples/gc_/eval.txt or examples/gc_/words.txt
#! Remove unnecessary
#! Then run this
def limit_data():
    """
    data/indic/words.txt + examples/gc_/eval.txt -> valid words
    valid words -> examples/mt_/words.txt
    examples/mt_/transcribed.txt in valid words -> examples/mt_/transcribed.txt
    examples/mt_/transcribed.txt in valid words -> examples/mt_base_/transcribed.txt
    """
    mt_transcribed_path = Path("examples/mt_/transcribed.txt")
    mt_base_transcribed_path = Path("examples/mt_base_/transcribed.txt")
    content = mt_transcribed_path.read_text(encoding="utf-8").strip()
    transcribed_dict = {
        line.split("\t")[0]: line.split("\t")[1] for line in content.split("\n")
    }

    _, _, words_news = get_words_news()
    content = Path("data/indic/words.txt").read_text(encoding="utf-8").strip()
    valid_words = words_news | set(content.split("\n"))
    transcribed_words = {word_bn for word_bn in transcribed_dict.keys()}
    Path("examples/mt_/words.txt").write_text(
        "\n".join(sorted(transcribed_words)).strip(), encoding="utf-8"
    )
    rem_words = valid_words.difference(transcribed_words)
    os.makedirs("temp", exist_ok=True)
    Path("temp/words_bn.txt").write_text(
        "\n".join(sorted(rem_words)).strip(), encoding="utf-8"
    )
    Path("temp/words_mm.txt").write_text("", encoding="utf-8")

    valid_transcribed = {
        f"{word_bn}\t{word_mm}"
        for word_bn, word_mm in transcribed_dict.items()
        if word_bn in valid_words
    }
    content = "\n".join(sorted(valid_transcribed))
    mt_transcribed_path.write_text(content, encoding="utf-8")
    mt_base_transcribed_path.write_text(content, encoding="utf-8")

    print(f"{len(valid_words)=} | {len(transcribed_words)=} | {len(rem_words)=}")
    print(f"{len(valid_transcribed)=}")


def get_words_news() -> Tuple[Set[str], Set[str], Set[str]]:
    words_ind, words_exo, words_news = set(), set(), set()
    content = Path("examples/gc_/eval.txt").read_text(encoding="utf-8").strip()
    for line in tqdm(content.split("\n"), desc="Extracting news words..."):
        fields = line.split("\t")
        if len(fields) == 6:
            _, word_bn, _, _, _, distribution = fields
            word_bn = word_bn.strip()
            words_news.add(word_bn)
            if distribution == "1":
                words_ind.add(word_bn)
            else:
                words_exo.add(word_bn)
        else:
            _, word_bn, *_ = fields
            words_news.add(word_bn.strip())

    return words_ind, words_exo, words_news


#! Obtain content of words_mm.txt from cdac_transliteration
#! temp/words_bn.txt + temp/words_mm.txt -> rem_transcribed
#! examples/mt_/transcribed.txt + rem_transcribed -> examples/mt_/transcribed.txt
def add_rem_transcribed():
    existing_file = Path("examples/mt_/transcribed.txt")
    existing = set(existing_file.read_text(encoding="utf-8").strip().split("\n"))
    words_bn = Path("temp/words_bn.txt").read_text(encoding="utf-8").strip().split("\n")
    words_mm = Path("temp/words_mm.txt").read_text(encoding="utf-8").strip()
    if words_mm:
        words_mm = words_mm.split("\n")
        print(f"{len(words_bn)=} != {len(words_mm)}")
        if len(words_bn) != len(words_mm):
            print(f"Not overwriting {existing_file}")
            return
        remaining = {
            f"{word_bn}\t{word_mm}" for word_bn, word_mm in zip(words_bn, words_mm)
        }
        existing = sorted(existing | remaining)
        ask = input(f"This will overwrite {existing_file}, enter y to accept")
        if ask == "y":
            existing_file.write_text("\n".join(existing), encoding="utf-8")


#! Clean
def clean_transcribed() -> None:
    transcribed_file: Path = Path("examples/mt_/transcribed.txt")
    new_lines = set()
    lines = transcribed_file.read_text(encoding="utf-8").strip().split("\n")
    for line in tqdm(lines, desc="Cleaning..."):
        word_bn, word_mm = line.split("\t")
        cleaned_word_bn = word_bn
        cleaned_word_mm = clean_mm(word_mm)
        new_lines.add(f"{cleaned_word_bn}\t{cleaned_word_mm}")
    transcribed_file.write_text("\n".join(sorted(new_lines)), encoding="utf-8")


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
    for key, value in the_map.items():
        word_mm = word_mm.replace(key, value)
    return "".join([char for char in word_mm if mm.has_char(char)])


#! Run split_transcribed() for evaluation
#! Fix the transcription here first -> examples/mt_/transcribed.txt
def split_transcribed():
    words_ind, words_exo, words_news = get_words_news()
    indic_file = Path("data/indic/words.txt")
    words_indic = indic_file.read_text(encoding="utf-8").strip().split("\n")
    lines = (
        Path("examples/mt_/transcribed.txt")
        .read_text(encoding="utf-8")
        .strip()
        .split("\n")
    )
    # Print
    print(
        f"Details\n{len(lines)=}\n"
        f"{len(words_ind)=} | {len(words_exo)=} | "
        f"{len(words_news)=} | {len(words_indic)=}"
    )
    words_dict: Dict[int, List[str]] = {
        0: [],  # News
        1: [],  # News Indigenous
        2: [],  # News Exotic
        4: [],  # Indic
    }
    # Start
    for line in tqdm(lines, desc="Extracting..."):
        word_bn, _ = line.split("\t")
        if word_bn in words_news:
            words_dict[0].append(line)
        if word_bn in words_ind:
            words_dict[1].append(line)
        if word_bn in words_exo:
            words_dict[2].append(line)
        if word_bn in words_indic:
            words_dict[4].append(line)

    Path("data/news/transcribed.txt").write_text(
        "\n".join(words_dict[0]), encoding="utf-8"
    )
    Path("data/news_ind/transcribed.txt").write_text(
        "\n".join(words_dict[1]), encoding="utf-8"
    )
    Path("data/news_exo/transcribed.txt").write_text(
        "\n".join(words_dict[2]), encoding="utf-8"
    )
    Path("data/indic/transcribed.txt").write_text(
        "\n".join(words_dict[4]), encoding="utf-8"
    )


#! Manually correct word_mm in examples/mt_/transcribed.txt
#! Or remove lines in examples/mt_/transcribed.txt
#! and run all the function in the given order to make dataset consistenet


if __name__ == "__main__":
    limit_data()
    add_rem_transcribed()
    clean_transcribed()
    split_transcribed()
