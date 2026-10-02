from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Conexion a la base de datos MySQL (las tablas ya existen, creadas con tu script SQL)
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/reservas_salas"
    SECRET_KEY: str = "cambia-esta-clave-super-secreta-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Horario institucional (regla de negocio R1)
    HORA_APERTURA: str = "07:00"
    HORA_CIERRE: str = "21:30"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()