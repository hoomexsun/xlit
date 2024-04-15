from typing import Dict, Set

from ..lon_ import Bengali, MeeteiMayek


class BaselineTU:
    """
    Bengali to Meetei Mayek
    Replication of Doren's work
    """

    def __init__(self) -> None:
        bn = Bengali()
        mm = MeeteiMayek()

        self.charmap: Dict[str, str] = {}
        self.sorted_keys = sorted(self.charmap.keys(), key=len, reverse=True)

    def transliterate(self, word_bn: str):
        word_mm = word_bn
        for key in self.sorted_keys:
            word_mm = word_mm.replace(key, self.charmap[key])
        return word_mm
