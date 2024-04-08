from typing import Dict, List

from .b2m import B2P, P2M
from ..lon_ import Phoneme, MeeteiMayek, PhonemeInventory, Bengali


class Spelling:

    def __init__(self) -> None:
        mm = MeeteiMayek()
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
        self.b2p_original_map: Dict[str, str] = b2p.original_map
        self.sorted_keys = sorted(self.b2p_charmap.keys(), key=len, reverse=True)
        self.mm_begin: Dict[str, str] = p2m.mm_begin
        self.mm_end: Dict[str, str] = p2m.mm_end

    def spell(
        self,
        syllabified_word: List[str],
        include_phonemes: bool = False,
    ) -> str:
        mm_syllables = []
        mm_phonemes = []
        for syllable in syllabified_word:
            syllable_phonemes = self.__extract_syllable_phonemes(syllable)

            mm_phonemes.append(".".join(syllable_phonemes))
            mm_syllable = self.__run(syllable_phonemes) if syllable_phonemes else ""
            mm_syllables.append(mm_syllable)

        syllable_mm = "/".join(mm_phonemes)
        word_mm = "/".join(mm_syllables) if include_phonemes else "".join(mm_syllables)

        self.__fix_post_spelling(word_mm)
        return word_mm if not include_phonemes else f"{syllable_mm}\t{word_mm}"

    def __extract_syllable_phonemes(self, syllable: str) -> List[str]:
        # 1. Phoneme Mapping
        sep = "/"
        text = f"{sep}{syllable}{sep}"
        for key in self.sorted_keys:
            text = text.replace(key, f"{sep}{self.b2p_charmap[key]}{sep}")
        syllable_phonemes: List[str] = text.replace(sep * 2, sep)[1:-1].split(sep)

        # Schwa Addition in Spelling Module
        # Use virama to show cluster and add schwa wherever necessary
        #! Extend this for all length
        if (
            len(syllable_phonemes) == 1
            and syllable_phonemes[0] in self.pi.phoneme_set_C
        ) or (
            len(syllable_phonemes) == 3
            and syllable_phonemes[0] in self.pi.phoneme_set_C
            and syllable_phonemes[1] == self.virama
            and syllable_phonemes[2] in self.pi.phoneme_set_C
        ):
            syllable_phonemes.append(Phoneme.x.value)
        elif (
            (
                len(syllable_phonemes) == 2
                or (len(syllable_phonemes) == 3 and syllable_phonemes[2] == self.virama)
            )
            and syllable_phonemes[0] in self.pi.phoneme_set_C
            and syllable_phonemes[1] in self.pi.phoneme_set_C
        ):
            syllable_phonemes.insert(1, Phoneme.x.value)

        # Remove if first char is virama in a syllable
        if syllable_phonemes[0] == self.virama:
            syllable_phonemes = syllable_phonemes[1:]

        # 3. Remove non-phonemes and empty syllables
        syllable_phonemes = [
            phoneme
            for phoneme in syllable_phonemes
            if phoneme in self.pi.phoneme_set_all or phoneme == self.virama
        ]

        return syllable_phonemes

    def __run(self, phoneme_list: List[str]) -> str:
        S = self.mm_begin[phoneme_list[0]]
        # To check whether nucleus is met
        flag = True if phoneme_list[0] in self.pi.phoneme_set_V else False
        for idx, phoneme in enumerate(phoneme_list[1:]):
            if phoneme == self.virama:
                if idx != len(phoneme_list) - 2:
                    S += self.mm_apun
            elif flag:
                S += self.mm_end[phoneme]
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
