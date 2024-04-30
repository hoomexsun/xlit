from typing import Dict, List, Tuple

from .b2m import P2M
from .conversion import PhonemeConvertor
from ..lon_ import PhonemeInventory, BN, MM, Cleaner


class Spelling:

    def __init__(self) -> None:
        self.pc = PhonemeConvertor()
        self.pi = PhonemeInventory()

    def spell(
        self,
        sup_chars: List[str],
    ) -> Tuple[List[str], List[str]]:
        chars_mm: List[str] = []
        phonemes_mm: List[str] = []
        word_phonemes: List[List[str]] = [
            self.pc.prepare_syllable_phoneme(syllable) for syllable in sup_chars
        ]

        # Fix if two or more vowels exist in the same syllable
        word_phonemes = self.split_more(word_phonemes)

        # Actual spelling
        for phoneme_seq in word_phonemes:
            mm_syllable = (
                Cleaner.replace_spell_mm(self.spell_syllable(phoneme_seq))
                if phoneme_seq
                else ""
            )
            chars_mm.append(mm_syllable)
            phonemes_mm.append(".".join(phoneme_seq))
        return chars_mm, phonemes_mm

    def spell_syllable(self, phoneme_seq: List[str]) -> str:
        """
        Apun always inserted for cluster.
        Format Syllable-final cluster: lonsum+apun+mapum

        Args:
            phoneme_list (List[str]): Phoneme sequence in Syllable

        Returns:
            str: spelt syllable in MM
        """
        S = P2M.mm_begin[phoneme_seq[0]]
        # To check whether nucleus is met
        flag = True if phoneme_seq[0] in self.pi.phoneme_set_V else False
        for idx, phoneme in enumerate(phoneme_seq[1:]):
            if phoneme == BN.virama:
                if idx != len(phoneme_seq) - 2:  # Exclude virama at last position
                    S += MM.apun_iyek
            elif flag:  # Next phoneme after Nucleus
                S += P2M.mm_end[phoneme]
                flag = False
            elif phoneme in self.pi.phoneme_set_C:  # all C except after nucleus
                S += P2M.mm_begin[phoneme]
            else:  # V
                flag = True
                S += P2M.mm_end[phoneme]
        return S

    def split_more(self, word_phonemes: List[List[str]]) -> List[List[str]]:
        phoneme_seq, is_split = self.pc.parse_phoneme_seq(word_phonemes)
        num_v = 0
        for i, phoneme in enumerate(phoneme_seq):
            if phoneme in self.pi.phoneme_set_V | self.pi.phoneme_set_D:
                num_v += 1
            if num_v > 1:
                is_split[i - 2] = True
                num_v = 1
            if is_split[i]:
                num_v = 0

        word_phonemes = self.pc.group_by_bool(phoneme_seq, is_split)

        return word_phonemes[1:] if word_phonemes[0] == BN.virama else word_phonemes
