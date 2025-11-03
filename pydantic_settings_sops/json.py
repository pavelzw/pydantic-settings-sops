from pydantic_settings import BaseSettings, JsonConfigSettingsSource
from pydantic_settings.sources import DEFAULT_PATH, PathType

from .mixin import SopsConfigFileSourceMixin


class SopsJsonSettingsSource(SopsConfigFileSourceMixin, JsonConfigSettingsSource):
    """
    A source that contains variables on a optionally encrypted SOPS JSON file
    """

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        json_file: PathType | None = DEFAULT_PATH,
        json_file_encoding: str | None = None,
        *,
        allow_unencrypted: bool = True,
    ):
        self.allow_unencrypted = allow_unencrypted
        super().__init__(settings_cls, json_file, json_file_encoding)
