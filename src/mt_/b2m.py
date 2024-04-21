from typing import Dict, Set, Tuple

from ..lon_ import Phoneme, Bengali, MeeteiMayek


class B2P:
    """Bengali to Phoneme"""

    def __init__(self) -> None:
        bn = Bengali()

        p2b_charmap: Dict[str, Set[str]] = {
            Phoneme.k: {bn.letter_ka},
            Phoneme.kh: {bn.letter_kha},
            Phoneme.g: {bn.letter_ga},
            Phoneme.gh: {bn.letter_gha},
            Phoneme.ng: {bn.sign_anusvara, bn.letter_nga},
            Phoneme.c: {bn.letter_ca},
            Phoneme.z: {bn.letter_ja},
            Phoneme.zh: {bn.letter_jha},
            Phoneme.t: {bn.letter_tta, bn.letter_ta, bn.letter_khanda_ta},
            Phoneme.th: {bn.letter_ttha, bn.letter_tha},
            Phoneme.d: {bn.letter_dda, bn.letter_da},
            Phoneme.dh: {bn.letter_ddha, bn.letter_dha},
            Phoneme.n: {bn.letter_nya, bn.letter_nna, bn.letter_na},
            Phoneme.p: {bn.letter_pa},
            Phoneme.ph: {bn.letter_pha},
            Phoneme.b: {bn.letter_ba},
            Phoneme.bh: {bn.letter_bha},
            Phoneme.m: {bn.letter_ma},
            Phoneme.j: {bn.letter_yya, bn.letter_ya},
            Phoneme.r: {
                bn.letter_r_vocalic,
                bn.vowel_r_vocalic,
                bn.letter_rra,
                bn.letter_ra,
                bn.letter_rha,
            },
            Phoneme.w: {bn.letter_w},
            Phoneme.l: {bn.letter_la},
            Phoneme.s: {bn.letter_cha, bn.letter_ssa, bn.letter_sa, bn.letter_sha},
            Phoneme.h: {bn.letter_h},
            # vowels - monophthongs
            Phoneme.i: {bn.letter_i, bn.letter_ii, bn.vowel_i, bn.vowel_ii},
            Phoneme.e: {bn.letter_e, bn.vowel_e},
            Phoneme.x: {bn.letter_a},
            Phoneme.u: {bn.letter_u, bn.letter_uu, bn.vowel_u, bn.vowel_uu},
            Phoneme.o: {bn.letter_o, bn.vowel_o},
            Phoneme.a: {bn.letter_aa, bn.vowel_aa},
            # vowel - diphthongs
            Phoneme.ai: bn.initial_ai | bn.final_ai,
            Phoneme.xi: bn.initial_xi | bn.final_xi,
            Phoneme.ui: bn.initial_ui | bn.final_ui,
            Phoneme.oi: bn.initial_oi | bn.final_oi,
            Phoneme.au: bn.initial_au | bn.final_au,
            Phoneme.xu: bn.initial_xu | bn.final_xu,
        }

        self.p2b_charmap: Dict[str, Set[str]] = {
            phoneme.value: char_bn_list for phoneme, char_bn_list in p2b_charmap.items()
        }

        self.charmap: Dict[str, str] = {
            char_bn: phoneme
            for phoneme, char_bn_list in self.p2b_charmap.items()
            for char_bn in char_bn_list
        }


