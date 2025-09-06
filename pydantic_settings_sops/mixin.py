from abc import ABC
from pathlib import Path
from typing import Any

from pydantic_settings.sources import ConfigFileSourceMixin
from sopsy import Sops, SopsyCommandFailedError


class SopsConfigFileSourceMixin(ConfigFileSourceMixin, ABC):
    """
    Mixin for reading configuration files optionally encrypted with SOPS.
    """

    allow_unencrypted: bool = True

    def _read_file(self, file_path: Path) -> dict[str, Any]:
        try:
            sops = Sops(file_path)
            decrypted = sops.decrypt(to_dict=True)
            assert isinstance(decrypted, dict)
            return decrypted
        except SopsyCommandFailedError as exc:
            if self.allow_unencrypted and "sops metadata not found" in str(exc):
                return super()._read_file(file_path)  # type: ignore[safe-super]
            raise
