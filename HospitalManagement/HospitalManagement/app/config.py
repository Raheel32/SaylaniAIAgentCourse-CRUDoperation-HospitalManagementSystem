"""
config.py
---------
Loads configuration values (like the database URL) from a `.env` file
using pydantic-settings, instead of hardcoding them in the code.

Why do this instead of just writing the database URL directly in
database.py? Two reasons:
1. Security — your real database password should never be committed to
   Git / shared in a zip. It stays in `.env`, which is gitignored.
2. Flexibility — your teammates, or your deployment server, can use
   different credentials/host without touching any code.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # These names must match the variable names in your .env file exactly.
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url(self) -> str:
        """Builds the full SQLAlchemy connection string from the pieces above."""
        return (
            f"postgresql://{self.database_username}:{self.database_password}"
            f"@{self.database_hostname}:{self.database_port}/{self.database_name}"
        )


# A single, shared Settings instance the rest of the app imports.
settings = Settings()
