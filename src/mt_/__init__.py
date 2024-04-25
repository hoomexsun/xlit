from tqdm import tqdm

from ..lon_ import BnErrors
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

        # 2. Syllabify word_bn and
        syllabified_word_bn, syllabified_phonemes = self.syllabification.syllabify(word)

        # 3. Spelling
        word_mm, intermediate_phoneme = self.spelling.spell(syllabified_word_bn)

        # Prepare result string
        res = ""
        if include_syllabified:
            if include_phonemes:
                syllabified_phonemes = sep.join(syllabified_phonemes)
                res += f"{syllabified_phonemes}\t"
            syllabified_word_bn = sep.join(syllabified_word_bn)
            res += f"{syllabified_word_bn}\t"
        if include_phonemes:
            intermediate_phoneme = sep.join(intermediate_phoneme)
            res += f"{intermediate_phoneme}\t"
            syllabified_word_mm = sep.join(word_mm)
            res += f"{syllabified_word_mm}\t"
        word_mm = "".join(word_mm)
        res += word_mm

        return res
