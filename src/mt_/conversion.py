from typing import List, Tuple

from .b2m import B2P
from ..lon_ import Phoneme, PhonemeInventory, BN


class PhonemeConvertor:

    def __init__(self) -> None:
        pi = PhonemeInventory()
        self.phoneme_set = pi.phoneme_set_all
        self.phoneme_set_C = pi.phoneme_set_C
        self.sorted_keys = sorted(B2P.charmap.keys(), key=len, reverse=True)

    def extract_phoneme_seq(self, text: str) -> List[str]:
        """Extracting phoneme sequence using charmap

        Args:
            text (str): text in Bengali

        Returns:
            List[str]: Phoneme Sequence
        """
        sep = "/"
        text = f"{sep}{text}{sep}"
        for key in self.sorted_keys:
            text = text.replace(key, f"{sep}{B2P.charmap[key]}{sep}")
        return text.replace(sep * 2, sep)[1:-1].split(sep)

    def extract_char_seq(
        self,
        text: str,
        phoneme_seq: List[str],
    ) -> List[str]:
        """Segmentation of word according to phoneme_seq

        Args:
            text (str): text in Bengali
            phoneme_seq (List[str]): phoneme sequence

        Returns:
            List[str]: character sequence
        """
        char_seq: List[str] = []
        curr_pos = 0
        for phoneme in phoneme_seq:
            if phoneme not in self.phoneme_set:
                char_seq.append(text[curr_pos])
                curr_pos += 1
            elif text[curr_pos] in B2P.p2b_charmap[phoneme]:
                char_seq.append(text[curr_pos])
                curr_pos += 1
            elif text[curr_pos : curr_pos + 2] in B2P.p2b_charmap[phoneme]:
                char_seq.append(text[curr_pos : curr_pos + 2])
                curr_pos += 2

        return char_seq

    def prepare_syllable_phoneme(self, syllable: str) -> List[str]:
        """Prepare Syllable phonemes for spelling module

        Args:
            phoneme_seq (List[str]): phoneme sequence

        Returns:
            List[str]: modified phoneme sequence
        """
        phoneme_seq = self.extract_phoneme_seq(syllable)
        new_phoneme_seq: List[str] = []
        last_idx = len(phoneme_seq) - 1
        # 1. Add schwa wherever necessary
        for i, phoneme in enumerate(phoneme_seq):
            if phoneme not in self.phoneme_set_C:  # C'
                new_phoneme_seq.append(phoneme)
            # phoneme is C
            elif last_idx == 0:  # [C]
                # C -> C + schwa
                new_phoneme_seq.append(phoneme)
                new_phoneme_seq.append(Phoneme.x.value)
            # len > 1
            elif i == last_idx or (  # C at coda
                i < last_idx and phoneme_seq[i + 1] not in self.phoneme_set_C  # CC'
            ):
                new_phoneme_seq.append(phoneme)
            else:
                # C -> C + schwa
                new_phoneme_seq.append(phoneme)
                new_phoneme_seq.append(Phoneme.x.value)

        # 2. Remove if first char in syllable is virama
        if new_phoneme_seq[0] == BN.virama:
            new_phoneme_seq = new_phoneme_seq[1:]

        # 3. Remove non-phonemes and empty syllables
        new_phoneme_seq = [
            phoneme
            for phoneme in new_phoneme_seq
            if phoneme in self.phoneme_set.union({BN.virama})
        ]

        return new_phoneme_seq

    @staticmethod
    def split_seq_by_bool(
        seq: List[str], is_split: List[bool], sep: str = ""
    ) -> List[str]:
        """
        Split a sequence of characters based on boolean split points.

        Args:
            seq (List[str]): The sequence of characters or phonemes to be split.
            is_split (List[bool]): A list of boolean split decisions corresponding to each character or phoneme.
            sep (str, optional): The separator used for joining the characters. Defaults to "".

        Returns:
            List[str]: A list of segments split according to the provided boolean split points.
        """
        indices = [i + 1 for i, sp in enumerate(is_split) if sp]
        return [
            sep.join(seq[start:end]) for start, end in zip([0] + indices[:-1], indices)
        ]

    @staticmethod
    def group_by_bool(
        seq: List[str],
        is_split: List[bool],
    ) -> List[List[str]]:
        """
        Group a sequence of characters based on boolean split points.

        Args:
            seq (List[str]): The sequence of characters or phonemes to be split.
            is_split (List[bool]): A list of boolean split decisions corresponding to each character or phoneme.

        Returns:
            List[str]: A list of segments split according to the provided boolean split points.
        """
        indices = [i + 1 for i, sp in enumerate(is_split) if sp]
        return [seq[start:end] for start, end in zip([0] + indices[:-1], indices)]

    @staticmethod
    def parse_phoneme_seq(
        word_phoneme: List[List[str]],
    ) -> Tuple[List[str], List[bool]]:
        """
        Extract phoneme sequences and split points based on a list of groups of phonemes.

        Args:
            sup_phoneme (List[List[str]]): A list containing groups of phonemes.

        Returns:
            Tuple[List[str], List[bool]]: A tuple containing the phoneme sequence and corresponding split points.
        """
        phoneme_seq = [
            phoneme for sup_phoneme in word_phoneme for phoneme in sup_phoneme
        ]
        is_split = [
            idx == len(ph) - 1 for ph in word_phoneme for idx, _ in enumerate(ph)
        ]
        return phoneme_seq, is_split
