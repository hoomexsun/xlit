from typing import Dict, Set

from .bn import BN, BNHelper
from .mm import MM, MMHelper


class Cleaner:
    @staticmethod
    def clean_mm(word_mm: str) -> str:
        """
        Clean Meetei Mayek text.

        This method cleans the given Meetei Mayek text from common errors and removes characters
        not belonging to the Meetei Mayek alphabet.

        Args:
        - word_mm (str): The Meetei Mayek text to be cleaned.

        Returns:
        - str: The cleaned Meetei Mayek text.
        """
        mapping_dict: Dict[str, str] = {
            #! Order is important
            # BN + MM error
            BN.nukta + BN.nukta: BN.nukta,
            MM.inap + BN.nukta: BN.nukta + MM.inap,
            MM.yenap + BN.nukta: BN.nukta + MM.yenap,
            MM.jil + BN.nukta: MM.yang,
            MM.dil + BN.nukta: MM.rai,
            # MM + MM error
            MM.anap + MM.nung: MM.anap + MM.ngou_lonsum,
            MM.onap + MM.nung: MM.onap + MM.ngou_lonsum,
            MM.yenap + MM.nung: MM.yenap + MM.ngou_lonsum,
            MM.cheinap + MM.nung: MM.cheinap + MM.ngou_lonsum,
            MM.sounap + MM.nung: MM.sounap + MM.ngou_lonsum,
            MM.inap + MM.nung: MM.inap + MM.ngou_lonsum,
            MM.unap + MM.nung: MM.unap + MM.ngou_lonsum,
            MM.yenap + MM.anap: MM.onap,
        }
        word_mm = Cleaner.clean_text(word_mm, mapping_dict)
        return Cleaner.keep_alphabet(word_mm, MMHelper.has_char)

    @staticmethod
    def clean_bn(word_bn: str, deep_clean: bool) -> str:
        """
        Clean Bengali text.

        This method cleans the given Bengali text from common errors and removes characters
        not belonging to the Bengali alphabet.

        Args:
        - word_bn (str): The Bengali text to be cleaned.

        Returns:
        - str: The cleaned Bengali text.
        """
        mapping_dict: Dict[str, str] = {
            # Repitition
            BN.nukta + BN.nukta: BN.nukta,
            BN.virama + BN.virama: BN.virama,
            BN.v_aa + BN.v_aa: BN.v_aa,
            BN.v_i + BN.v_ii: BN.v_ii,
            BN.v_ii + BN.v_i: BN.v_ii,
            # Always true
            BN.v_e + BN.v_aa: BN.v_o,  # ে +  া :  ো
            BN.v_e + BN.mark_au: BN.v_au,  # ে +  ৗ :  ৌ
            # Mistypes
            BN.v_aa + BN.v_e: BN.v_o,  # া +  ে :  ো
            BN.mark_au + BN.v_aa: BN.v_au,  # ৗ +  ে :  ৌ
            # Combination with nukta
            BN.dda + BN.nukta: BN.rra,
            BN.ddha + BN.nukta: BN.rha,
            BN.ya + BN.nukta: BN.yya,
            # Remove mark characters
            BN.nukta: "",
            BN.mark_au: "",
        }
        word_bn = Cleaner.clean_text(word_bn, mapping_dict)
        if deep_clean:
            digit_mapping_dict = {char: "" for char in BN.digit_set}
            invalid_virama_pre = {
                f"{BN.virama}{char}": char
                for char in BN.fi_set_V | BN.main_set_V | BN.fi_set_C
            }
            invalid_virama_suff = {
                f"{char}{BN.virama}": char
                for char in BN.fi_set_V | BN.main_set_V | BN.fi_set_C
            }

            rare_error_mapping_dict = {
                **digit_mapping_dict,
                **invalid_virama_pre,
                **invalid_virama_suff,
            }
            word_bn = word_bn[1:] if word_bn[0] == BN.virama else word_bn
            word_bn = Cleaner.clean_text(word_bn, rare_error_mapping_dict)

        return Cleaner.keep_alphabet(word_bn, BNHelper.has_char)

    @staticmethod
    def clean_text(word: str, the_map: Dict[str, str]) -> str:
        """
        Cleans the given text based on the specified mapping.

        Args:
        - word (str): The text to be cleaned.
        - the_map (Dict[str, str]): The mapping of erroneous sequences to corrected sequences.

        Returns:
        - str: The cleaned text.
        """
        for key, value in the_map.items():
            word = word.replace(key, value)
        return "".join(word)

    @staticmethod
    def keep_alphabet(word: str, has_char_func: callable) -> str:
        """
        Removes character in the word which are outside the alphabet.

        Args:
        - word (str): The text to be cleaned.
        - has_char_func (callable): A function to check if a character belongs to the alphabet.

        Returns:
        - str: The cleaned text.
        """
        return "".join([char for char in word if has_char_func(char)])

    @staticmethod
    def replace_spell_mm(word_mm: str):
        """
        Replace spellings in Meetei Mayek text.

        This method replaces specific spellings in the Meetei Mayek text with corrected versions.

        Args:
        - word_mm (str): The Meetei Mayek text to be checked and corrected.

        Returns:
        - str: The corrected Meetei Mayek text.
        """
        if MM.ngou_lonsum not in word_mm:
            return word_mm
        else:
            fixed_chars_reverse = ""
            for idx, char in enumerate(word_mm):
                if char == MM.ngou_lonsum and word_mm[idx - 1] not in MM.cheitap_set_V:
                    fixed_chars_reverse += MM.nung
                else:
                    fixed_chars_reverse += char
            return fixed_chars_reverse
