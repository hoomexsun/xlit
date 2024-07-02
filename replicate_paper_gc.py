from pathlib import Path
import matplotlib.pyplot as plt
from collections import Counter


def evaluate() -> None:
    file_path = "data/gc_/comparison.txt"


def plot() -> None:
    file_path = "data/gc_/comparison.txt"
    counts = Counter(read_edit_distance(file_path=Path(file_path)))
    distances = sorted(counts.keys())
    occurences = [counts[distance] for distance in distances]

    plt.bar(distances, occurences)
    plt.xlabel("Edit distance")
    plt.ylabel("Count")
    plt.title("Count of Edit Distances")
    plt.show()


def read_edit_distance(file_path: Path):
    edit_distances = []
    lines = file_path.read_text(encoding="utf-8").strip().split("\n")
    for i, line in enumerate(lines):
        *others, ed = line.split("\t")
        if ed:
            # print(f"{i+1}. {line}")
            edit_distance = int(ed)
            if edit_distance != 0:
                edit_distances.append(edit_distance)
    return edit_distances


if __name__ == "__main__":
    # evaluate()
    plot()
