from typing import Dict, List, Set, Tuple

from ..lon_ import Phoneme, PhonemeInventory, BN


class PhonemeConvertor:

    def __init__(self) -> None:
        self.pi = PhonemeInventory()
        self.phoneme_set = self.pi.phoneme_set_all
        self.phoneme_set_C = self.pi.phoneme_set_C
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
        #! 1. Special case. diphthong followed by matras is not a diphthong and shoukd be
        #! VCV (for ay) y is semi vowel (check for all diphthongs)
        #! 2. Special combination changing phoneme include diphthong and cluster with b pronounced as w
        #! 3. vocalic r should be ri not just r (viramma-r)
        #! 4. cluster with b at end where it should be w like sb -> sw

        # # Exceptional but always true changes
        # for idx, char in enumerate(char_seq):
        #     if char == BN.yya and char_seq[idx + 1] == BN.virama:
        #         phoneme_seq[idx] = Phoneme.i.value
        #         split_points[idx + 1] = True
        #     if char == BN.v_aa + BN.yya and char_seq[idx + 1] in BN.fi_set_V:
        #         phoneme_seq[idx] == Phoneme.a.value
        #         char_seq[idx] = char_seq
        #     if char == BN.v_aa + BN.yya and char_seq[idx + 1] in BN.fi_set_V:
        #         phoneme_seq[idx]

        # vocalic_r_vowel -> connected r and i sound
        # a+y and a+yy are both ai but y have /Z/ and yya have /Y/
        # some /B/ will have /BH/ in cluster
        # vowel + yya + vowel is not diphthong (for only with matras)
        # change every ya+virama to i before converting to phoneme
        # jophola, rophola and bophola
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

    def split_more(self, word_phonemes: List[List[str]]) -> List[List[str]]:
        phoneme_seq, is_split = self.parse_phoneme_seq(word_phonemes)
        num_v = 0
        for i, phoneme in enumerate(phoneme_seq):
            if phoneme in self.pi.phoneme_set_V | self.pi.phoneme_set_D:
                num_v += 1
            if num_v > 1:
                is_split[i - 2] = True
                num_v = 1
            if is_split[i]:
                num_v = 0

        word_phonemes = self.group_by_bool(phoneme_seq, is_split)
        return word_phonemes[1:] if word_phonemes[0] == BN.virama else word_phonemes

    @staticmethod
    def split_seq_by_bool(
        seq: List[str], split_tags: List[bool], sep: str = ""
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
        indices = [i + 1 for i, sp in enumerate(split_tags) if sp]
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


# Resource: Bengali -> Phoneme
class B2P:
    """Bengali to Phoneme"""

    p2b_charmap: Dict[Phoneme, Set[str]] = {
        Phoneme.k: {BN.ka},
        Phoneme.kh: {BN.kha},
        Phoneme.g: {BN.ga},
        Phoneme.gh: {BN.gha},
        Phoneme.ng: {BN.anusvara, BN.nga},
        Phoneme.c: {BN.ca},
        Phoneme.z: {BN.ja},
        Phoneme.zh: {BN.jha},
        Phoneme.t: {BN.tta, BN.ta, BN.khanda_ta},
        Phoneme.th: {BN.ttha, BN.tha},
        Phoneme.d: {BN.dda, BN.da},
        Phoneme.dh: {BN.ddha, BN.dha},
        Phoneme.n: {BN.nya, BN.nna, BN.na},
        Phoneme.p: {BN.pa},
        Phoneme.ph: {BN.pha},
        Phoneme.b: {BN.ba},
        Phoneme.bh: {BN.bha},
        Phoneme.m: {BN.ma},
        Phoneme.j: {BN.yya, BN.ya},
        Phoneme.r: {BN.r_vocalic, BN.v_r_vocalic, BN.rra, BN.ra, BN.rha},
        Phoneme.w: {BN.w},
        Phoneme.l: {BN.la},
        Phoneme.s: {BN.cha, BN.ssa, BN.sa, BN.sha},
        Phoneme.h: {BN.h},
        # vowels - monophthongs
        Phoneme.i: {BN.i, BN.ii, BN.v_i, BN.v_ii},
        Phoneme.e: {BN.e, BN.v_e},
        Phoneme.x: {BN.a},
        Phoneme.u: {BN.u, BN.uu, BN.v_u, BN.v_uu},
        Phoneme.o: {BN.o, BN.v_o},
        Phoneme.a: {BN.aa, BN.v_aa},
        # vowel - diphthongs
        Phoneme.ai: BN.in_ai | BN.fi_ai,
        Phoneme.xi: BN.in_xi | BN.fi_xi,
        Phoneme.ui: BN.in_ui | BN.fi_ui,
        Phoneme.oi: BN.in_oi | BN.fi_oi,
        Phoneme.au: BN.in_au | BN.fi_au,
        Phoneme.xu: BN.in_xu | BN.fi_xu,
    }

    p2b_charmap: Dict[str, Set[str]] = {
        phoneme.value: char_bn_list for phoneme, char_bn_list in p2b_charmap.items()
    }

    charmap: Dict[str, str] = {
        char_bn: phoneme
        for phoneme, char_bn_list in p2b_charmap.items()
        for char_bn in char_bn_list
    }
