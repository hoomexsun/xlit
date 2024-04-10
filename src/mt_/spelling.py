from typing import Dict, List, Tuple

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
    ) -> Tuple[List[str], List[str]]:
        mm_syllables: List[str] = []
        mm_phonemes: List[str] = []
        for syllable in syllabified_word:
            syllable_phonemes = self.__extract_syllable_phonemes(syllable)
            mm_syllable = (
                self.__fix_post_spelling(self.__run(syllable_phonemes))
                if syllable_phonemes
                else ""
            )
            mm_syllables.append(mm_syllable)
            mm_phonemes.append(".".join(syllable_phonemes))
        return mm_syllables, mm_phonemes

    def __extract_syllable_phonemes(self, syllable: str) -> List[str]:
        # 1. Phoneme Mapping
        sep = "/"
        text = f"{sep}{syllable}{sep}"
        for key in self.sorted_keys:
            text = text.replace(key, f"{sep}{self.b2p_charmap[key]}{sep}")
        syllable_phonemes: List[str] = text.replace(sep * 2, sep)[1:-1].split(sep)

        # Schwa Addition in Spelling Module
        # Use virama to show cluster and add schwa wherever necessary
        new_syllable_phonemes: List[str] = []

        last_idx = len(syllable_phonemes) - 1
        for idx, phoneme in enumerate(syllable_phonemes):
            if phoneme in self.pi.phoneme_set_C:
                # C
                if last_idx == 0:
                    new_syllable_phonemes.append(phoneme)
                    new_syllable_phonemes.append(Phoneme.x.value)
                # .C ..C ...C ....C
                elif idx == last_idx:
                    new_syllable_phonemes.append(phoneme)
                # CV .CV CV. ..CV CV... ...CV.
                # C+ .C+ C+. ..C+ C+... ...C+.
                elif (
                    idx < last_idx
                    and syllable_phonemes[idx + 1] not in self.pi.phoneme_set_C
                ):
                    new_syllable_phonemes.append(phoneme)
                # CC .CC CC. ..CC CC... ...CC. <- First C
                else:
                    new_syllable_phonemes.append(phoneme)
                    new_syllable_phonemes.append(Phoneme.x.value)
                # V / 09cd
            else:
                new_syllable_phonemes.append(phoneme)

        # elif (
        #     len(syllable_phonemes) == 2
        #     and syllable_phonemes[0] in self.pi.phoneme_set_C
        #     and syllable_phonemes[1] in self.pi.phoneme_set_C
        # ):
        #     syllable_phonemes.insert(1, Phoneme.x.value)
        # elif (
        #     len(syllable_phonemes) == 3
        #     and syllable_phonemes[0] in self.pi.phoneme_set_C
        #     and syllable_phonemes[1] == self.virama
        #     and syllable_phonemes[2] in self.pi.phoneme_set_C
        # ):
        #     syllable_phonemes.append(Phoneme.x.value)
        # elif (
        #     len(syllable_phonemes) == 3
        #     and syllable_phonemes[0] in self.pi.phoneme_set_C
        #     and syllable_phonemes[1] in self.pi.phoneme_set_C
        #     and syllable_phonemes[2] == self.virama
        # ):
        #     syllable_phonemes.insert(1, Phoneme.x.value)

        # Remove if first char is virama in a syllable
        if new_syllable_phonemes[0] == self.virama:
            new_syllable_phonemes = new_syllable_phonemes[1:]

        # 3. Remove non-phonemes and empty syllables
        syllable_phonemes = [
            phoneme
            for phoneme in syllable_phonemes
            if phoneme in self.pi.phoneme_set_all or phoneme == self.virama
        ]

        return new_syllable_phonemes

    def __run(self, phoneme_list: List[str]) -> str:
        S = self.mm_begin[phoneme_list[0]]
        # To check whether nucleus is met
        flag = True if phoneme_list[0] in self.pi.phoneme_set_V else False
        for idx, phoneme in enumerate(phoneme_list[1:]):
            if phoneme == self.virama:
                # if idx != len(phoneme_list) - 2:
                if idx != len(phoneme_list) - 2 and not flag:
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
