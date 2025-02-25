from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_user: str
    rabbitmq_password: str

    translator_url: str

    date_format: str = '%Y-%m-%d'
    date_time_format: str = '%Y-%m-%d %H:%M'

    model_config = SettingsConfigDict(env_file='.env')

    def get_rabbitmq_uri(self):
        return f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}"

settings = Settings()
