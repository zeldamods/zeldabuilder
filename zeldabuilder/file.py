import abc
from pathlib import Path
import re
import typing

import sarc
import wszst_yaz0

class FileDevice(abc.ABC):
    @abc.abstractmethod
    def list_files(self) -> typing.Iterable[Path]:
        pass

    @abc.abstractmethod
    def read_file(self, path: Path) -> bytes:
        pass

    def read_file_and_decomp(self, path: Path) -> bytes:
        data = self.read_file(path)
        if path.suffix.startswith(".s"):
            return wszst_yaz0.decompress(data)
        return data

class FileDeviceHostDirectory(FileDevice):
    def __init__(self, base_dir: Path):
        self._base_dir = base_dir

    def list_files(self) -> typing.Iterable[Path]:
        for p in self._base_dir.glob("**/*"):
            if not p.is_dir():
                yield p.relative_to(self._base_dir)

    def read_file(self, path: Path):
        with (self._base_dir / path).open("rb") as f:
            return f.read()

class FileDeviceArchive(FileDevice):
    def __init__(self, archive: sarc.SARC):
        self._archive = archive

    def list_files(self) -> typing.Iterable[Path]:
        for name in self._archive.list_files():
            yield Path(name)

    def read_file(self, path: Path):
        return bytes(self._archive.get_file_data(path.as_posix()))

def remove_extension_prefix_char_from_path(path: Path, prefix_char: str) -> Path:
    if path.suffix.startswith("." + prefix_char):
        return path.with_suffix("." + path.suffix[2:])
    return path

_weird_extension_pairs = [
    (".yml.yml", ".yml"),
    (".xml.yml", ".yml"),
]
def fix_weird_looking_extensions(path: Path) -> Path:
    str_path = str(path)
    str_path = re.sub(".yml.yml$", ".yml", str_path)
    str_path = re.sub(".xml.yml$", ".yml", str_path)
    return Path(str_path)
