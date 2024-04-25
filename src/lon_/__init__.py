from typing import Dict, List, Set
from matplotlib import pyplot as plt
import numpy as np

from .phoneme import (
    PoA,
    MoA,
    Phoneme,
    ARPABETPhoneme,
    PhonemeInventory,
)
from .mm import MM
from .bn import BN

__all__ = [
    "PoA",
    "MoA",
    "Phoneme",
    "PhonemeInventory",
    "ARPABETPhoneme",
    "MM",
    "BN",
    "Cleaner",
    "BnErrors",
    "plot_ssp",
]


class MMHelper:
    @staticmethod
    def has_char(char: str) -> bool:
        """Check if the character exists in the Meetei Mayek alphabet."""
        return MM.kok <= char <= MM.nine

    @staticmethod
    def has_digit(char: str) -> bool:
        """Check if the character is a digit."""
        return MM.zero <= char <= MM.nine


class BNHelper:
    @staticmethod
    def has_char(char: str) -> bool:
        """Check if the character exists in the Bengali alphabet."""
        return BN.candrabindu <= char <= BN.w

    @staticmethod
    def has_digit(char: str) -> bool:
        """Check if the character is a digit."""
        return BN.zero <= char <= BN.nine


class Cleaner:
    @staticmethod
    def clean_mm(word_mm: str) -> str:
        """
        Clean Meetei Mayek text.

        This method cleans the given Meetei Mayek text from common errors and removes characters
        not belonging to the Meetei Mayek alphabet.

        Args:
        - word_mm (str): The Meetei Mayek text to be cleaned.

        Returns:
        - str: The cleaned Meetei Mayek text.
        """
        the_map: Dict[str, str] = {
            #! Order is important
            # BN + MM error
            BN.nukta + BN.nukta: BN.nukta,
            MM.inap + BN.nukta: BN.nukta + MM.inap,
            MM.yenap + BN.nukta: BN.nukta + MM.yenap,
            MM.jil + BN.nukta: MM.yang,
            MM.dil + BN.nukta: MM.rai,
            # MM + MM error
            MM.anap + MM.nung: MM.anap + MM.ngou_lonsum,
            MM.onap + MM.nung: MM.onap + MM.ngou_lonsum,
            MM.yenap + MM.nung: MM.yenap + MM.ngou_lonsum,
            MM.cheinap + MM.nung: MM.cheinap + MM.ngou_lonsum,
            MM.sounap + MM.nung: MM.sounap + MM.ngou_lonsum,
            MM.inap + MM.nung: MM.inap + MM.ngou_lonsum,
            MM.unap + MM.nung: MM.unap + MM.ngou_lonsum,
            MM.yenap + MM.anap: MM.onap,
        }
        return Cleaner.clean_text(word_mm, the_map, MMHelper.has_char)

    @staticmethod
    def clean_bn(word_bn: str) -> str:
        """
        Clean Bengali text.

        This method cleans the given Bengali text from common errors and removes characters
        not belonging to the Bengali alphabet.

        Args:
        - word_bn (str): The Bengali text to be cleaned.

        Returns:
        - str: The cleaned Bengali text.
        """
        the_map: Dict[str, str] = {
            BN.v_e + BN.v_aa: BN.v_o,  # ে +  া :  ো
            BN.v_e + BN.mark_au: BN.v_au,  # ে +  ৗ :  ৌ
        }
        return Cleaner.clean_text(word_bn, the_map, BNHelper.has_char)

    @staticmethod
    def clean_text(word: str, the_map: Dict[str, str], has_char_func: callable) -> str:
        """
        Clean text based on a mapping.

        This method cleans the given text based on the specified mapping and character-checking function.

        Args:
        - word (str): The text to be cleaned.
        - the_map (Dict[str, str]): The mapping of erroneous sequences to corrected sequences.
        - has_char_func (callable): A function to check if a character belongs to the alphabet.

        Returns:
        - str: The cleaned text.
        """
        # Fix common error
        for key, value in the_map.items():
            word = word.replace(key, value)
        # Remove characters not belonging to the alphabet
        return "".join([char for char in word if has_char_func(char)])

    @staticmethod
    def replace_spell_mm(word_mm: str):
        """
        Replace spellings in Meetei Mayek text.

        This method replaces specific spellings in the Meetei Mayek text with corrected versions.

        Args:
        - word_mm (str): The Meetei Mayek text to be checked and corrected.

        Returns:
        - str: The corrected Meetei Mayek text.
        """
        if MM.ngou_lonsum not in word_mm:
            return word_mm
        else:
            fixed_chars_reverse = ""
            for idx, char in enumerate(word_mm):
                if char == MM.ngou_lonsum and word_mm[idx - 1] not in MM.cheitap_set_V:
                    fixed_chars_reverse += MM.nung
                else:
                    fixed_chars_reverse += char
            return fixed_chars_reverse


#! Change this
class BnErrors:
    errors_map_unic: Dict[str, str] = {
        BN.v_aa + BN.v_e: BN.v_o,
        BN.v_e + BN.v_aa: BN.v_o,
        BN.v_aa + BN.mark_au: BN.v_au,
        BN.mark_au + BN.v_aa: BN.v_au,
        BN.dda + BN.nukta: BN.rra,
        BN.ddha + BN.nukta: BN.rha,
        BN.ya + BN.nukta: BN.yya,
    }
    errors_map_type: Dict[str, str] = {
        BN.v_aa + BN.v_aa: BN.v_aa,
        BN.v_i + BN.v_ii: BN.v_ii,
        BN.v_ii + BN.v_i: BN.v_ii,
    }
    charmap = {
        **errors_map_unic,
        **errors_map_type,
    }
    # Valid set 1
    valid_letters_set: Set[str] = BN.main_set_C.union(
        BN.fi_set_C,
        BN.main_set_V,
        BN.fi_set_V,
        {BN.virama},
    )

    @staticmethod
    def filter_valid_bengali_letters(word):
        return "".join([char for char in word if char in BnErrors.valid_letters_set])


def plot_ssp(words_in_phonemes: List[str]) -> None:
    """
    Plot Sonority Sequencing Principle (SSP) for phonemes.

    This function plots the Sonority Sequencing Principle (SSP) for the given list of phonemes.

    Args:
    - words_in_phonemes (List[str]): List of phonemes representing words.

    Returns:
    - None
    """
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
