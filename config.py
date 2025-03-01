from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_user: str
    rabbitmq_password: str

    openai_endpoint: str
    openai_api_key: str
    openai_default_model: str

    translator_url: str
    
    tasks_queue: str = "tasks"
    tasks_statuses_queue: str = "task_statuses"

    date_format: str = '%Y-%m-%d'
    date_time_format: str = '%Y-%m-%d %H:%M'

    model_config = SettingsConfigDict(env_file='.env')

    def get_rabbitmq_uri(self):
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}"

settings = Settings()
