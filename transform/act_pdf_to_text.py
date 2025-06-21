from io import FileIO
import logging
from pypdf import PdfReader


class PdfToTextException(Exception):
    pass


class PageHeaderNotFound(PdfToTextException):
    """Not found expected page header."""

    def __init__(self, message: str):
        super().__init__(message)


def text_as_hex(text: str) -> str:
    buf = ""
    for char in text:
        buf += f"\n'{char}' = {ord(char):x} hex"
    return buf


def act_pdf_to_text(pdf_file: FileIO, act_position: int) -> str:
    """Transform Sejm act PDF to text."""
    page_header_marks = [
        f"Poz. {act_position}",
        f"Poz.\xa0{act_position}",
        f"Poz. \xa0{act_position}",
        "Poz. 000 ",
        f"Poz.{act_position}",
        f"Poz.  {act_position}",
    ]

    reader = PdfReader(pdf_file)
    text = ""
    number_of_pages = len(reader.pages)
    page_number = 0
    for page in reader.pages:
        page_number += 1
        if number_of_pages > 10 and page_number % 10 == 0:
            logging.info(f"Processing page {page_number}/{number_of_pages}")

        page_text = page.extract_text()

        if page_number > 1:
            for page_header_mark in page_header_marks:
                page_header_pos = page_text.find(page_header_mark)
                if page_header_pos != -1:
                    break
            if page_header_pos == -1:
                raise PageHeaderNotFound(
                    f"Page {page_number}, '{page_header_mark}' context '{text[-100:]}'=============='{page_text[0:100]}' {text_as_hex(page_text[0:100])}"
                )
            # raise ValueError(
            # f"{page_text[:page_header_pos]}==={page_text[page_header_pos:100]}"
            # )
            page_text = page_text[page_header_pos + len(page_header_mark) :]
        text += page_text.strip() + "\n"

    text = text.replace("  ", " ")
    text = text.replace("-\n", "")
    return text
