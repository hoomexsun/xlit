from pathlib import Path
from typing import Callable, List, Tuple, Union

import enchant
from tqdm import tqdm

from src.mt_base_ import Baseline, BaselineExtended
from src.mt_ import MTransliteration
from utils import prepare_files, save_wordmap


MT_DEFAULT_ROOT_DIR = "examples/mt_"


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
        filename,
        output_dir,
        output_files=["output.txt"],
        default_root_dir=MT_DEFAULT_ROOT_DIR,
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
    Output (detailed.txt):
        word_bn\tsyllabified_word_bn\tsyllabified_phonemes\tsyllabified_word_mm
    """
    mt = MTransliteration()
    words_file, detailed_txt_file = prepare_files(
        filename,
        output_dir,
        output_files=["detailed.txt"],
        default_root_dir=MT_DEFAULT_ROOT_DIR,
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
        filename,
        output_dir,
        output_files=["uniq_words_mm.txt", "wordmap"],
        default_root_dir=MT_DEFAULT_ROOT_DIR,
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
    transcribed_file, transliterated_file, comparison_file, result_file = prepare_files(
        filename or "transcribed.txt",
        output_dir,
        output_files=["transliterated.txt", "comparison.txt", "result.txt"],
        use_root_for_input=use_root,
        default_root_dir=MT_DEFAULT_ROOT_DIR,
    )
    # Proposed Model
    save_evaluation(
        model_name="Proposed Transliteration",
        transliteration_func=mt.transliterate,
        transcribed_file=transcribed_file,
        transliterated_file=transliterated_file,
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
            "result.txt",
            "ext_transliterated.txt",
            "ext_comparison.txt",
            "ext_result.txt",
        ],
        use_root_for_input=use_root_for_input,
        default_root_dir="examples/mt_base_",
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
        for word_bn in tqdm(words, desc=f"Transliterating using {model_name}")
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
    # run_simple()
    run_detailed()
    # run_wordmap()
    # run_evaluate()
    # run_evaluate_baseline()
