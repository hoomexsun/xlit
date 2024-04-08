from pathlib import Path
from typing import List, Tuple, Union

import enchant
from tqdm import tqdm

from src.mt_ import MTransliteration
from utils import save_wordmap


# 1. Run simple
def run_simple(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """
    Input: text_bn
    Output (output.txt): text_mm
    """
    mt = MTransliteration()
    data_file, output_file = prepare_files(
        filename, output_dir, output_files=["output.txt"]
    )
    content: str = data_file.read_text(encoding="utf-8").strip()
    output: str = mt.transliterate_words(content)
    output_file.write_text(output, encoding="utf-8")


# 2. Run detailed for both syllabification and transliteration results
def run_detailed(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """
    Input: words_bn
    Output (detailed.txt, detailed.tsv):
        word_bn\tsyllabified_word_bn\tsyllabified_phonemes\tsyllabified_word_mm
    """
    mt = MTransliteration()
    words_file, detailed_txt_file, detailed_tsv_file = prepare_files(
        filename, output_dir, output_files=["detailed.txt", "detailed.tsv"]
    )
    content: str = words_file.read_text(encoding="utf-8").strip()
    output: str = mt.transliterate_words(
        content, include_syllabified=True, include_phonemes=True
    )
    detailed_content = "\n".join(
        [
            f"{word_bn}\t{detailed_word_mm}"
            for word_bn, detailed_word_mm in zip(
                content.split("\n"), output.split("\n")
            )
        ]
    )
    detailed_txt_file.write_text(detailed_content, encoding="utf-8")
    detailed_tsv_file.write_text(detailed_content, encoding="utf-8")


# 3. Run wordmap to get wordmaps
def run_wordmap(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """
    Input: words_bn
    Output:
        0. uniq_words_mm.txt: unique word_mm ordered
        1. wordmap.txt: word_bn\tword_mm
        2. wordmap.json: {word_bn:word_mm}
        3. wordmap.csv: word_bn,word_mm
    """
    mt = MTransliteration()
    data_file, uniq_words_mm_file, wordmap_file = prepare_files(
        filename, output_dir, output_files=["uniq_words_mm.txt", "wordmap"]
    )
    content: str = data_file.read_text(encoding="utf-8").strip()

    output: str = mt.transliterate_words(content)
    uniq_words_mm: List[str] = sorted(set(output.split("\n")))
    uniq_words_mm_file.write_text("\n".join(uniq_words_mm).strip(), encoding="utf-8")
    wordmap = {
        word: transliterated
        for word, transliterated in zip(content.split("\n"), output.split("\n"))
    }
    save_wordmap(wordmap=wordmap, wordmap_file=wordmap_file)


# 4. Run evaluate to calculate WER and CER
# CER -> normalize Levenshtein distance to [0, 1]
# d(a,b) / max(len(a), len(b))
def run_evaluate(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """
    Input (transcribed.txt): words_bn\twords_mm
    Output:
        1. transliterated.txt:
        2. comparison.txt:
        3. result.txt:
    """
    mt = MTransliteration()
    transcribed_file, transliterated_file, comparison_file, result_file = prepare_files(
        filename or "transcribed.txt",
        output_dir,
        output_files=["transliterated.txt", "comparison.tsv", "result.txt"],
        use_root=True,
    )
    word_pairs: str = sorted(
        transcribed_file.read_text(encoding="utf-8").strip().split("\n")
    )
    transcribed_dict = {}
    for line in word_pairs:
        word_bn, transcribed_word_mm = line.split("\t")
        transcribed_dict[word_bn] = transcribed_word_mm
    words = sorted(transcribed_dict.keys())
    transliterated_dict = {
        word_bn: mt.transliterate(word_bn)
        for word_bn in tqdm(words, desc="Transliterating")
    }
    comparison = []

    M = len(words)  # number of words
    N = 0  # Number of characters
    err = 0  # Total edit distance
    num_mismatch = 0  # Number of words with error
    for idx, word in enumerate(tqdm(words, desc="Evaluating")):
        target = transcribed_dict.get(word, "")
        output = transliterated_dict.get(word, "")
        if target != output:
            num_mismatch += 1
        edit_distance = enchant.utils.levenshtein(target, output)
        err += edit_distance
        N += max(len(target), len(output))
        comparison.append(f"{word}\t{target}\t{output}\t{edit_distance}")

    accuracy_word: float = f"{(1-num_mismatch / M)*100=:.02f}"
    accuracy_character: float = f"{(1-err / N)*100=:.02f}"
    result_content: str = (
        f"Word Level Accuracy={accuracy_word} | {num_mismatch=} | {M=}\n"
        f"Character Level Accuracy={accuracy_character} | {err=} | {N=}\n"
    )
    result_file.write_text(result_content)
    print(result_content)

    # Save transliterated file
    transliterated_file.write_text(
        "\n".join(
            [
                f"{word_bn}\t{transliterated_word_mm}"
                for word_bn, transliterated_word_mm in transliterated_dict.items()
            ]
        ),
        encoding="utf-8",
    )

    # Save comparison file
    comparison_file.write_text(
        "\n".join(comparison).strip(),
        encoding="utf-8",
    )


# 0. Preparing default files for Machine Transliteration
def prepare_files(
    filename: Union[str, Path],
    output_dir: Union[str, Path],
    output_files: List[Union[str, Path]],
    use_root: bool = False,
) -> Tuple[Path]:
    root_dir = Path("examples/mt_")
    filename = filename if not use_root else root_dir / filename
    data_file = root_dir / "words.txt" if not filename else Path(filename)
    output_files = [
        root_dir / file if not output_dir else Path(output_dir) / file
        for file in output_files
    ]

    all_files = [data_file] + output_files
    # print(f"{tuple(all_files)=}")
    return tuple(all_files)


if __name__ == "__main__":
    # run_simple()
    # run_detailed()
    # run_wordmap()
    run_evaluate()
