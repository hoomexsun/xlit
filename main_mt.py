from pathlib import Path
from typing import Callable, List, Union

import enchant
from tqdm import tqdm

from src.mt_base_ import Baseline, BaselineExtended
from src.mt_ import MTransliteration
from prepare import prepare_files, prepare_mt_files
from utils import save_wordmap


MT_BASE_ROOT_DIR = "data/mt_base_"


# 4. Run evaluate using Proposed Transliteration
def run_evaluate(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
    use_root: bool = True,
) -> None:
    """
    Input (transcribed.txt): words_bn\twords_mm
    Output:
        1. transliterated.txt:
        2. comparison.txt:
        3. result.txt:
    """
    mt = MTransliteration()
    target_file, output_file, comparison_file, result_file = prepare_files(
        filename or "transcribed.txt",
        output_dir,
        output_files=["transliterated.txt", "comparison.txt", "result"],
        use_root_for_input=use_root,
        root_dir=MT_DEFAULT_ROOT_DIR,
    )
    # Proposed Model
    save_evaluation(
        model_name="Proposed",
        transliteration_func=mt.transliterate,
        transcribed_file=target_file,
        transliterated_file=output_file,
        comparison_file=comparison_file,
        result_file=result_file,
    )


# 5. Run evaluate using Baseline Transliteration
def run_evaluate_baseline(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
    use_root_for_input: bool = True,
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
            "comparison.txt",
            "result",
            "ext_transliterated.txt",
            "ext_comparison.txt",
            "ext_result",
        ],
        use_root_for_input=use_root_for_input,
        root_dir=MT_BASE_ROOT_DIR,
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

    # Baseline 2
    save_evaluation(
        model_name="Baseline 2",
        transliteration_func=baseline_ext.transliterate,
        transcribed_file=transcribed_file,
        transliterated_file=ext_transliterated_file,
        comparison_file=ext_comparison_file,
        result_file=ext_result_file,
    )


# CER -> normalize Levenshtein distance to [0, 1]
# d(a,b) / max(len(a), len(b))
def save_evaluation(
    model_name: str,
    transliteration_func: Callable,
    transcribed_file: Path,
    transliterated_file: Path,
    comparison_file: Path,
    result_file: Path,
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
        for word_bn in tqdm(words, desc=f"Model: {model_name}")
    }
    comparison = []
    M = len(words)  # number of words
    N = 0  # Number of characters
    err = 0  # Total edit distance
    num_mismatch = 0  # Number of words with error
    for i, word in enumerate(tqdm(words, desc=f"{model_name} Evaluation")):
        target = transcribed_dict.get(word, "")
        output = transliterated_dict.get(word, "")
        if target != output:
            num_mismatch += 1
        edit_distance = enchant.utils.levenshtein(target, output)
        err += edit_distance
        N += max(len(target), len(output))
        comparison.append(f"{word}\t{target}\t{output}\t{edit_distance}")

    result_content: str = (
        f"{(num_mismatch/M)*100:.02f}\n{(err/N)*100:.02f}\n"
        f"Word Level Accuracy={(1-num_mismatch/M)*100=:.02f}% | {num_mismatch=} | {M=}\n"
        f"Character Level Accuracy={(1-err/N)*100=:.02f}% | {err=} | {N=}"
    )

    result_file.write_text(result_content)
    print(f"\n{result_content}\n")

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


if __name__ == "__main__":

    run_evaluate()
    run_evaluate_baseline()
