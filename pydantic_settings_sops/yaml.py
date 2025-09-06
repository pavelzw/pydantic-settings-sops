from pydantic_settings import BaseSettings, YamlConfigSettingsSource
from pydantic_settings.sources import DEFAULT_PATH, PathType

from .mixin import SopsConfigFileSourceMixin


class SopsYamlSettingsSource(SopsConfigFileSourceMixin, YamlConfigSettingsSource):
    """
    A source that contains variables on a optionally encrypted SOPS YAML file
    """

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        yaml_file: PathType | None = DEFAULT_PATH,
        yaml_file_encoding: str | None = None,
        yaml_config_section: str | None = None,
        *,
        allow_unencrypted: bool = True,
    ):
        self.allow_unencrypted = allow_unencrypted
        super().__init__(
            settings_cls, yaml_file, yaml_file_encoding, yaml_config_section
        )
