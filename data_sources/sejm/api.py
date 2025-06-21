from enum import StrEnum
from datetime import datetime
import logging
import os
import requests
from settings.settings import get_settings

from transform.act_pdf_to_text import PageHeaderNotFound, act_pdf_to_text
from data_sources.sejm.serializers import ActsInfo, ActInfo

settings = get_settings()


def get_acts_list(publisher: str, year: int) -> list[ActInfo]:
    """Get acts list for given publisher and year."""
    base_url = "https://api.sejm.gov.pl/eli"
    acts_list_url = f"{base_url}/acts/{publisher}/{year}"
    response = requests.get(
        url=acts_list_url, timeout=settings.requests_external_timeout
    )
    response.raise_for_status()
    data = ActsInfo.model_validate_json(response.content)
    return data.items


def get_act_as_pdf(publisher: str, year: int, position: int) -> bytes:
    """Function to get act text as pdf from ISAP API"""
    base_url = "https://api.sejm.gov.pl/eli"
    act_pdf_url = f"{base_url}/acts/{publisher}/{year}/{position}/text.pdf"
    response = requests.get(act_pdf_url, timeout=settings.requests_external_timeout)
    response.raise_for_status()
    return response.content


class ActFormatType(StrEnum):
    """Enum class for act format types."""

    PDF = "pdf"
    TXT = "txt"


def get_act_cache_path(act_info: ActInfo, base_dir: str, format: ActFormatType) -> str:
    return f"{base_dir}/{format}/{act_info.year}/{act_info.address}.{format}"


def is_act_cached(act_info: ActInfo, format: ActFormatType) -> bool:
    act_cache_path = get_act_cache_path(
        act_info=act_info,
        base_dir=settings.cache_base_dir,
        format=format,
    )
    if not os.path.exists(act_cache_path):
        return False

    file_size = os.path.getsize(act_cache_path)
    return file_size > 0


def get_and_cache_act_pdf(act_info: ActInfo) -> None:
    pdf_data = get_act_as_pdf(act_info.publisher, act_info.year, position=act_info.pos)

    pdf_file_path = get_act_cache_path(
        act_info=act_info,
        base_dir=settings.cache_base_dir,
        format=ActFormatType.PDF,
    )
    os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
    logging.info(f"Saving {pdf_file_path}")
    with open(pdf_file_path, "wb") as pdf_file:
        pdf_file.write(pdf_data)


def tranform_pdf_to_txt(act_info: ActInfo) -> None:
    pdf_file_path = get_act_cache_path(
        act_info=act_info,
        base_dir=settings.cache_base_dir,
        format=ActFormatType.PDF,
    )
    logging.info(f"Transforming PDF to TXT {pdf_file_path}")
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            text = act_pdf_to_text(pdf_file=pdf_file, act_position=act_info.pos)
    except PageHeaderNotFound as exc:
        logging.error(
            f"Extracting text from pdf {pdf_file_path} - Page header not found error: {exc}"
        )
        return

    text_file_path = get_act_cache_path(
        act_info=act_info,
        base_dir=settings.cache_base_dir,
        format=ActFormatType.TXT,
    )
    os.makedirs(os.path.dirname(text_file_path), exist_ok=True)
    with open(text_file_path, "w") as pdf_file:
        pdf_file.write(text)


def update_sejm_acts_data():
    """Run the ETL pipeline for acts."""
    logging.info("Started running the ETL pipeline for acts")
    settings.number_of_years_to_process = 3
    publishers = ["DU", "MP"]

    current_year = datetime.now().year
    for year in range(
        current_year, current_year - settings.number_of_years_to_process, -1
    ):
        for publisher in publishers:
            logging.info(f"Processing year: {year} for publishers: {publisher}")
            acts_list = get_acts_list(publisher, year)
            logging.info(
                f"Processing publisher: {publisher}, year: {year}, number of acts: {len(acts_list)}"
            )
            n = 0
            for act_info in acts_list:
                n += 1
                if n % 100 == 0:
                    logging.info(f"Processed {n} acts out of {len(acts_list)}")

                if not is_act_cached(act_info=act_info, format=ActFormatType.PDF):
                    get_and_cache_act_pdf(act_info=act_info)

                if not is_act_cached(act_info=act_info, format=ActFormatType.TXT):
                    tranform_pdf_to_txt(act_info=act_info)

    logging.info("Finished ETL pipeline for acts")
