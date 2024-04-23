import os
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt

from main_mt import run_evaluate, run_evaluate_baseline
from utils import prepare_corpus_transcription


def evaluate(data_subdir_dict: Dict[str, str]):
    for data_type, transcribed_file in data_subdir_dict.items():
        transcribed_file = Path(transcribed_file) / "transcribed.txt"
        print(f"Data type: {data_type}")
        # Baseline models
        output_dir = Path(transcribed_file).parent / "mt_base_"
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nModel: Baselines | Location: {output_dir.as_posix()}\n")
        run_evaluate_baseline(transcribed_file, output_dir, False)
        # Proposed model
        output_dir = Path(transcribed_file).parent / "mt_"
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nModel: Proposed | Location: {output_dir.as_posix()}\n")
        run_evaluate(transcribed_file, output_dir, False)


def plot(data_subdir_dict: Dict[str, str], result_files: Dict[str, str]):
    metrics = ["WER", "CER"]
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    for idx, metric in enumerate(metrics):
        data_points = {data_type: [] for data_type in data_subdir_dict}
        for data_type, transcribed_file in data_subdir_dict.items():
            wer_values, cer_values = [], []
            for result_file in result_files.values():
                result_file = Path(transcribed_file) / result_file
                result_file_lines = (
                    result_file.read_text(encoding="utf-8").strip().split("\n")
                )
                wer_values.append(float(result_file_lines[0]))
                cer_values.append(float(result_file_lines[1]))
            data_points[data_type].extend(wer_values if metric == "WER" else cer_values)

        # Plot on the corresponding subplot
        ax = axs[idx]
        for data_type, values in data_points.items():
            ax.plot(values, label=f"{data_type}")

        ax.set_xlabel("Models")
        ax.set_ylabel(f"{metric} (%)")
        ax.set_title(f"{metric} Comparison")
        ax.legend()
        ax.grid(True)
        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(result_files.keys())
        # ax.set_ylim([0, 100])

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
    prepare_corpus_transcription()
    evaluate(data_subdir_dict)
    plot(data_subdir_dict, result_files_dict)
