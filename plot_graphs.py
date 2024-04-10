import os
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt

from main_mt import run_evaluate, run_evaluate_baseline


def main(
    run_eval: bool = False,
    run_plot: bool = False,
):
    data_dict: Dict[str, str] = {
        "News-Indigenous": "data/news_ind/transcribed.txt",
        "News-Exotic": "data/news_exo/transcribed.txt",
        "EM-corpus": "data/em/transcribed.txt",
        "IndicTTS": "data/indic/transcribed.txt",
    }
    if run_eval:
        evaluate(data_dict)
    if run_plot:
        plot(data_dict)


def evaluate(data_dict: Dict[str, str]):
    for data_type, transcribed_file in data_dict.items():
        print(f"Evaluating with {data_type}:")
        output_dir = Path(transcribed_file).parent / "mt_"
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nModel: Proposed | Location: {output_dir.as_posix()}\n")
        run_evaluate(transcribed_file, output_dir, False)
        output_dir = Path(transcribed_file).parent / "mt_base_"
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nModel: Baseline | Location: {output_dir.as_posix()}\n")
        run_evaluate_baseline(transcribed_file, output_dir, False)


def plot(data_dict: Dict[str, str]):
    metrics = ["WER", "CER"]
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    for idx, metric in enumerate(metrics):
        data_points = {data_type: [] for data_type in data_dict}

        for data_type, transcribed_file in data_dict.items():
            parent_dir = Path(transcribed_file).parent
            result_files = [
                parent_dir / f"mt_base_/result.txt",
                parent_dir / f"mt_base_/ext_result.txt",
                parent_dir / f"mt_/result.txt",
            ]

            wer_values = []
            cer_values = []

            for result_file in result_files:
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
        ax.set_xticklabels(
            [
                "Baseline",
                "Baseline2",
                "Proposed",
            ]
        )
        # ax.set_ylim([0, 100])

    plt.savefig(Path("data/graph.png"))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main(False, True)
    # main(True, True)
