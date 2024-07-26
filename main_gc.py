from pathlib import Path
from typing import List, Union

from src.gc_ import GlyphCorrection
from prepare import prepare_files, prepare_gc_files
from utils import save_wordmap


# Manually prepare eval.txt (from raw_eval.txt) after running prepare_eval()
# 4. Evaluate to calculate WER and CER
# CER -> normalize Levenshtein distance to [0, 1]
# d(a,b) / max(len(a), len(b))
def run_evaluate(
    filename: Union[str, Path] = "",
    output_dir: Union[str, Path] = "",
    use_root: bool = True,
) -> None:
    """
    Input (corrected.txt): words_s550\twords_bn
    Output: result.txt
    """
    gc = GlyphCorrection()
    target_file, output_file, comparison_file, result_file = prepare_files(
        filename or "corrected.txt",
        output_dir,
        output_files=["transliterated.txt", "comparison.txt", "result.txt"],
        use_root_for_input=use_root,
        root_dir=GC_DEFAULT_ROOT_DIR,
    )

    # Glyph Correction
    save_evaluation(
        model_name="Glyph Correction",
        transliteration_func=gc.correct,
        transcribed_file=target_file,
        transliterated_file=output_file,
        comparison_file=comparison_file,
        result_file=result_file,
    )


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
        root_dir=GC_DEFAULT_ROOT_DIR,
    )
    wordmap_content = wordmap_file.read_text(encoding="utf-8").strip()
    new_content = ""
    for word_pair in wordmap_content.split("\n"):
        _, word_bn = word_pair.split("\t")
        new_content += f"{word_pair}\t{len(word_bn)}\t0\n"
    raw_eval_file.write_text(new_content.strip(), encoding="utf-8")


if __name__ == "__main__":

    evaluate()

    #! Warning: This might overwrite manually modified file. (Rename existing raw_eval.txt).
    prepare_eval()
