from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from pydantic_settings_sops import SOPSConfigSettingsSource


def test_settings_yaml():
    settings = ExampleSettingsYaml()
    assert settings.foobar == "foo"
    assert settings.foobar2 == "foo"

    settings2 = ExampleSettingsYaml(foobar="bar")
    assert settings2.foobar == "bar"
    assert settings2.foobar2 == "foo"


def test_settings_json():
    settings = ExampleSettingsJson()
    assert settings.foobar == "foo"
    assert settings.foobar2 == "foo"

    settings2 = ExampleSettingsJson(foobar="bar")
    assert settings2.foobar == "bar"
    assert settings2.foobar2 == "foo"


class ExampleSettingsYaml(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=["tests/resources/secrets.yaml", "tests/resources/secrets2.yaml"]
    )

    foobar: str
    foobar2: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, SOPSConfigSettingsSource(settings_cls))


class ExampleSettingsJson(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=["tests/resources/secrets.json", "tests/resources/secrets2.json"]
    )

    foobar: str
    foobar2: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: BaseSettings,  # type: ignore[override]
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, SOPSConfigSettingsSource(settings_cls))
