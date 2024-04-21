from typing import Dict, List, Tuple


from .b2m import B2P, P2M
from .conversion import PhonemeConvertor
from ..lon_ import Bengali, Phoneme, PhonemeInventory, PoA, MoA


class Syllabification:
    def __init__(self) -> None:
        self.pi = PhonemeInventory()
        self.pc = PhonemeConvertor()
        self.b2p = B2P()
        self.bn = Bengali()
        self.bn_virama = self.bn.sign_virama
        self.b2p_charmap: Dict[str, str] = self.b2p.charmap
        self.b2p_original_map: Dict[str, str] = self.b2p.p2b_charmap
        self.sorted_keys = sorted(self.b2p_charmap.keys(), key=len, reverse=True)

    def syllabify(self, text: str) -> List[str]:
        # Prepare phoneme list and characters list (includes diphthongs)
        phoneme_seq = self.pc.extract_phoneme_seq(text)
        char_seq = self.pc.extract_char_seq(text, phoneme_seq)

        # Initialise split point to False
        split_points = [False] * (len(char_seq) - 1)

        # Modify marker to universal features
        split_points = self.__char_based_splitting(char_seq, split_points)
        # Modify marker to contextual features
        split_points = self.__phoneme_based_splitting(phoneme_seq, split_points)

        syllabified_word = self.__prepare_syllabified_word(char_seq, split_points)
        syllabified_phonemes = self.__prepare_syllabified_word(
            phoneme_seq, split_points, sep="."
        )

        return syllabified_word, syllabified_phonemes

    def __char_based_splitting(
        self,
        char_list: List[str],
        split_points: List[bool],
    ) -> List[bool]:
        last_idx = len(char_list) - 1
        for idx, char in enumerate(char_list):
            if idx != last_idx and char in self.bn.dependent_consonant_set:
                split_points[idx] = True
            if (
                idx > 1
                and char
                in (
                    self.bn.dependent_consonant_set
                    | self.bn.dependent_vowel_set
                    | self.bn.dependent_diphthongs_set
                )
                and char_list[idx - 1] in self.bn.independent_consonant_set
                and char_list[idx - 2] != self.bn_virama
            ):
                split_points[idx - 2] = True
            if idx > 0 and char in self.bn.independent_vowel_set:
                split_points[idx - 1] = True

        return split_points

    def __phoneme_based_splitting(
        self,
        phoneme_list: List[str],
        split_points: List[bool],
    ) -> List[bool]:
        last_idx = len(phoneme_list) - 1
        for idx, phoneme in enumerate(phoneme_list):
            if idx > 0 and idx < last_idx and phoneme == self.bn_virama:
                if phoneme_list[idx - 1] == phoneme_list[idx + 1]:
                    split_points[idx] = True
                if (
                    self.pi.get_MoA(phoneme_list[idx - 1]) == MoA.PLOSIVE
                    and self.pi.get_MoA(phoneme_list[idx + 1]) == MoA.PLOSIVE
                ):
                    split_points[idx] = True

        return split_points

    def __prepare_syllabified_word(
        self, char_list: List[str], markers: List[bool], sep: str = ""
    ) -> List[str]:
        syllabified_word = []
        used_idx = 0
        for idx, marker in enumerate(markers):
            if marker:
                syllable = sep.join(char_list[used_idx : idx + 1])
                syllabified_word.append(syllable)
                used_idx = idx + 1
        syllable = sep.join(char_list[used_idx:])
        syllabified_word.append(syllable)

        return syllabified_word
