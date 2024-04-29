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
        show_steps: bool = False,
    ) -> str:
        words = []
        for word in tqdm(text.split(), desc="Transliterating..."):
            # for word in text.split():
            words.append(self.transliterate(word=word, show_steps=show_steps))
        return "\n".join(words)

    def transliterate(
        self,
        word: str,
        show_steps: bool = False,
        sep: str = "/",
    ) -> str:
        # 0. Correct common BnErrors
        for key, value in BnErrors.charmap.items():
            word = word.replace(key, value)
        word = BnErrors.filter_valid_bengali_letters(word)
        # 0.1 Skip other process if string is empty
        if not word.strip():
            return ""

        # 1. Phoneme Conversion
        # Prepare phoneme list and characters list (includes diphthongs)
        phoneme_seq = self.pc.extract_phoneme_seq(word)
        char_seq = self.pc.extract_char_seq(word, phoneme_seq)

        # 2. Syllabification
        # Get split points
        split_points = self.syllabification.get_split_points(char_seq, phoneme_seq)

        sup_chars = self.use_split_points(char_seq, split_points)
        sup_phonemes = self.use_split_points(phoneme_seq, split_points, sep=".")

        # 3. Spelling
        # Get words in mm from the syllables
        chars_mm, phonemes_mm = self.spelling.spell(sup_chars)

        # Prepare result string
        res = ""
        if show_steps:
            res += f"{sep.join(sup_chars)}\t{sep.join(sup_phonemes)}\t{sep.join(phonemes_mm)}\t"
        res += "".join(chars_mm)

        return res

    def use_split_points(
        self, char_list: List[str], split_points: List[bool], sep: str = ""
    ) -> List[str]:
        seq = []
        used_idx = 0
        for idx, split_point in enumerate(split_points):
            if split_point:
                seq.append(sep.join(char_list[used_idx : idx + 1]))
                used_idx = idx + 1
        seq.append(sep.join(char_list[used_idx:]))
        return seq
