import os
from typing import Optional

# from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

	# Database settings
	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str
	DB_PORT: str
	DB_NAME: str

	DATABASE_URL: Optional[str] = None

	@model_validator(mode='after')
	def get_database_url(self) -> 'Settings':
		if self.DATABASE_URL is None:
			self.DATABASE_URL = (
				f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
			)
		return self


settings = Settings()  # pylint: disable=no-value-for-parameter
