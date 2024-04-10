from pathlib import Path
from typing import List, Tuple, Union

from tqdm import tqdm

from src.gc_ import GlyphCorrection
from utils import save_wordmap


# 1. Run simple
def run_simple(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """
    Input: text_s550
    Output (output.txt): text_bn
    """
    gc = GlyphCorrection()
    data_file, output_file = prepare_files(
        filename, output_dir, output_files=["output.txt"]
    )
    content: str = data_file.read_text(encoding="utf-8").strip()
    output: str = gc.correct_words(content)
    output_file.write_text(output, encoding="utf-8")


# 2. Run detailed for both syllabification and transliteration results
def run_detailed(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """
    Input: words_bn
    Output (detailed.txt, detailed.tsv): word_s550\tstepwise_text\tword_bn
    """
    gc = GlyphCorrection()
    words_file, detailed_txt_file = prepare_files(
        filename, output_dir, output_files=["detailed.txt"]
    )
    content: str = words_file.read_text(encoding="utf-8").strip()
    output: str = gc.correct_words(content, include_steps=True)
    detailed_content = "\n".join(
        [
            f"{word_s550}\t{detailed_word_bn}"
            for word_s550, detailed_word_bn in zip(
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
    Input: words_s550
    Output:
        0. uniq_words_bn.txt: unique word_bn ordered
        1. wordmap.txt: word_s550\tword_bn
        2. wordmap.json: {word_s500:word_bn}
        3. wordmap.csv: word_s550,word_bn
    """
    gc = GlyphCorrection()
    data_file, uniq_words_bn_file, wordmap_file = prepare_files(
        filename, output_dir, output_files=["uniq_words_bn.txt", "wordmap"]
    )
    content: str = data_file.read_text(encoding="utf-8").strip()
    output: str = gc.correct_words(content)
    uniq_words_bn: List[str] = sorted(set(output.split("\n")))
    uniq_words_bn_file.write_text(
        "\n".join(uniq_words_bn).strip(), encoding="utf-8"
    )
    wordmap = {
        word: corrected
        for word, corrected in zip(content.split("\n"), output.split("\n"))
    }
    save_wordmap(wordmap=wordmap, wordmap_file=wordmap_file)


# Manually prepare eval.txt (from raw_eval.txt) after running prepare_eval()
# 4. Evaluate to calculate WER and CER
# CER -> normalize Levenshtein distance to [0, 1]
# d(a,b) / max(len(a), len(b))
def evaluate(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """
    Only evaluate
    Input (eval.txt): words_bn\twords_mm
    Output: result.txt
    """
    eval_file, result_file = prepare_files(
        filename or "eval.txt",
        output_dir,
        output_files=["result.txt"],
        use_root=True,
    )
    distribution = {
        "1": 0,  # Indigenous
        "2": 0,  # Loan word
        "3": 0,  # Named Entity
        "4": 0,  # Mixed (Loan+ind or named+ind)
    }
    
    M = 0  # number of words
    N = 0  # Number of characters
    err = 0 # Total edit distance
    num_mismatch = 0  # Number of words with error
    eval_content = eval_file.read_text(encoding="utf-8").strip()
    for idx, line in enumerate(tqdm(eval_content.split("\n"), desc="Evaluating")):
        fields = line.split("\t")
        # print(f"{idx=} | {line=} | {fields=}")
        M += 1
        N += int(fields[2])
        if fields[3] != "0":
            num_mismatch += 1
            err += int(fields[3])
        if len(fields) > 5:
            distribution[fields[5]] += 1

    result_content: str = (
        f"{(num_mismatch/M)*100:.02f}\n{(err/N)*100:.02f}\n"
        f"Word Level Accuracy={(1-num_mismatch/M)*100=:.02f}% | {num_mismatch=} | {M=}\n"
        f"Character Level Accuracy={(1-err/N)*100=:.02f}% | {err=} | {N=}"
        f"{distribution=} | Total={sum(distribution.values())}"
    )
    result_file.write_text(result_content)
    print(result_content)


#! Warning: This might overwrite manually modified file (Rename existing raw_eval.txt).
def prepare_eval(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
) -> None:
    """Prepare raw eval file."""
    wordmap_file, raw_eval_file = prepare_files(
        filename or "wordmap.txt",
        output_dir,
        output_files=["raw_eval.txt"],
        use_root=True,
    )
    wordmap_content = wordmap_file.read_text(encoding="utf-8").strip()
    new_content = ""
    for word_pair in wordmap_content.split("\n"):
        _, word_bn = word_pair.split("\t")
        new_content += f"{word_pair}\t{len(word_bn)}\t0\t{word_bn}\n"
    raw_eval_file.write_text(new_content.strip(), encoding="utf-8")

#! Warning: This might overwrite lots of existing files.
def prepare_swap(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
)-> None:
    eval_file, words_swap_file, uniq_words_bn_swap_file, wordmap_swap_file, fix_wordmap_file = prepare_files(
        filename or "eval.txt",
        output_dir,
        output_files=["words.swap.txt", "uniq_words_bn.swap.txt", "wordmap.swap.txt", "fix_wordmap"],
        use_root=True,
    )
    eval_content = (
        eval_file.read_text(encoding="utf-8").strip()
    )
    all_words = []
    all_gc_words = []
    all_gc_words_fix = []
    all_wordmap_ori = {}
    all_wordmap_fix = {}
    for idx, line in enumerate(tqdm(eval_content.split("\n"), desc="Extracting")):
        fields = line.split("\t")
        # print(f"{idx=} | {line=} | {fields=}")
        all_words.append(fields[0])
        all_gc_words.append(fields[1])
        all_gc_words_fix.append(fields[4])
        all_wordmap_ori[fields[0]] = fields[1]
        all_wordmap_fix[fields[1]] = fields[4]

    words_swap_file.write_text("\n".join(all_words), encoding="utf-8")
    uniq_words_bn_swap_file.write_text(
        "\n".join(sorted(set(all_gc_words))), encoding="utf-8"
    )
    save_wordmap(wordmap=all_wordmap_ori, wordmap_file=wordmap_swap_file)
    save_wordmap(wordmap=all_wordmap_fix, wordmap_file=fix_wordmap_file)


# 0. Preparing default files for Glyph Correction
def prepare_files(
    filename: Union[str, Path],
    output_dir: Union[str, Path],
    output_files: List[Union[str, Path]],
    use_root: bool = False,
) -> Tuple[Path]:
    root_dir = Path("examples/gc_")
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
    """        
    For evaluation, run in order of
        run_wordmap() -> prepare_eval() -> `raw_eval.txt` ->
        manually correct & rename file to `eval.txt` ->
        run_evaluate()
    """
    # run_simple()
    # run_detailed()
    # run_wordmap()
    evaluate()

    #! Warning: This might overwrite manually modified file. (Rename existing raw_eval.txt).
    # prepare_eval()

    #! Warning: This might overwrite a lost of existing files.
    # prepare_swap()
