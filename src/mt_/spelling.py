from typing import Dict, List, Tuple

from .b2m import B2P, P2M
from .conversion import PhonemeConvertor
from ..lon_ import MeeteiMayek, PhonemeInventory, Bengali


class Spelling:

    def __init__(self) -> None:
        self.pc = PhonemeConvertor()
        mm = MeeteiMayek()
        self.mm_apun = mm.apun_iyek
        self.ngou_lonsum = mm.letter_ngou_lonsum
        self.nung = mm.vowel_nung
        self.cheitap_vowel_set = mm.cheitap_vowel_set
        bn = Bengali()
        self.virama = bn.sign_virama
        self.pi = PhonemeInventory()
        p2m = P2M()
        self.mm_begin: Dict[str, str] = p2m.mm_begin
        self.mm_end: Dict[str, str] = p2m.mm_end

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
                self.__fix_post_spelling(self.spell_syllable(phoneme_seq))
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
        S = self.mm_begin[phoneme_seq[0]]
        # To check whether nucleus is met
        flag = True if phoneme_seq[0] in self.pi.phoneme_set_V else False
        for idx, phoneme in enumerate(phoneme_seq[1:]):
            if phoneme == self.virama:
                if idx != len(phoneme_seq) - 2:  # Exclude virama at last position
                    S += self.mm_apun
            elif flag:  # Next phoneme after Nucleus
                S += self.mm_end[phoneme]
                flag = False
            elif phoneme in self.pi.phoneme_set_C:  # all C except after nucleus
                S += self.mm_begin[phoneme]
            else:  # V
                flag = True
                S += self.mm_end[phoneme]
        return S

    def __fix_post_spelling(self, word_mm: str):
        if self.ngou_lonsum not in word_mm:
            return word_mm
        else:
            fixed_chars_reverse = ""
            for idx, char in enumerate(word_mm):
                if (
                    char == self.ngou_lonsum
                    and word_mm[idx - 1] not in self.cheitap_vowel_set
                ):
                    fixed_chars_reverse += self.nung
                else:
                    fixed_chars_reverse += char
            return fixed_chars_reverse
