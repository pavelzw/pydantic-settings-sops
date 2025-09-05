import importlib.metadata
import warnings

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError as e:  # pragma: no cover
    warnings.warn(f"Could not determine version of {__name__}\n{e!s}", stacklevel=2)
    __version__ = "unknown"

from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings
from pydantic_settings.sources import (
    ConfigFileSourceMixin,
    InitSettingsSource,
)
from pydantic_settings.sources.types import DEFAULT_PATH, PathType
from sopsy import Sops


class SOPSConfigSettingsSource(InitSettingsSource, ConfigFileSourceMixin):
    """
    A simple settings source class that loads variables via SOPS.
    """

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        json_file: PathType | None = DEFAULT_PATH,
        yaml_file: PathType | None = DEFAULT_PATH,
    ):
        self.json_file_path = (
            json_file
            if json_file != DEFAULT_PATH
            else settings_cls.model_config.get("json_file")
        )
        self.yaml_file_path = (
            yaml_file
            if yaml_file != DEFAULT_PATH
            else settings_cls.model_config.get("yaml_file")
        )
        self.data = self._read_files(self.json_file_path)
        self.data |= self._read_files(self.yaml_file_path)
        super().__init__(settings_cls, self.data)

    def _read_file(self, file_path: Path) -> dict[str, Any]:
        sops = Sops(file_path)
        decrypted = sops.decrypt(to_dict=True)
        assert isinstance(decrypted, dict)
        return decrypted
