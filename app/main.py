import json

from pymongo import MongoClient

from core.settings import settings
from pdf.questions_extractor import QuestionsPdfExtractor


client = MongoClient(settings.mongo_connection_string)

history_questions = QuestionsPdfExtractor(settings.history_pdf_path).extract()
history_questions = [json.loads(question.json()) for question in history_questions]
language_questions = QuestionsPdfExtractor(settings.language_pdf_path).extract()
language_questions = [json.loads(question.json()) for question in language_questions]

law_table = client.georgian_tests.law
history_table = client.georgian_tests.history
language_table = client.georgian_tests.language

history_table.insert_many(history_questions)
language_table.insert_many(language_questions)
