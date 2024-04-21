from typing import Dict, List, Tuple

from .b2m import B2P, P2M
from .conversion import PhonemeConvertor
from ..lon_ import MeeteiMayek, PhonemeInventory, Bengali


class Spelling:

    def __init__(self) -> None:
        mm = MeeteiMayek()
        self.pc = PhonemeConvertor()
        self.mm_apun = mm.apun_iyek
        self.ngou_lonsum = mm.letter_ngou_lonsum
        self.nung = mm.vowel_nung
        self.cheitap_vowel_set = mm.cheitap_vowel_set
        bn = Bengali()
        self.virama = bn.sign_virama
        p2m = P2M()
        b2p = B2P()
        self.pi = PhonemeInventory()
        self.b2p_charmap: Dict[str, str] = b2p.charmap
        self.b2p_original_map: Dict[str, str] = b2p.p2b_charmap
        self.sorted_keys = sorted(self.b2p_charmap.keys(), key=len, reverse=True)
        self.mm_begin: Dict[str, str] = p2m.mm_begin
        self.mm_end: Dict[str, str] = p2m.mm_end

    def spell(
        self,
        syllabified_word: List[str],
    ) -> Tuple[List[str], List[str]]:
        mm_syllables: List[str] = []
        mm_phonemes: List[str] = []
        for syllable in syllabified_word:

            syllable_phonemes = self.pc.prepare_syllable_phoneme(
                self.pc.extract_phoneme_seq(syllable)
            )

            mm_syllable = (
                self.__fix_post_spelling(self.spell_syllable(syllable_phonemes))
                if syllable_phonemes
                else ""
            )
            mm_syllables.append(mm_syllable)
            mm_phonemes.append(".".join(syllable_phonemes))
        return mm_syllables, mm_phonemes

    def spell_syllable(self, phoneme_list: List[str]) -> str:
        S = self.mm_begin[phoneme_list[0]]
        # To check whether nucleus is met
        flag = True if phoneme_list[0] in self.pi.phoneme_set_V else False
        for idx, phoneme in enumerate(phoneme_list[1:]):
            if phoneme == self.virama:
                # if idx != len(phoneme_list) - 2:
                if idx != len(phoneme_list) - 2:
                    S += self.mm_apun
            elif flag:
                S += self.mm_end[phoneme]
                flag = False
            elif phoneme in self.pi.phoneme_set_C:
                S += self.mm_begin[phoneme]
            else:
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
