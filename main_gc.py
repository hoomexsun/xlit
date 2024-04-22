from pathlib import Path
from typing import List, Tuple, Union

from tqdm import tqdm

from src.gc_ import GlyphCorrection
from utils import prepare_files, save_wordmap


GC_DEFAULT_ROOT_DIR = "data/gc_"


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
        filename, output_dir, output_files=["output.txt"], 
        default_root_dir=GC_DEFAULT_ROOT_DIR,
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
        filename, output_dir, output_files=["detailed.txt"], 
        default_root_dir=GC_DEFAULT_ROOT_DIR,
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
        filename, output_dir, output_files=["uniq_words_bn.txt", "wordmap"], 
        default_root_dir=GC_DEFAULT_ROOT_DIR,
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
        output_files=["result"],
        use_root_for_input=True, 
        default_root_dir=GC_DEFAULT_ROOT_DIR,
    )
    
    M = 0  # number of words
    N = 0  # Number of characters
    err = 0 # Total edit distance
    num_mismatch = 0  # Number of words with error
    eval_content = eval_file.read_text(encoding="utf-8").strip()
    for idx, line in enumerate(tqdm(eval_content.split("\n"), desc="Evaluating")):
        _, _, count, edit_distance = line.split("\t")
        # print(f"{idx=} | {line=} | {fields=}")
        M += 1
        N += int(count)
        if edit_distance != "0":
            num_mismatch += 1
            err += int(edit_distance)

    result_content: str = (
        f"{(num_mismatch/M)*100:.02f}\n{(err/N)*100:.02f}\n"
        f"Word Level Accuracy={(1-num_mismatch/M)*100=:.02f}% | {num_mismatch=} | {M=}\n"
        f"Character Level Accuracy={(1-err/N)*100=:.02f}% | {err=} | {N=}\n"
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
        use_root_for_input=True, 
        default_root_dir=GC_DEFAULT_ROOT_DIR,
    )
    wordmap_content = wordmap_file.read_text(encoding="utf-8").strip()
    new_content = ""
    for word_pair in wordmap_content.split("\n"):
        _, word_bn = word_pair.split("\t")
        new_content += f"{word_pair}\t{len(word_bn)}\t0\n"
    raw_eval_file.write_text(new_content.strip(), encoding="utf-8")

if __name__ == "__main__":
    """        
    For evaluation, run in order of
        run_wordmap() -> prepare_eval() -> `raw_eval.txt` ->
        manually correct & rename file to `eval.txt` ->
        run_evaluate()
    """
    run_simple()
    run_detailed()
    run_wordmap()
    evaluate()

    #! Warning: This might overwrite manually modified file. (Rename existing raw_eval.txt).
    prepare_eval()
