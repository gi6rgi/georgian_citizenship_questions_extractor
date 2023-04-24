from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    mongo_connection_string: str = Field(default="")
    language_pdf_path: str = Field(default="/Users/georgii/Code/georgian_quiz/app/tests/language.pdf")
    history_pdf_path: str = Field(default="/Users/georgii/Code/georgian_quiz/app/tests/history.pdf")
    law_pdf_path: str = Field(default="/Users/georgii/Code/georgian_quiz/app/tests/law.pdf")


settings = Settings()
