from tqdm import tqdm

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
    ) -> str:
        syllabified_word = self.syllabification.syllabify(word)
        word_mm = self.spelling.spell(
            syllabified_word=syllabified_word, include_phonemes=include_phonemes
        )

        return word_mm if not include_syllabified else f"{syllabified_word}\t{word_mm}"
