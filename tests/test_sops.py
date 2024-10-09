from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from pydantic_settings_sops import SOPSConfigSettingsSource


def test_get_settings():
    settings = TestSettings()
    assert settings.foobar == "foo"
    assert settings.foobar2 == "foo"

    settings2 = TestSettings(foobar="bar")
    assert settings2.foobar == "bar"
    assert settings2.foobar2 == "foo"


class TestSettings(BaseSettings):
    # todo: add json tests: https://github.com/nikaro/sopsy/issues/73
    model_config = SettingsConfigDict(
        yaml_file=["tests/resources/secrets.yaml", "tests/resources/secrets2.yaml"]
    )

    foobar: str
    foobar2: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: BaseSettings,
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, SOPSConfigSettingsSource(settings_cls))
