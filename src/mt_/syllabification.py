from typing import List

from ..lon_ import BN, Phoneme, PhonemeInventory, PoA, MoA


class Syllabification:
    def __init__(self) -> None:
        self.pi = PhonemeInventory()

    def get_is_split(
        self,
        char_seq: List[str],
        phoneme_seq: List[str],
    ) -> List[bool]:
        # Initialise split point to False
        # split_points[idx] <- after char
        # split_points[idx - 1] <- before char and so on
        last_idx = len(char_seq) - 1
        split_points = [False] * len(char_seq)
        split_points.append(True)

        # char based (curr -> idx -> context)
        for idx, char in enumerate(char_seq):
            # Independent vowel and diphthongs
            if char in BN.in_diphthong_set | BN.main_set_V:
                if idx > 0:
                    split_points[idx - 1] = True
            # dependent vowel and diphthongs
            elif char in BN.fi_set_V | BN.fi_diphthong_set:
                if idx > 1:
                    if (
                        char_seq[idx - 1] in BN.main_set_C
                        and char_seq[idx - 2] != BN.virama
                    ):
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
        # Find invalid clusters and split them
        # Find valid cluster and mark nearest possible split point
        for idx, phoneme in enumerate(phoneme_seq):
            if phoneme == BN.virama:

                if idx > 0 and idx < last_idx:
                    # 1. Invalid clusters
                    # Same phoneme
                    if phoneme_seq[idx - 1] == phoneme_seq[idx + 1]:
                        split_points[idx] = True
                    # plosive + plosive
                    elif (
                        self.pi.get_MoA(phoneme_seq[idx - 1]) == MoA.PLOSIVE
                        and self.pi.get_MoA(phoneme_seq[idx + 1]) == MoA.PLOSIVE
                    ):
                        split_points[idx] = True
                    # plosive + nasal
                    elif (
                        self.pi.get_MoA(phoneme_seq[idx - 1]) == MoA.PLOSIVE
                        and self.pi.get_MoA(phoneme_seq[idx + 1]) == MoA.NASAL
                    ):
                        split_points[idx] = True
                    # dip in ssp and next phoneme being vowel is raised
                    # nasal + plosive + V
                    elif (
                        idx < last_idx - 1
                        and self.pi.get_MoA(phoneme_seq[idx - 1]) == MoA.NASAL
                        and self.pi.get_MoA(phoneme_seq[idx + 1]) == MoA.PLOSIVE
                        and phoneme_seq[idx + 2]
                        in self.pi.phoneme_set_V | self.pi.phoneme_set_D
                    ):
                        split_points[idx] = True

                    # 2. Valid clusters
                    # split before when syllable initial consonant cluster is detected
                    elif phoneme_seq[idx + 1] in [
                        Phoneme.r.value,
                        Phoneme.j.value,
                        Phoneme.w.value,
                    ]:
                        if idx > 3 and phoneme_seq[idx - 3] == Phoneme.s.value:
                            split_points[idx - 4] = True
                        elif idx > 1:
                            split_points[idx - 2] = True

                    # split after when syllable final consonant cluster is detected

        # if consonant + virama at end, then join consonant with previous valid vowel to form syllable
        # Forced addition of split point when more than 2 C exist between two consescutive split points
        split_indices = [
            idx for idx, split_point in enumerate(split_points) if split_point
        ]
        # for split_point in split_indices:

        # for idx, char
        # Return split_points
        return split_points