class P2M:
    """Phoneme to Meetei Mayek"""

    def __init__(self) -> None:
        mm = MeeteiMayek()
        original_map: Dict[str, Tuple[str, str, str]] = {
            Phoneme.k: (mm.letter_kok, mm.letter_kok_lonsum, mm.letter_kok_lonsum),
            Phoneme.kh: (mm.letter_khou, mm.letter_khou, mm.letter_kok_lonsum),
            Phoneme.g: (mm.letter_gok, mm.letter_gok, mm.letter_kok_lonsum),
            Phoneme.gh: (mm.letter_ghou, mm.letter_ghou, mm.letter_kok_lonsum),
            Phoneme.ng: (
                mm.letter_ngou,
                mm.letter_ngou_lonsum,
                mm.letter_ngou_lonsum,
            ),
            Phoneme.c: (mm.letter_chil, mm.letter_chil, mm.letter_chil),
            Phoneme.z: (mm.letter_jil, mm.letter_jil, mm.letter_jil),
            Phoneme.zh: (mm.letter_jham, mm.letter_jham, mm.letter_jil),
            Phoneme.t: (mm.letter_til, mm.letter_til_lonsum, mm.letter_til_lonsum),
            Phoneme.th: (mm.letter_thou, mm.letter_thou, mm.letter_til_lonsum),
            Phoneme.d: (mm.letter_dil, mm.letter_dil, mm.letter_til_lonsum),
            Phoneme.dh: (mm.letter_dhou, mm.letter_dhou, mm.letter_til_lonsum),
            Phoneme.n: (mm.letter_na, mm.letter_na_lonsum, mm.letter_na_lonsum),
            Phoneme.p: (mm.letter_pa, mm.letter_pa_lonsum, mm.letter_pa_lonsum),
            Phoneme.ph: (mm.letter_pham, mm.letter_pham, mm.letter_pa_lonsum),
            Phoneme.b: (mm.letter_ba, mm.letter_ba, mm.letter_pa_lonsum),
            Phoneme.bh: (mm.letter_bham, mm.letter_bham, mm.letter_pa_lonsum),
            Phoneme.m: (mm.letter_mit, mm.letter_mit_lonsum, mm.letter_mit_lonsum),
            Phoneme.j: (mm.letter_yang, mm.letter_i_lonsum, mm.letter_i_lonsum),
            Phoneme.r: (mm.letter_rai, mm.letter_rai, mm.letter_rai),
            Phoneme.w: (mm.letter_wai, "", ""),
            Phoneme.l: (mm.letter_lai, mm.letter_lai_lonsum, mm.letter_lai_lonsum),
            Phoneme.s: (mm.letter_sam, mm.letter_sam, mm.letter_sam),
            Phoneme.h: (mm.letter_huk, "", ""),
            # vowels - monophthongs
            Phoneme.i: (mm.letter_i, mm.vowel_inap, mm.vowel_inap),
            Phoneme.e: (
                f"{mm.letter_atiya}{mm.vowel_yenap}",
                mm.vowel_yenap,
                mm.vowel_yenap,
            ),
            Phoneme.x: (mm.letter_atiya, "", ""),
            Phoneme.u: (mm.letter_un, mm.vowel_unap, mm.vowel_unap),
            Phoneme.o: (
                f"{mm.letter_atiya}{mm.vowel_onap}",
                mm.vowel_onap,
                mm.vowel_onap,
            ),
            Phoneme.a: (
                f"{mm.letter_atiya}{mm.vowel_anap}",
                mm.vowel_anap,
                mm.vowel_anap,
            ),
            # vowel - diphthongs
            Phoneme.ai: (
                f"{mm.letter_atiya}{mm.vowel_anap}{mm.letter_i_lonsum}",
                f"{mm.vowel_anap}{mm.letter_i_lonsum}",
                f"{mm.vowel_anap}{mm.letter_i_lonsum}",
            ),
            Phoneme.xi: (
                f"{mm.letter_atiya}{mm.vowel_cheinap}",
                mm.vowel_cheinap,
                mm.vowel_cheinap,
            ),
            Phoneme.ui: (
                f"{mm.letter_un}{mm.letter_i_lonsum}",
                f"{mm.vowel_unap}{mm.letter_i_lonsum}",
                f"{mm.vowel_unap}{mm.letter_i_lonsum}",
            ),
            Phoneme.oi: (
                f"{mm.letter_atiya}{mm.vowel_onap}{mm.letter_i_lonsum}",
                f"{mm.vowel_onap}{mm.letter_i_lonsum}",
                f"{mm.vowel_onap}{mm.letter_i_lonsum}",
            ),
            Phoneme.au: (
                f"{mm.letter_atiya}{mm.vowel_anap}{mm.letter_un}",
                f"{mm.vowel_anap}{mm.letter_un}",
                f"{mm.vowel_anap}{mm.letter_un}",
            ),
            Phoneme.xu: (
                f"{mm.letter_atiya}{mm.vowel_sounap}",
                mm.vowel_sounap,
                mm.vowel_sounap,
            ),
        }

        self.mm_begin, self.mm_end, self.mm_end_2 = {}, {}, {}
        for phoneme, chars_mm in original_map.items():
            self.mm_begin[phoneme.value] = chars_mm[0]
            self.mm_end[phoneme.value] = chars_mm[1]
            self.mm_end_2[phoneme.value] = chars_mm[2]


class BnErrors:
    def __init__(self) -> None:
        bn = Bengali()
        self.errors_map_unic: Dict[str, str] = {
            f"{bn.vowel_aa}{bn.vowel_e}": bn.vowel_o,
            f"{bn.vowel_e}{bn.vowel_aa}": bn.vowel_o,
            f"{bn.vowel_aa}{bn.mark_au}": bn.vowel_au,
            f"{bn.mark_au}{bn.vowel_aa}": bn.vowel_au,
            f"{bn.letter_dda}{bn.sign_nukta}": bn.letter_rra,
            f"{bn.letter_ddha}{bn.sign_nukta}": bn.letter_rha,
            f"{bn.letter_ya}{bn.sign_nukta}": bn.letter_yya,
        }
        self.errors_map_type: Dict[str, str] = {
            f"{bn.vowel_aa}{bn.vowel_aa}": bn.vowel_aa,
            f"{bn.vowel_i}{bn.vowel_ii}": bn.vowel_ii,
            f"{bn.vowel_ii}{bn.vowel_i}": bn.vowel_ii,
        }
        self.charmap = {
            **self.errors_map_unic,
            **self.errors_map_type,
        }
        # Valid set 1
        self.valid_letters_set: Set[str] = bn.independent_consonant_set.union(
            bn.dependent_consonant_set,
            bn.independent_vowel_set,
            bn.dependent_vowel_set,
            {bn.sign_virama},
        )

    def filter_valid_bengali_letters(self, word):
        return "".join([char for char in word if char in self.valid_letters_set])
