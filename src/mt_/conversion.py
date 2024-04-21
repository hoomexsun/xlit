from typing import Dict, List, Set

from .b2m import B2P
from ..lon_ import Phoneme, PhonemeInventory, Bengali


class PhonemeConvertor:

    def __init__(self) -> None:
        bn = Bengali()
        self.virama = bn.sign_virama
        pi = PhonemeInventory()
        self.phoneme_set = pi.phoneme_set_all
        self.phoneme_set_C = pi.phoneme_set_C
        b2p = B2P()
        self.p2b_map: Dict[str, Set[str]] = b2p.p2b_charmap
        self.b2p_map: Dict[str, str] = b2p.charmap
        self.sorted_keys = sorted(self.b2p_map.keys(), key=len, reverse=True)

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
            text = text.replace(key, f"{sep}{self.b2p_map[key]}{sep}")
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
            elif text[curr_pos] in self.p2b_map[phoneme]:
                char_seq.append(text[curr_pos])
                curr_pos += 1
            elif text[curr_pos : curr_pos + 2] in self.p2b_map[phoneme]:
                char_seq.append(text[curr_pos : curr_pos + 2])
                curr_pos += 2

        # Return character sequence
        return char_seq

    def prepare_syllable_phoneme(self, phoneme_seq: List[str]) -> List[str]:
        """Prepare Syllable phonemes for spelling module

        Args:
            phoneme_seq (List[str]): phoneme sequence

        Returns:
            List[str]: modified phoneme sequence
        """
        new_phoneme_seq: List[str] = []
        last_idx = len(phoneme_seq) - 1
        # 1. Add schwa wherver necessary
        for idx, phoneme in enumerate(phoneme_seq):
            if phoneme not in self.phoneme_set_C:  # C'
                new_phoneme_seq.append(phoneme)
            elif last_idx == 0:  # [C]
                # C -> C + schwa
                new_phoneme_seq.append(phoneme)
                new_phoneme_seq.append(Phoneme.x.value)
            elif idx == last_idx or (  # C at coda
                idx < last_idx and phoneme_seq[idx + 1] not in self.phoneme_set_C  # CC'
            ):
                new_phoneme_seq.append(phoneme)
            else:
                # C -> C + schwa
                new_phoneme_seq.append(phoneme)
                new_phoneme_seq.append(Phoneme.x.value)

        # 2. Remove if first char in syllable is virama
        if new_phoneme_seq[0] == self.virama:
            new_phoneme_seq = new_phoneme_seq[1:]

        # 3. Remove non-phonemes and empty syllables
        new_phoneme_seq = [
            phoneme
            for phoneme in new_phoneme_seq
            if phoneme in self.phoneme_set.union({self.virama})
        ]

        return new_phoneme_seq
