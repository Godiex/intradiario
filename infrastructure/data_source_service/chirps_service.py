import datetime
import pandas

import requests
from dependency_injector.wiring import inject, Provide

from infrastructure.config import ChirpsConfig
from infrastructure.data_source_service import ExternalDataSourceService
from infrastructure.model_config import ModelConfig
from shared.constants_application import FileOpeningModes, FormatDates
from shared.datetime_utils import get_current_date, add_days_to_date, get_date_of_str, get_str_date_formatted
from shared.folder_utils import join_path, create_folder, list_dir


class ChirpsService(ExternalDataSourceService):
    @inject
    def __init__(self, model_config: ModelConfig):
        self.config_chirps: ChirpsConfig = model_config.get_config_chirps()
        self.amount_file = 16
        self.ideal_size = 1024

    def get_data(self):
        create_folder(self.config_chirps.output_path)
        self.download_data()

    def download_data(self):
        current_date = get_current_date()
        for file_number in range(0, self.amount_file):
            file_name_formatted_date = self.generate_file_name_formatted_date(current_date, file_number)
            server_url = self.config_chirps.server_url + file_name_formatted_date
            self.write_file(server_url, file_name_formatted_date)

    def generate_file_name_formatted_date(self, current_date, file_number: int) -> str:
        reference_date = add_days_to_date(current_date, file_number)
        formatted_date = get_str_date_formatted(reference_date, FormatDates.YEAR_POINT_MONTH_DAY)
        file_name: str = self.config_chirps.files_name
        return file_name.format(formatted_date)

    def write_file(self, server_url, file_name_formatted_date):
        response = requests.get(server_url, stream=True)
        path = join_path(self.config_chirps.output_path, file_name_formatted_date)
        with open(file=path, mode=FileOpeningModes.OPEN_AND_TRUNCATE.value) as f:
            for chunk in response.iter_content(chunk_size=self.ideal_size):
                if chunk:
                    f.write(chunk)
        response.close()

    def process_data(self):
        files_name = [file for file in list_dir(self.config_chirps.output_path)]
        dates = [self.generate_date_format(file_name) for file_name in list_dir(self.config_chirps.output_path)]
        tiff_data_frame = pandas.DataFrame(data={'DATE': dates, 'FILE': files_name})
        tiff_data_frame.set_index('DATE', inplace=True)

    @staticmethod
    def generate_date_format(file_name: str) -> datetime:
        data = file_name.split('.')
        year = 1
        month_and_day = 2
        year = data[year]
        month = data[month_and_day][0:2]
        day = data[month_and_day][2:4]
        return get_date_of_str(f"{day}/{month}/{year}", FormatDates.DAY_MONTH_YEAR)

    def gauge(self):
        pass

    def basin(self):
        pass
