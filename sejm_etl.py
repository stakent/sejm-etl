import logging


from data_sources.sejm.api import update_sejm_acts_data
from settings.settings import get_settings


settings = get_settings()


logging.basicConfig(
    level=settings.log_level, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """Main function to process ETL pipeline for Sejm data."""
    update_sejm_acts_data()


if __name__ == "__main__":
    main()
