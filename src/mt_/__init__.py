from typing import List
from tqdm import tqdm


from ..lon_ import BnErrors
from .conversion import PhonemeConvertor
from .syllabification import Syllabification
from .spelling import Spelling

__all__ = [
    "MTransliteration",
    "B2P",
    "P2M",
    "Syllabification",
    "Spelling",
]


class MTransliteration:
    def __init__(self) -> None:
        self.pc = PhonemeConvertor()
        self.syllabification = Syllabification()
        self.spelling = Spelling()

    def transliterate_words(
        self,
        text: str,
        include_syllabified: bool = False,
        include_phonemes: bool = False,
    ) -> str:
        words = []
        for word in tqdm(text.split(), desc="Transliterating..."):
            # for word in text.split():
            words.append(
                self.transliterate(
                    word=word,
                    include_syllabified=include_syllabified,
                    include_phonemes=include_phonemes,
                )
            )
        return "\n".join(words)

    def transliterate(
        self,
        word: str,
        include_syllabified: bool = False,
        include_phonemes: bool = False,
        sep: str = "/",
    ) -> str:
        # 1. Correct spelling first
        for key, value in BnErrors.charmap.items():
            word = word.replace(key, value)
        word = BnErrors.filter_valid_bengali_letters(word)
        # 1.1 Skip other process if strin is empty
        if not word.strip():
            return ""

        # Prepare phoneme list and characters list (includes diphthongs)
        phoneme_seq = self.pc.extract_phoneme_seq(word)
        char_seq = self.pc.extract_char_seq(word, phoneme_seq)

        # 2. Syllabify word_bn and
        split_points = self.syllabification.get_split_points(char_seq, phoneme_seq)

        sup_chars = self.use_split_points(char_seq, split_points)
        sup_phonemes = self.use_split_points(phoneme_seq, split_points, sep=".")

        # 3. Spelling
        word_mm, intermediate_phoneme = self.spelling.spell(sup_chars)

        # Prepare result string
        res = ""
        if include_syllabified:
            if include_phonemes:
                res += f"{sep.join(sup_phonemes)}\t"
            res += f"{sep.join(sup_chars)}\t"
        if include_phonemes:
            res += f"{sep.join(intermediate_phoneme)}\t"
            res += f"{sep.join(word_mm)}\t"
        word_mm = "".join(word_mm)
        res += word_mm

        return res

    def use_split_points(
        self, char_list: List[str], split_points: List[bool], sep: str = ""
    ) -> List[str]:
        syllabified_word = []
        used_idx = 0
        for idx, marker in enumerate(split_points):
            if marker:
                syllable = sep.join(char_list[used_idx : idx + 1])
                syllabified_word.append(syllable)
                used_idx = idx + 1
        syllable = sep.join(char_list[used_idx:])
        syllabified_word.append(syllable)

        return syllabified_word
