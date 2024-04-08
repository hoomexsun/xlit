from enum import Enum


class PoA(Enum):
    """Place of Articulation Enum"""

    BILABIAL = "bilabial"
    ALVEOLAR = "alveolar"
    PALATAL = "palatal"
    VELAR = "velar"
    GLOTTAL = "glottal"
    UNDEFINED = ""


class MoA(Enum):
    """Manner of Articulation"""

    NASAL = "nasal"
    PLOSIVE = "plosive"
    FRICATIVE = "fricative"
    APPROXIMANT = "approximant"
    TAP_FLAP = "tap/flap"
    TRILL = "trill"
    LATERAL_FRICATIVE = "lateral fricative"
    LATERAL_APPROXIMANT = "lateral approximant"
    LATEAL_TAP_FLAP = "lateral tap/flap"
    UNDEFINED = ""


class Sievers(Enum):
    """Sonority classes for SSP (Sievers 1876) based on relative loudness.

    Args:
        Enum (int): ssp value
    """

    PHONE_S: int = 0
    OBSTRUENT: int = 1
    NASAL: int = 2
    LIQUID: int = 3
    GLIDE: int = 4


class Parker(Enum):
    """Sonority classes for SSP (Parker 2002) based on acoustic intensity.

    Args:
        Enum (int): ssp value
    """

    VCL_STOP: int = 0
    VCL_FRICATIVE: int = 1
    VCD_STOP: int = 2
    VCD_FRICATIVE: int = 3
    PHONE_H: int = 4
    NASAL: int = 5
    TRILL: int = 6
    FLAP: int = 7
    LATERAL: int = 8
    RHOTIC: int = 9
    GLIDE: int = 10


class VowelTongue(Enum):
    """Tongue position of Articulation

    Args:
        enum (int): value
    """

    FRONT: int = 0
    CENTRAL: int = 1
    BACK: int = 2


class VowelMouth(Enum):
    """Articulation from mouth

    Args:
        enum (int): value
    """

    CLOSE: int = 0
    MID: int = 1
    OPEN: int = 2


class VowelLips(Enum):
    """Whether lips is rounded

    Args:
        enum (bool): value
    """

    ROUNDED: bool = True
    NOT_ROUNDED: bool = False


class Phoneme(Enum):
    """Define the 36 phonemes of Meetei Mayek.

    Args:
        Enum (str): phoneme values
    """

    k: str = "K"
    kh: str = "KH"
    g: str = "G"
    gh: str = "GH"
    ng: str = "NG"
    c: str = "C"
    z: str = "Z"
    zh: str = "ZH"
    t: str = "T"
    th: str = "TH"
    d: str = "D"
    dh: str = "DH"
    n: str = "N"
    p: str = "P"
    ph: str = "PH"
    b: str = "B"
    bh: str = "BH"
    m: str = "M"
    j: str = "J"
    r: str = "R"
    w: str = "W"
    l: str = "L"
    s: str = "S"
    h: str = "H"
    i: str = "I"
    e: str = "E"
    a: str = "A"
    x: str = "X"
    u: str = "U"
    o: str = "O"
    ai: str = "AI"
    xi: str = "XI"
    ui: str = "UI"
    oi: str = "OI"
    au: str = "AU"
    xu: str = "XU"
