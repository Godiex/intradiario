import datetime
import math

import pandas

import requests
from dependency_injector.wiring import inject

from infrastructure.data_source_service.data_source_service import ExternalDataSourceService
from infrastructure.model_config.data_source_config_model import ChirpsConfig
from infrastructure.model_config.model_config_service import ModelConfigService
from shared import geo_utils
from shared.constants_application import FileOpeningModes, FormatDates
from shared.datetime_utils import get_current_date, add_days_to_date, get_date_of_str, get_str_date_formatted
from shared.folder_utils import join_path, create_folder, list_dir


class ChirpsService(ExternalDataSourceService):
    @inject
    def __init__(self, model_config: ModelConfigService):
        self.config_chirps: ChirpsConfig = model_config.get_config_chirps()
        self.amount_file = 16
        self.ideal_size = 1024
        self.top_cell = 6158060
        self.lower_cell = 6906903
        self.path_folder = self.generate_path_folder()

    def get_data(self):
        create_folder(self.path_folder)
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
        path = join_path(self.path_folder, file_name_formatted_date)
        with open(file=path, mode=FileOpeningModes.OPEN_AND_TRUNCATE.value) as f:
            for chunk in response.iter_content(chunk_size=self.ideal_size):
                if chunk:
                    f.write(chunk)
        response.close()

    def process_data(self):
        files_name = [file for file in list_dir(self.path_folder)]
        dates = [self.generate_date_format(file_name) for file_name in list_dir(self.path_folder)]
        tiff_data_frame = pandas.DataFrame(data={'DATE': dates, 'FILE': files_name})
        tiff_data_frame.set_index('DATE', inplace=True)
        results = [self.generate_vector(file_name) for file_name in enumerate(tiff_data_frame['FILE'])]
        aux_forecast = pandas.DataFrame(data=results, index=tiff_data_frame.index, columns=self.coords.POINTID)

    def generate_vector(self, file_name):
        n_cols = 'ncols'
        raster_path = join_path(self.path_folder, file_name)
        raster = geo_utils.read_raster(raster_path)
        row_up = math.floor(self.top_cell / raster[n_cols])
        col_left = (self.lower_cell % raster[n_cols] - 1)
        row_down = math.floor(self.lower_cell / raster[n_cols]) + 1
        col_right = self.lower_cell % raster[n_cols]
        return raster['mtrx'][row_up:row_down, col_left:col_right].ravel()

    def gauge(self):
        pass

    def basin(self):
        pass

    def generate_path_folder(self):
        current_date = get_current_date()
        date_str = get_str_date_formatted(current_date, FormatDates.YEAR_MONTH_DAY_HOUR_MINUTES)
        path_folder = join_path(self.config_chirps.output_path, date_str)
        return path_folder

    @staticmethod
    def generate_date_format(file_name: str) -> datetime:
        data = file_name.split('.')
        year = 1
        month_and_day = 2
        year = data[year]
        month = data[month_and_day][0:2]
        day = data[month_and_day][2:4]
        return get_date_of_str(f"{day}/{month}/{year}", FormatDates.DAY_MONTH_YEAR)
