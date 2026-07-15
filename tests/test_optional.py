import pytest
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from pydantic_settings_sops import SopsJsonSettingsSource, SopsYamlSettingsSource


class ExampleSettingsYaml(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=[
            "tests/resources/secrets.yaml",
            "tests/resources/secrets2.yaml",
            "tests/resources/unencrypted.yaml",
        ]
    )

    foobar: str
    foobar2: str
    answer: int

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, SopsYamlSettingsSource(settings_cls)


class ExampleSettingsJson(BaseSettings):
    model_config = SettingsConfigDict(
        json_file=[
            "tests/resources/secrets.json",
            "tests/resources/secrets2.json",
            "tests/resources/unencrypted.json",
        ]
    )

    foobar: str
    foobar2: str
    answer: int

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, SopsJsonSettingsSource(settings_cls)


@pytest.mark.parametrize("settings_cls", [ExampleSettingsYaml, ExampleSettingsJson])
def test_basic_settings(settings_cls):
    settings = settings_cls()
    assert settings.foobar == "foo"
    assert settings.foobar2 == "foo"
    assert settings.answer == 42


@pytest.mark.parametrize("settings_cls", [ExampleSettingsYaml, ExampleSettingsJson])
def test_settings_with_override(settings_cls):
    settings2 = settings_cls(foobar="bar")
    assert settings2.foobar == "bar"
    assert settings2.foobar2 == "foo"
    assert settings2.answer == 42
