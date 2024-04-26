from enum import Enum
from typing import Dict, Set, Tuple

from ..lon_ import Phoneme, BN, MM


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


class P2M:
    """Phoneme to Meetei Mayek"""

    original_map: Dict[Phoneme, Tuple[str, str, str]] = {
        Phoneme.k: (MM.kok, MM.kok_lonsum, MM.kok_lonsum),
        Phoneme.kh: (MM.khou, MM.khou, MM.kok_lonsum),
        Phoneme.g: (MM.gok, MM.gok, MM.kok_lonsum),
        Phoneme.gh: (MM.ghou, MM.ghou, MM.kok_lonsum),
        Phoneme.ng: (
            MM.ngou,
            MM.ngou_lonsum,
            MM.ngou_lonsum,
        ),
        Phoneme.c: (MM.chil, MM.chil, MM.chil),
        Phoneme.z: (MM.jil, MM.jil, MM.jil),
        Phoneme.zh: (MM.jham, MM.jham, MM.jil),
        Phoneme.t: (MM.til, MM.til_lonsum, MM.til_lonsum),
        Phoneme.th: (MM.thou, MM.thou, MM.til_lonsum),
        Phoneme.d: (MM.dil, MM.dil, MM.til_lonsum),
        Phoneme.dh: (MM.dhou, MM.dhou, MM.til_lonsum),
        Phoneme.n: (MM.na, MM.na_lonsum, MM.na_lonsum),
        Phoneme.p: (MM.pa, MM.pa_lonsum, MM.pa_lonsum),
        Phoneme.ph: (MM.pham, MM.pham, MM.pa_lonsum),
        Phoneme.b: (MM.ba, MM.ba, MM.pa_lonsum),
        Phoneme.bh: (MM.bham, MM.bham, MM.pa_lonsum),
        Phoneme.m: (MM.mit, MM.mit_lonsum, MM.mit_lonsum),
        Phoneme.j: (MM.yang, MM.i_lonsum, MM.i_lonsum),
        Phoneme.r: (MM.rai, MM.rai, MM.rai),
        Phoneme.w: (MM.wai, "", ""),
        Phoneme.l: (MM.lai, MM.lai_lonsum, MM.lai_lonsum),
        Phoneme.s: (MM.sam, MM.sam, MM.sam),
        Phoneme.h: (MM.huk, MM.huk, ""),
        # vowels - monophthongs
        Phoneme.i: (MM.i, MM.inap, MM.inap),
        Phoneme.e: (
            MM.atiya + MM.yenap,
            MM.yenap,
            MM.yenap,
        ),
        Phoneme.x: (MM.atiya, "", ""),
        Phoneme.u: (MM.un, MM.unap, MM.unap),
        Phoneme.o: (
            MM.atiya + MM.onap,
            MM.onap,
            MM.onap,
        ),
        Phoneme.a: (
            MM.atiya + MM.anap,
            MM.anap,
            MM.anap,
        ),
        # vowel - diphthongs
        Phoneme.ai: (
            MM.atiya + MM.anap + MM.i_lonsum,
            MM.anap + MM.i_lonsum,
            MM.anap + MM.i_lonsum,
        ),
        Phoneme.xi: (
            MM.atiya + MM.cheinap,
            MM.cheinap,
            MM.cheinap,
        ),
        Phoneme.ui: (
            MM.un + MM.i_lonsum,
            MM.unap + MM.i_lonsum,
            MM.unap + MM.i_lonsum,
        ),
        Phoneme.oi: (
            MM.atiya + MM.onap + MM.i_lonsum,
            MM.onap + MM.i_lonsum,
            MM.onap + MM.i_lonsum,
        ),
        Phoneme.au: (
            MM.atiya + MM.anap + MM.un,
            MM.anap + MM.un,
            MM.anap + MM.un,
        ),
        Phoneme.xu: (
            MM.atiya + MM.sounap,
            MM.sounap,
            MM.sounap,
        ),
    }

    mm_begin, mm_end, mm_end_2 = {}, {}, {}
    for phoneme, chars_mm in original_map.items():
        mm_begin[phoneme.value] = chars_mm[0]
        mm_end[phoneme.value] = chars_mm[1]
        mm_end_2[phoneme.value] = chars_mm[2]


class TUType(Enum):
    VI = "vowel initial/independent"
    VF = "vowel final/dependent"
    DI = "diphthong initial/independent"
    DF = "diphthong final/dependent"
    CI = "consonant initial/independent"
    CF = "consonant final/dependent"
    PI = "pure consonant initial/independent"
    PF = "pure consonant final/dependent"

    def get_spell_type(self) -> Tuple[bool, bool]:
        """Spell map based on TU type
            spell_type {True: mm_begin, False: mm_end}
            add_cluster_mark {True: map + apun, False: map}

        Returns:
            Tuple[bool, bool]: (spell_type, cluster_mark)
        """

        spell_type = self in [TUType.VI, TUType.DI, TUType.CI, TUType.PI]
        add_cluster_mark = self in [TUType.PI, TUType.PF]
        return spell_type, add_cluster_mark
