import logging
from dependency_injector.wiring import inject

from infrastructure.model_config.model_config_service import ModelConfigService
from shared import datetime_utils, folder_utils
from shared.constants_application import FormatDates


class Log():

    @inject
    def __init__(self, model_config: ModelConfigService):
        self.__log_path = model_config.get_project_config().logPath
        self.__configure_log()

    def __configure_log(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        current_date = datetime_utils.get_current_date()
        date_now = datetime_utils.get_str_date_formatted(
            current_date, FormatDates.YEAR_MONTH_DAY)

        path_folder = f'{self.__log_path}{date_now}'
        folder_utils.create_folder_with_subfolders(path_folder)
        path_machine = f'{path_folder}\\reporte_{date_now}.log'
        file_handler = logging.FileHandler(path_machine)
        formatter = logging.Formatter(
            '%(asctime)s _ %(levelname)s : %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)
