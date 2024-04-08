from typing import Dict, Set

from ..lon_ import Bengali, MeeteiMayek


class Baseline:
    """
    Bengali to Meetei Mayek
    Replication of Nongmeikapam et. al.'s work
    """

    def __init__(self) -> None:
        bn = Bengali()
        mm = MeeteiMayek()

        iyek_ipee: Dict[str, Set[str]] = {
            mm.letter_kok: {bn.letter_ka},
            mm.letter_sam: {bn.letter_cha, bn.letter_ssa, bn.letter_sa, bn.letter_sha},
            mm.letter_lai: {bn.letter_la},
            mm.letter_mit: {bn.letter_ma},
            mm.letter_pa: {bn.letter_pa},
            mm.letter_na: {bn.letter_nya, bn.letter_nna, bn.letter_na},
            mm.letter_chil: {bn.letter_ca},
            mm.letter_til: {bn.letter_tta, bn.letter_ta, bn.letter_khanda_ta},
            mm.letter_khou: {bn.letter_kha},
            mm.letter_ngou: {bn.sign_anusvara, bn.letter_nga},
            mm.letter_thou: {bn.letter_ttha, bn.letter_tha},
            mm.letter_wai: {bn.letter_w},
            mm.letter_yang: {bn.letter_yya, bn.letter_ya},
            mm.letter_huk: {bn.letter_h},
            mm.letter_un: {bn.letter_u, bn.letter_uu},
            mm.letter_i: {bn.letter_i, bn.letter_ii},
            mm.letter_pham: {bn.letter_pha},
            mm.letter_a: {bn.letter_a},
            mm.letter_gok: {bn.letter_ga},
            mm.letter_jham: {bn.letter_jha},
            mm.letter_rai: {
                bn.letter_r_vocalic,
                bn.vowel_r_vocalic,
                bn.letter_rra,
                bn.letter_ra,
                bn.letter_rha,
            },
            mm.letter_ba: {bn.letter_ba},
            mm.letter_jil: {bn.letter_ja},
            mm.letter_dil: {bn.letter_dda, bn.letter_da},
            mm.letter_ghou: {bn.letter_gha},
            mm.letter_dhou: {bn.letter_ddha, bn.letter_dha},
            mm.letter_bham: {bn.letter_bha},
        }

        vowel_letters: Dict[str, Set[str]] = {
            f"{mm.letter_atiya}{mm.vowel_anap}": {bn.letter_aa},
            f"{mm.letter_atiya}{mm.vowel_yenap}": {bn.letter_e},
            f"{mm.letter_atiya}{mm.vowel_cheinap}": {bn.letter_ai},
            f"{mm.letter_atiya}{mm.vowel_onap}": {bn.letter_o},
            f"{mm.letter_atiya}{mm.vowel_sounap}": {bn.letter_ao},
            f"{mm.letter_atiya}{mm.vowel_nung}": {f"{bn.letter_aa}{bn.sign_anusvara}"},
        }

        cheitap_iyek: Dict[str, Set[str]] = {
            mm.vowel_onap: {bn.vowel_o},
            mm.vowel_inap: {bn.vowel_i, bn.vowel_ii},
            mm.vowel_anap: {bn.vowel_aa},
            mm.vowel_yenap: {bn.vowel_e},
            mm.vowel_sounap: {bn.vowel_au},
            mm.vowel_unap: {bn.vowel_u, bn.vowel_uu},
            mm.vowel_cheinap: {bn.vowel_ai},
            mm.vowel_nung: {bn.sign_anusvara},
        }

        cheising_iyek: Dict[str, Set[str]] = {
            mm.digit_one: {bn.digit_one},
            mm.digit_two: {bn.digit_two},
            mm.digit_three: {bn.digit_three},
            mm.digit_four: {bn.digit_four},
            mm.digit_five: {bn.digit_five},
            mm.digit_six: {bn.digit_six},
            mm.digit_seven: {bn.digit_seven},
            mm.digit_eight: {bn.digit_eight},
            mm.digit_nine: {bn.digit_nine},
            mm.digit_zero: {bn.digit_zero},
        }

        lonsum_iyek: Dict[str, Set[str]] = {
            mm.letter_kok_lonsum: {f"{bn.letter_ka}{bn.sign_virama}"},
            mm.letter_lai_lonsum: {f"{bn.letter_la}{bn.sign_virama}"},
            mm.letter_mit_lonsum: {f"{bn.letter_ma}{bn.sign_virama}"},
            mm.letter_pa_lonsum: {f"{bn.letter_pa}{bn.sign_virama}"},
            mm.letter_na_lonsum: {
                f"{bn.letter_nna}{bn.sign_virama}",
                f"{bn.letter_na}{bn.sign_virama}",
            },
            mm.letter_til_lonsum: {
                f"{bn.letter_tta}{bn.sign_virama}",
                f"{bn.letter_ta}{bn.sign_virama}",
            },
            mm.letter_ngou_lonsum: {f"{bn.letter_nga}{bn.sign_virama}"},
        }

        self.original_map = {
            **iyek_ipee,
            **vowel_letters,
            **cheitap_iyek,
            **cheising_iyek,
            **lonsum_iyek,
        }

        self.charmap: Dict[str, str] = {
            char_bn: char_mm
            for char_mm, char_bn_list in self.original_map.items()
            for char_bn in char_bn_list
        }


class BaselineExtended:
    """
    Bengali to Meetei Mayek
    Added Gyanendro et. al.'s work
    """

    def __init__(self) -> None:
        bn = Bengali()
        mm = MeeteiMayek()
        self.extra_charmap = {
            f"{bn.sign_virama}{bn.letter_ya}": f"{mm.apun_iyek}{mm.letter_yang}",
            f"{bn.sign_virama}{bn.letter_yya}": f"{mm.apun_iyek}{mm.letter_yang}",
            f"{bn.sign_virama}{bn.letter_ra}": f"{mm.apun_iyek}{mm.letter_rai}",
            f"{bn.sign_virama}{bn.letter_rha}": f"{mm.apun_iyek}{mm.letter_rai}",
            f"{bn.sign_virama}{bn.letter_rra}": f"{mm.apun_iyek}{mm.letter_rai}",
            f"{bn.sign_virama}{bn.letter_la}": f"{mm.apun_iyek}{mm.letter_lai}",
            f"{bn.sign_virama}{bn.letter_w}": f"{mm.apun_iyek}{mm.letter_wai}",
        }
