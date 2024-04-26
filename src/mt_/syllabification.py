from typing import List

from .b2m import B2P
from ..lon_ import BN, Phoneme, PhonemeInventory, PoA, MoA


class Syllabification:
    def __init__(self) -> None:
        self.pi = PhonemeInventory()
        self.sorted_keys = sorted(B2P.charmap.keys(), key=len, reverse=True)

    def syllabify_text(self, text: str) -> List[str]:
        # Prepare phoneme list and characters list (includes diphthongs)
        phoneme_seq = self.pc.extract_phoneme_seq(text)
        char_seq = self.pc.extract_char_seq(text, phoneme_seq)

        # Get syllabify
        return self.get_split_points(char_seq, phoneme_seq)

    def get_split_points(
        self,
        char_seq: List[str],
        phoneme_seq: List[str],
    ) -> List[bool]:
        # Initialise split point to False
        # split_points[idx] <- after char
        # split_points[idx - 1] <- before char and so on
        last_idx = len(char_seq) - 1
        split_points = [False] * (len(char_seq) - 1)

        # char based (curr -> idx -> context)
        for idx, char in enumerate(char_seq):
            # Independent vowel and diphthongs
            if char in BN.in_diphthong_set | BN.main_set_V:
                if idx > 0:
                    split_points[idx - 1] = True
            # dependent vowel and diphthongs
            elif char in BN.fi_set_V | BN.fi_diphthong_set:
                if (
                    char_seq[idx - 1] in BN.main_set_C
                    and char_seq[idx - 2] != BN.virama
                ):
                    if idx > 1:
                        split_points[idx - 2] = True
            # dependent consonants
            elif char in BN.fi_set_C:
                if idx != last_idx:
                    split_points[idx] = True
                if idx > 1:
                    if (
                        char_seq[idx - 1] in BN.main_set_C
                        and char_seq[idx - 2] != BN.virama
                    ):
                        split_points[idx - 2] = True
            # Independent/main consonants
            else:
                pass

        # phoneme based (curr -> idx -> context)
        for idx, phoneme in enumerate(phoneme_seq):
            if phoneme == BN.virama:
                if idx > 0 and idx < last_idx:
                    if phoneme_seq[idx - 1] == phoneme_seq[idx + 1]:  # Same phoneme
                        split_points[idx] = True
                    if (
                        self.pi.get_MoA(phoneme_seq[idx - 1]) == MoA.PLOSIVE
                        and self.pi.get_MoA(phoneme_seq[idx + 1]) == MoA.PLOSIVE
                    ):  # Both phoneme are plosive
                        split_points[idx] = True

        # Return split_points
        return split_points
