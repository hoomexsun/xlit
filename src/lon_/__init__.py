from typing import List
from matplotlib import pyplot as plt
import numpy as np

from .enums import Phoneme
from .basic import PoA, MoA, PhonemeInventory, ARPABETPhoneme, MeeteiMayek, Bengali

__all__ = [
    "Phoneme",
    "PoA",
    "MoA",
    "PhonemeInventory",
    "ARPABETPhoneme",
    "MeeteiMayek",
    "Bengali",
    "plot_ssp",
]


def plot_ssp(words_in_phonemes: List[str]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    mmP = PhonemeInventory()
    for i, phonemes in enumerate(words_in_phonemes):
        row = i // 2
        col = i % 2

        sonority_values = [
            mmP.get_seivers(
                phoneme,
            )[0]
            for phoneme in phonemes
        ]
        y = np.array(sonority_values)

        phoneme_labels = [f"{idx}/{phoneme}" for idx, phoneme in enumerate(phonemes)]

        axes[row, col].plot(phoneme_labels, y, marker="*", label=phonemes)

    plt.tight_layout()
    plt.show()
