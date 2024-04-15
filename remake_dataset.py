from pathlib import Path
from typing import Dict, List, Tuple

from tqdm import tqdm


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


if __name__ == "__main__":
    main()
    add_rem_words()
    # add_rem_transcription()
