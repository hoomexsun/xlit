from pathlib import Path
from typing import List, Tuple, Union

import enchant
from tqdm import tqdm

from src.mt_base_ import Baseline, BaselineExtended


# Evaluate Baseline 1
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
    baseline = Baseline()
    baseline_ext = BaselineExtended()
    (
        transcribed_file,
        transliterated_file,
        comparison_file,
        result_file,
        ext_transliterated_file,
        ext_comparison_file,
        ext_result_file,
    ) = prepare_files(
        filename or "transcribed.txt",
        output_dir,
        output_files=[
            "transliterated.txt",
            "comparison.tsv",
            "result.txt",
            "ext_transliterated.txt",
            "ext_comparison.tsv",
            "ext_result.txt",
        ],
        use_root=True,
    )

    # Baseline
    save_evaluation(
        model_name="Baseline",
        transliteration_func=baseline.transliterate,
        transcribed_file=transcribed_file,
        transliterated_file=transliterated_file,
        comparison_file=comparison_file,
        result_file=result_file,
    )

    # Baseline Extended
    save_evaluation(
        model_name="Baseline Extended",
        transliteration_func=baseline_ext.transliterate,
        transcribed_file=transcribed_file,
        transliterated_file=ext_transliterated_file,
        comparison_file=ext_comparison_file,
        result_file=ext_result_file,
    )


def save_evaluation(
    model_name,
    transliteration_func,
    transcribed_file,
    transliterated_file,
    comparison_file,
    result_file,
):
    word_pairs: str = sorted(
        transcribed_file.read_text(encoding="utf-8").strip().split("\n")
    )
    transcribed_dict = {}
    for line in word_pairs:
        word_bn, transcribed_word_mm = line.split("\t")
        transcribed_dict[word_bn] = transcribed_word_mm
    words = sorted(transcribed_dict.keys())
    transliterated_dict = {
        word_bn: transliteration_func(word_bn)
        for word_bn in tqdm(words, desc="Transliterating using Baseline")
    }
    comparison = []
    M = len(words)  # number of words
    N = 0  # Number of characters
    err = 0  # Total edit distance
    num_mismatch = 0  # Number of words with error
    for idx, word in enumerate(tqdm(words, desc=f"Evaluating {model_name}")):
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
    root_dir = Path("examples/mt_base_")
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
    run_evaluate()
