from typing import Dict, List, Set, Tuple

from .u2b import U2B
from ..lon_ import BN, Cleaner


class Correction:

    def correct(
        self,
        text: str,
        include_steps: bool = False,
    ) -> str:
        steps = []
        # Step 0: Adjusting s550 characters
        text = self.__adjust_glyph(text, charmap=U2B.premap)
        steps.append(text)

        # Step 1: Mapping Bengali Alphabet
        text = self.__map_unicode(text, charmap=U2B.charmap)
        steps.append(text)

        # Step 2: Fix suffix position of r and then mapping
        text = self.__fix_r_glyph(
            text, chars=U2B.s550_extra_chars, charmap=U2B.R_char_r
        )
        steps.append(text)

        # Step 3: Fix prefix position of vowels and fix vowels
        text = self.__fix_vowels(
            text,
            chars=BN.L_vowels,
        )
        text = Cleaner.clean_bn_utf(text)

        steps.append(text)

        # Returns final content
        return text if not include_steps else "\t".join(steps)

    # Private methods
    def __adjust_glyph(self, text: str, charmap: Dict[str, str]) -> str:
        for key, value in charmap.items():
            text = text.replace(key, value)
        return text

    def __map_unicode(self, text: str, charmap: Dict[str, str]) -> str:
        # 1. Mapping to correct unicode values (in order of decreasing size of key length)
        sorted_keys = sorted(charmap.keys(), key=len, reverse=True)
        for key in sorted_keys:
            text = text.replace(key, charmap[key])
        # 2. Fix redundant virama
        num_mistypes: int = 2
        for num in range(num_mistypes + 1, 1, -1):
            text = text.replace(BN.virama * num, BN.virama)
        return text

    def __fix_r_glyph(self, text: str, chars: Set[str], charmap: Dict[str, str]) -> str:
        # 0. Remove extra chars
        for char in chars:
            text = text.replace(char, "")
        # 1. Fixing position of r glyph
        char_list = []
        for idx, char in enumerate(text):
            if char in charmap:
                start_idx = (
                    idx - 7
                    if idx > 6
                    else (idx - 5 if idx > 4 else (idx - 3 if idx > 2 else idx - 1))
                )
                substring, offset = self.__jump(text[start_idx : idx + 1][::-1])
                char_list = char_list[: idx - offset] + substring[::-1]
            else:
                char_list.append(char)
        # 2. Post mapping r
        text = "".join(char_list)
        for char, replacement in charmap.items():
            text = text.replace(char, replacement)

        # 3. Fix redundant virama
        for num in range(3, 1, -1):
            text = text.replace(BN.virama * num, BN.virama)
        return text

    def __fix_vowels(self, text: str, chars: Set[str]):
        # 1. Fixing Left Vowels' position
        char_list = []
        skip_index = -1
        for idx, char in enumerate(text):
            if idx == skip_index:
                skip_index = -1
            elif char in chars:
                stop_idx = (
                    idx + 8
                    if idx <= len(text) - 7
                    else (idx + 6 if idx <= len(text) - 5 else idx + 4)
                )
                substring, offset = self.__jump(text[idx:stop_idx])
                char_list += substring
                skip_index = idx + offset
            elif idx > skip_index:
                char_list.append(char)

        text = "".join(char_list)
        return text

    def __jump(self, chars: str) -> Tuple[List[str], int]:
        char, *right = chars
        idx = 0
        while idx < len(right) - 1 and right[idx + 1] == BN.virama:
            idx += 2
        if idx >= len(right):
            return list(chars), 1
        return (right[: idx + 1] + [char], idx + 1)
