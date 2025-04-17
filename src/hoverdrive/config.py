"""Configuration definition."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from safir.logging import LogLevel, Profile

__all__ = ["Config", "config"]


class Config(BaseSettings):
    """Configuration for hoverdrive."""

    model_config = SettingsConfigDict(
        env_prefix="HOVERDRIVE_", case_sensitive=False
    )

    log_level: LogLevel = Field(
        LogLevel.INFO, title="Log level of the application's logger"
    )

    name: str = Field("hoverdrive", title="Name of application")

    path_prefix: str = Field("/hoverdrive", title="URL prefix for application")

    profile: Profile = Field(
        Profile.development, title="Application logging profile"
    )

    slack_webhook: SecretStr | None = Field(
        None,
        title="Slack webhook for alerts",
        description="If set, alerts will be posted to this Slack webhook",
    )

    ook_url: str = Field(
        "https://roundtable.lsst.cloud/ook",
        description="Base URL for the Ook API",
    )


config = Config()
"""Configuration for hoverdrive."""
