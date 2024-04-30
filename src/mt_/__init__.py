from tqdm import tqdm


from ..lon_ import Cleaner
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
        for i, word in enumerate(tqdm(text.split(), desc="Transliterating...")):
            # print(f"{i=} | {word=}")
            words.append(self.transliterate(word=word, show_steps=show_steps))
        return "\n".join(words)

    def transliterate(
        self,
        word: str,
        show_steps: bool = False,
        sep: str = "/",
    ) -> str:
        # 0. Clean input text
        word = Cleaner.clean_bn(word, deep_clean=True)
        # 0.1 Skip other process if string is empty
        if not word.strip():
            return ""

        # 1. Phoneme Conversion
        # Prepare phoneme list and characters list (includes diphthongs)
        phoneme_seq = self.pc.extract_phoneme_seq(word)
        char_seq = self.pc.extract_char_seq(word, phoneme_seq)

        # 2. Syllabification
        # Get split points
        is_split = self.syllabification.get_is_split(char_seq, phoneme_seq)

        sup_chars = self.pc.split_seq_by_bool(char_seq, is_split)
        sup_phonemes = self.pc.split_seq_by_bool(phoneme_seq, is_split, sep=".")

        # 3. Spelling
        # Get words in mm from the syllables
        chars_mm, phonemes_mm = self.spelling.spell(sup_chars)

        # Prepare result string
        res = ""
        if show_steps:
            res += f"{sep.join(sup_chars)}\t{sep.join(sup_phonemes)}\t{sep.join(phonemes_mm)}\t"
        res += "".join(chars_mm)

        return res
