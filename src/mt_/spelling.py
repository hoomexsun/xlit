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
        syllabified_word: List[str],
    ) -> Tuple[List[str], List[str]]:
        mm_syllables: List[str] = []
        mm_phonemes: List[str] = []
        for syllable in syllabified_word:
            phoneme_seq = self.pc.prepare_syllable_phoneme(
                self.pc.extract_phoneme_seq(syllable)
            )
            mm_syllable = (
                Cleaner.replace_spell_mm(self.spell_syllable(phoneme_seq))
                if phoneme_seq
                else ""
            )
            mm_syllables.append(mm_syllable)
            mm_phonemes.append(".".join(phoneme_seq))
        return mm_syllables, mm_phonemes

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
