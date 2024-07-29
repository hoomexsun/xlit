import os
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
from src.mt_ import MTransliteration
from src.mt_base_.b2m import Baseline, BaselineExtended
from run import run
from prepare import prepare_paper_replication


def evaluate(data_subdir_dict: Dict[str, str]):
    mt = MTransliteration()
    base1 = Baseline()
    base2 = BaselineExtended()
    for data_type, transcribed_file in data_subdir_dict.items():
        root_dir = f"{transcribed_file}"
        transcribed_file = Path(transcribed_file) / "target.txt"
        print(f"Data type: {data_type}")
        run(
            mt.transliterate_words,
            "evaluate",
            model_name="Proposed",
            root_dir=root_dir,
        )
        run(
            base1.transliterate,
            "evaluate",
            model_name="Baseline",
            root_dir=root_dir,
        )
        run(
            base2.transliterate,
            "evaluate",
            model_name="Baseline 2",
            root_dir=root_dir,
        )


def plot(data_subdir_dict: Dict[str, str], result_files: Dict[str, str]):
    metrics = ["Accuracy", "CER"]
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    for i, metric in enumerate(metrics):
        data_points = {data_type: [] for data_type in data_subdir_dict}
        for data_type, transcribed_file in data_subdir_dict.items():
            w_values, c_values = [], []
            for result_file in result_files.values():
                result_file = Path(transcribed_file) / result_file
                result_file_lines = (
                    result_file.read_text(encoding="utf-8").strip().split("\n")
                )
                w_values.append(100 - float(result_file_lines[0]))
                c_values.append(float(result_file_lines[1]))
            data_points[data_type].extend(
                w_values if metric == "Accuracy" else c_values
            )

        # Plot on the corresponding subplot
        ax = axs[i]
        for data_type, values in data_points.items():
            ax.plot(values, label=f"{data_type}")

        ax.set_xlabel("Models")
        ax.set_ylabel(f"{metric} (%)")
        ax.set_title(f"{metric} Comparison")
        ax.legend(title="Data Subset")
        ax.grid(True)
        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(result_files.keys())
        # ax.set_ylim([0, 100])

        data = pd.DataFrame(data_points, index=list(result_files.keys()))
        print(f"\n{metric}\n{data}")

    plt.savefig(Path("data/corpus/graph.png"))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data_subdir_dict: Dict[str, str] = {
        "Indigenous words": "data/corpus/indigenous_words",
        "Exotic words": "data/corpus/exotic_words",
        "News Corpus": "data/corpus/news_subset",
        "Literature Corpus": "data/corpus/literature_subset",
    }
    result_files_dict: Dict[str, str] = {
        "Baseline 1": "mt_base_/result",
        "Baseline 2": "mt_base_/ext_result",
        "Proposed": "mt_/result",
    }
    prepare_paper_replication()
    evaluate(data_subdir_dict)
    plot(data_subdir_dict, result_files_dict)
