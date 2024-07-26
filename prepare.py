from pathlib import Path
from typing import Dict, List, Tuple, Union

from tqdm import tqdm

from src.lon_ import Cleaner
from utils import read_list, read_dict, write_list, write_dict


def prepare_gc_files() -> None:
    """Prepare corrected files for glyph correction."""
    print("Preparing glyph correction files:")
    corrected = read_dict("data/corrected.txt")
    write_dict("data/gc_/corrected.txt", corrected)
    write_list("data/gc_/words.txt", corrected.keys(), True)
    print(f"No of words: {len(corrected)}")


def prepare_mt_files() -> None:
    """Prepare transcribed files for machine transliteration."""
    print("Preparing machine transliteration files:")
    transcribed = read_dict("data/transcribed.txt")
    write_dict("data/mt_/transcribed.txt", transcribed)
    write_dict("data/mt_base_/transcribed.txt", transcribed)
    write_list("data/mt_/words.txt", transcribed.keys(), True)
    write_list("data/mt_base_/words.txt", transcribed.keys(), True)
    print(f"No of words: {len(transcribed)}")


def prepare_files(
    output_files: List[Union[str, Path]],
    root_dir: str,
    use_root_for_input: bool = False,
) -> Tuple[Path]:
    """Prepare default files for Glyph Correction & Machine Transliteration."""
    filename, output_dir = "", ""
    root_dir = Path(root_dir)
    filename = filename if not use_root_for_input else root_dir / filename
    data_file = root_dir / "words.txt" if not filename else Path(filename)
    output_files = [
        root_dir / file if not output_dir else Path(output_dir) / file
        for file in output_files
    ]

    all_files = [data_file] + output_files
    return tuple(all_files)


#! Fix the transcription here first -> examples/mt_/transcribed.txt
def prepare_paper_replication():
    """Prepare corpus transcription by splitting words into various categories."""
    words_news = {
        line.split("\t")[1].strip() for line in read_list("data/gc_/eval.txt")
    }
    words_literature = read_list("data/corpus/literature_subset/words.txt")
    original = read_list("data/transcribed.txt")

    count_ind, count_exo, count_ne, count_hy, count_rem = 0, 0, 0, 0, 0
    words_ind, words_exo = set(), set()
    for i, line in enumerate(tqdm(original, desc="Extracting..."), start=1):
        # print(f"{i=}. {line=}")
        word_bn, _, dist_id = line.split("\t")
        dist_id = int(dist_id)
        if dist_id == 1:
            words_ind.add(word_bn)
            count_ind += 1
        elif dist_id > 1:
            words_exo.add(word_bn)
            if dist_id == 2:
                count_exo += 1
            if dist_id == 3:
                count_ne += 1
            if dist_id == 4:
                count_hy += 1
        elif dist_id == 0:
            count_rem += 1

    words_dict: Dict[int, List[str]] = {
        0: [],  # Indigenous words
        1: [],  # Exotic words
        2: [],  # News subset
        3: [],  # Literature subset
    }
    # Start splitting
    for line in tqdm(original, desc="Preparing..."):
        word_bn, word_mm, _ = line.split("\t")
        new_line = f"{word_bn}\t{word_mm}"
        if word_bn in words_ind:
            words_dict[0].append(new_line)
        if word_bn in words_exo:
            words_dict[1].append(new_line)
        if word_bn in words_news:
            words_dict[2].append(new_line)
        if word_bn in words_literature:
            words_dict[3].append(new_line)

    write_list("data/corpus/indigenous_words/transcribed.txt", words_dict[0]),
    write_list("data/corpus/exotic_words/transcribed.txt", words_dict[1]),
    write_list("data/corpus/news_subset/transcribed.txt", words_dict[2]),
    write_list("data/corpus/literature_subset/transcribed.txt", words_dict[3]),

    print(
        f"Completed Transcription\n{len(original)=}\n"
        f"{len(words_ind)=} | {len(words_exo)=}\n"
        f"{len(words_news)=} | {len(words_literature)=}\n"
    )
    print(
        f"Corpus Distribution\n"
        f"{count_ind=} | {count_exo=} | {count_ne=} | {count_hy=}\n"
        f"{(count_ind+count_exo+count_ne+count_hy)=} | {count_rem=}\n"
    )


#! Text Cleaning "data/mt_/transcribed.txt"
def clean_transcribed() -> None:
    """Clean the transcribed file."""
    c = Cleaner()
    transcribed_file: Path = Path("data/mt_/transcribed.txt")
    new_lines = set()
    lines = transcribed_file.read_text(encoding="utf-8").strip().split("\n")
    for line in tqdm(lines, desc="Cleaning..."):
        word_bn, word_mm = line.split("\t")
        cleaned_word_bn = word_bn
        cleaned_word_mm = c.clean_mm_utf(word_mm)
        new_lines.add(f"{cleaned_word_bn}\t{cleaned_word_mm}")
    transcribed_file.write_text("\n".join(sorted(new_lines)), encoding="utf-8")
