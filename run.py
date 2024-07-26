from typing import Callable

from prepare import prepare_files, prepare_gc_files, prepare_mt_files
from src.gc_ import GlyphCorrection
from src.mt_ import MTransliteration
from utils import save_wordmap, write_list


all_modes = [
    "simple",
    "detailed",
    "wordmap",
    "evaluate",
]


def run(func: Callable, mode: str, baseline: bool = False):
    print(f"Run info:\n{func.__name__=} | {mode=} | {baseline=}")

    root_dir = "data/gc_" if func.__name__.startswith("correct") else "data/mt_"
    if baseline:
        root_dir = root_dir + "base_"

    if mode not in all_modes:
        print(f"{mode} is not a valid mode.")
    # 1. Simple mode
    elif mode == "simple":
        data_file, output_file = prepare_files(
            output_files=["output.txt"],
            root_dir=root_dir,
        )
        content = data_file.read_text(encoding="utf-8").strip()
        output = func(content, show_steps=True)
        output_file.write_text(output, encoding="utf-8")
    # 2. Detailed mode
    elif mode == "detailed":
        data_file, output_file = prepare_files(
            output_files=["detailed.txt"],
            root_dir=root_dir,
        )
        content = data_file.read_text(encoding="utf-8").strip()
        output = func(content, show_steps=True)
        write_list(
            output_file,
            data=[f"{x}\t{y}" for x, y in zip(content.split("\n"), output.split("\n"))],
        )
    # 3. Wordmap mode
    elif mode == "wordmap":
        data_file, output_file, wordmap_file = prepare_files(
            output_files=["uniq_words.txt", "wordmap"],
            root_dir=root_dir,
        )
        content = data_file.read_text(encoding="utf-8").strip()
        output = func(content)
        uniq_words = sorted(set(output.split("\n")))
        write_list(output_file, uniq_words)
        wordmap = {x: y for x, y in zip(content.split("\n"), output.split("\n"))}
        save_wordmap(wordmap=wordmap, wordmap_file=wordmap_file)
    # 4. Evaluate proposed mode
    elif not baseline:
        target_file, output_file, comparison_file, result_file = prepare_files(
            filename or "transcribed.txt",
            output_files=["transliterated.txt", "comparison.txt", "result"],
            use_root_for_input=True,
            root_dir=root_dir,
        )
    # 5. Evaluate baseline modes
    else:
        pass


def run_gc():
    prepare_gc_files()
    gc = GlyphCorrection()
    for mode in all_modes:
        run(gc.correct_words, mode)


def run_mt():
    prepare_mt_files()
    mt = MTransliteration()
    for mode in all_modes:
        run(mt.transliterate_words, mode)
    run(mt.transliterate_words, "evaluate", baseline=True)


if __name__ == "__main__":
    run_gc()
    run_mt()
