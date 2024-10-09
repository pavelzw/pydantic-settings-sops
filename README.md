# pydantic-settings-sops

[![CI](https://img.shields.io/github/actions/workflow/status/pavelzw/pydantic-settings-sops/ci.yml?style=flat-square&branch=main)](https://github.com/pavelzw/pydantic-settings-sops/actions/workflows/ci.yml)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/pydantic-settings-sops?logoColor=white&logo=conda-forge&style=flat-square)](https://prefix.dev/channels/conda-forge/packages/pydantic-settings-sops)
[![pypi-version](https://img.shields.io/pypi/v/pydantic-settings-sops.svg?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/pydantic-settings-sops)
[![python-version](https://img.shields.io/pypi/pyversions/pydantic-settings-sops?logoColor=white&logo=python&style=flat-square)](https://pypi.org/project/pydantic-settings-sops)

SOPS extension for `pydantic-settings`.

This package allows you to read SOPS files into a `pydantic-settings` object.

You can install this package via

```bash
pip install pydantic-settings-sops
# or
pixi add pydantic-settings-sops
```

## Example

To use pydantic-settings-sops, adjust your settings sources by defining a custom `settings_customise_sources`.
For more information on `pydantic-settings`, please visit the [official documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings).

```py
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pydantic_settings_sops import SOPSConfigSettingsSource

class SettingsExample(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file="secrets.yaml"
    )

    foobar: str

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
```

## Installation

This project is managed by [pixi](https://pixi.sh).
You can install the package in development mode using:

```bash
git clone https://github.com/pavelzw/pydantic-settings-sops
cd pydantic-settings-sops

pixi run pre-commit-install
pixi run postinstall
pixi run test
```
