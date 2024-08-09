from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    user: str
    password: str
    host: str
    port: int
    database: str

    @staticmethod
    def from_env(env: Env):
        return DbConfig(
            user=env.str("MYSQL_USER"),
            password=env.str("MYSQL_PASSWORD"),
            host=env.str("DB_HOST", default="db"),
            port=env.int("DB_PORT", default=3306),
            database=env.str("MYSQL_DATABASE"),
        )

    def get_connection_string(self) -> str:
        return f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class Config:
    db: DbConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(db=DbConfig.from_env(env))
