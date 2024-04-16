from pathlib import Path
from typing import Dict, List, Tuple

from tqdm import tqdm

from src.lon_ import MeeteiMayek, Bengali


def main():
    """
    Fix the transcription here first -> "examples/mt_/transcribed.txt"
    """

    words_indigenous, words_exotic, words_news = get_words_news()
    words_em = Path("data/em/words.txt").read_text(encoding="utf-8").strip().split("\n")
    words_indic = (
        Path("data/indic/words.txt").read_text(encoding="utf-8").strip().split("\n")
    )
    all_transcribed_lines = (
        Path("examples/mt_/transcribed.txt")
        .read_text(encoding="utf-8")
        .strip()
        .split("\n")
    )
    # Print
    print(
        f"First Pass\n{len(all_transcribed_lines)=}\n"
        f"{len(words_indigenous)=} | {len(words_exotic)=} | "
        f"{len(words_news)=} | {len(words_em)=} | {len(words_indic)=}"
    )
    words_dict: Dict[int, List[str]] = {
        0: [],  # News
        1: [],  # News Indigenous
        2: [],  # News Exotic
        3: [],  # EM
        4: [],  # Indic
    }
    # Start
    for transcribed_line in tqdm(all_transcribed_lines, desc="Extracting..."):
        word_bn, word_mm = transcribed_line.split("\t")
        if word_bn in words_news:
            words_dict[0].append(transcribed_line)
        if word_bn in words_indigenous:
            words_dict[1].append(transcribed_line)
        if word_bn in words_exotic:
            words_dict[2].append(transcribed_line)
        if word_bn in words_em:
            words_dict[3].append(transcribed_line)
        if word_bn in words_indic:
            words_dict[4].append(transcribed_line)

    Path("data/news/transcribed.txt").write_text(
        "\n".join(words_dict[0]), encoding="utf-8"
    )
    Path("data/news_ind/transcribed.txt").write_text(
        "\n".join(words_dict[1]), encoding="utf-8"
    )
    Path("data/news_exo/transcribed.txt").write_text(
        "\n".join(words_dict[2]), encoding="utf-8"
    )
    Path("data/em/transcribed.txt").write_text(
        "\n".join(words_dict[3]), encoding="utf-8"
    )
    Path("data/indic/transcribed.txt").write_text(
        "\n".join(words_dict[4]), encoding="utf-8"
    )


def get_words_news() -> Tuple[List[str], List[str], List[str]]:
    lines = (
        Path("examples/gc_/eval.txt").read_text(encoding="utf-8").strip().split("\n")
    )
    words_indigenous, words_exotic, words_news = [], [], []
    for line in tqdm(lines, desc="Extracting news words..."):
        fields = line.split("\t")
        if len(fields) == 6:
            word_s550, word_bn, length, err, word_bn_corrected, distribution = fields
            words_news.append(word_bn)
            if distribution == "1":
                words_indigenous.append(word_bn)
            else:
                words_exotic.append(word_bn)
        else:
            word_s550, word_bn, *_ = fields
            words_news.append(word_bn)

    return words_indigenous, words_exotic, words_news


def add_rem_words():
    indic_words = (
        Path("data/indic/words.txt").read_text(encoding="utf-8").strip().split("\n")
    )
    em_words = Path("data/em/words.txt").read_text(encoding="utf-8").strip().split("\n")
    pre_existing_words = (
        Path("examples/mt_/words.txt").read_text(encoding="utf-8").strip().split("\n")
    )
    remaining_words = set(indic_words).union(set(em_words))
    all_words = set(pre_existing_words).union(remaining_words)

    Path("examples/mt_/words.txt").write_text(
        "\n".join(sorted(all_words)), encoding="utf-8"
    )
    Path("examples/mt_/rem_words.txt").write_text(
        "\n".join(sorted(remaining_words)), encoding="utf-8"
    )


def build_rem_pre_transcription():
    pass


def add_rem_transcription():
    pass


#! 16/04/2024
def fix_words_mm():
    transcribed = Path("temp/words_mm_old.txt").read_text(encoding="utf-8")
    transcribed = fix(transcribed)
    Path("temp/words_mm.txt").write_text(transcribed, encoding="utf-8")


def fix_words_pre_existing():
    transcribed = Path("examples/mt_/transcribed.txt").read_text(encoding="utf-8")
    transcribed = fix(transcribed)
    Path("examples/mt_/transcribed.txt").write_text(transcribed, encoding="utf-8")


def fix(transcribed: str) -> str:
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
        # Remove nukta
        bn.sign_nukta: "",
    }
    for key, value in tqdm(the_map.items(), desc="Replacing..."):
        transcribed = transcribed.replace(key, value)
    return transcribed


def combine_words_bn_mm():
    words_bn = Path("temp/words_bn.txt").read_text(encoding="utf-8").strip().split("\n")
    words_mm = Path("temp/words_mm.txt").read_text(encoding="utf-8").strip().split("\n")

    output = "\n".join(
        [f"{word_bn}\t{word_mm}" for word_bn, word_mm in zip(words_bn, words_mm)]
    )

    Path("temp/rem_transcribed.txt").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    # main()
    # add_rem_words()
    # add_rem_transcription()
    # fix_words_mm()
    # combine_words_bn_mm()
    fix_words_pre_existing()
