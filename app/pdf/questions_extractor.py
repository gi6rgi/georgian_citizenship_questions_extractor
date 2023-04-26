from typing import Union, Dict, List
from abc import ABC, abstractmethod

from PyPDF2 import PdfReader

from schemas.question import Question


class Extractor(ABC):
    def __init__(self, file_path: str) -> None:
        self.question_counter = 1
        self.pdf_reader = PdfReader(file_path)
        self.all_pdf_lines = [line.lstrip().rstrip() for page in self.pdf_reader.pages for line in page.extract_text().split("\n") if line != " "]
    
    @abstractmethod
    def find_answers(self, start_line: int) -> Dict[str, Union[str, List[str]]]:
        pass

    def extract_questions_from_page(self):
        questions = []
        line_number = 0
        for line in self.all_pdf_lines:
            line_number += 1
            if f"{self.question_counter}." in line:
                self.question_counter += 1
                questions_and_answers = self.find_answers(line_number)
                if ")" not in self.all_pdf_lines[line_number] and "ტესტები" not in self.all_pdf_lines[line_number]:
                    line += f" {self.all_pdf_lines[line_number]}"
                questions.append(Question(id=self.question_counter, text=line, **questions_and_answers))
        return questions

    def extract(self):
        return self.extract_questions_from_page()


class LawQuestionsExtractor(Extractor):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def find_answers(self, start_line: int) -> Dict[str, str | List[str]]:
        ...


class HistoryQuestionsExtractor(Extractor):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
    
    def find_answers(self, start_line: int) -> Dict[str, Union[str, List[str]]]:
        answers_counter = 4
        answers = []
        for line in self.all_pdf_lines[start_line:]:
            if answers_counter == 0 and ")" in line:
                correct_answer = line.split(")")[0][-1]
                return {"answers": answers, "correct_answer": correct_answer}
            if ")" in line:
                answers.append(line)
                answers_counter -= 1


class LanguageQuestionsExtractor(Extractor):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
    
    def find_answers(self, start_line: int) -> Dict[str, str | List[str]]:
        answers_counter = 4
        answers = []
        for line in self.all_pdf_lines[start_line:]:
            if answers_counter == 0 and "სწორი" in line:
                correct_answer = line[-1]
                return {"answers": answers, "correct_answer": correct_answer}
            if line[1:2] == "." and not line.startswith("."):
                answers.append(line)
                answers_counter -= 1


class QuestionsPdfExtractor:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.mapper = {"law": LawQuestionsExtractor, "history": HistoryQuestionsExtractor, "language": LanguageQuestionsExtractor}
        self.extractor = self.create_extractor(file_path)

    def create_extractor(self, file_path: str) -> Union[HistoryQuestionsExtractor, LawQuestionsExtractor, LanguageQuestionsExtractor]:
        file_type = file_path.split("/")[-1].split(".")[0]
        return self.mapper[file_type](file_path)

    def extract(self):
        return self.extractor.extract()
