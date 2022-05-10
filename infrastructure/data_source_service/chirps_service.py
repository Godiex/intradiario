import datetime
import math
import pandas
import requests
from dependency_injector.wiring import inject

from infrastructure.data_source_service.data_source_service import ExternalDataSourceService
from infrastructure.model_config.data_source_config_model import ChirpsConfig
from infrastructure.model_config.model_config_service import ModelConfigService
from shared.constants_application import FileOpeningModes, FormatDates, Granularity
from shared import datetime_utils
from shared import folder_utils
from shared import geo_utils


class ChirpsService(ExternalDataSourceService):
    __forecasts = None
    __amount_file = 16
    __ideal_size = 1024
    __top_cell = 6158060
    __lower_cell = 6906903
    granularity = Granularity.ONE_HOUR.value

    @inject
    def __init__(self, model_config: ModelConfigService):
        self.__config_chirps: ChirpsConfig = model_config.get_config_chirps()
        self.__folder_path = self.__generate_folder_path()

    # region GetData
    def get_data(self):
        folder_utils.create_folder(self.__folder_path)
        self.__download_data()

    def __download_data(self):
        current_date = datetime_utils.get_current_day()
        date_str = datetime_utils.get_str_date_formatted(current_date, FormatDates.YEAR_MONTH_DAY_SLASH)
        for file_number in range(0, self.__amount_file):
            file_name_formatted_date = self.__generate_file_name_formatted_date(current_date, file_number)
            server_url = self.__config_chirps.server_url + date_str + file_name_formatted_date
            self.__write_files(server_url, file_name_formatted_date)

    def __generate_file_name_formatted_date(self, current_date, file_number: int) -> str:
        reference_date = datetime_utils.add_days_to_date(current_date, file_number)
        formatted_date = datetime_utils.get_str_date_formatted(reference_date, FormatDates.YEAR_POINT_MONTH_DAY)
        file_name: str = self.__config_chirps.files_name
        return file_name.format(formatted_date)

    def __write_files(self, server_url, file_name_formatted_date):
        response = requests.get(server_url, stream=True)
        path = folder_utils.join_path(self.__folder_path, file_name_formatted_date)
        with open(file=path, mode=FileOpeningModes.OPEN_AND_TRUNCATE.value) as f:
            for chunk in response.iter_content(chunk_size=self.__ideal_size):
                if chunk:
                    f.write(chunk)
        response.close()

    def __generate_folder_path(self):
        current_date = datetime_utils.get_current_date()
        date_str = datetime_utils.get_str_date_formatted(current_date, FormatDates.YEAR_MONTH_DAY_HOUR_MINUTES)
        return folder_utils.join_path(self.__config_chirps.output_path, date_str)
    # endregion

    # region ProcessData
    def process_data(self):
        files_name = [file for file in folder_utils.list_dir(self.__folder_path)]
        dates = [self.__generate_date_format(file_name) for file_name in folder_utils.list_dir(self.__folder_path)]
        tiff_data_frame = pandas.DataFrame(data={'DATE': dates, 'FILE': files_name})
        tiff_data_frame.set_index('DATE', inplace=True)
        results = [self.__generate_vector(file_name) for n, file_name in enumerate(tiff_data_frame['FILE'])]
        self.__interpolate_data(results, tiff_data_frame)
        folder_utils.delete_folder(self.__folder_path)

    def __interpolate_data(self, results, tiff_data_frame):
        coordinates = pandas.read_csv(self.__config_chirps.coordinates_path)
        aux_forecast = pandas.DataFrame(data=results, index=tiff_data_frame.index, columns=coordinates.POINTID)
        if self.granularity in [Granularity.ONE_HOUR.value, Granularity.DIARY.value]:
            aux_forecast = aux_forecast.cumsum(axis=0)
            aux_forecast = aux_forecast.resample(self.granularity).asfreq()
            aux_forecast = aux_forecast.interpolate(method='linear', limit_direction='forward', axis='index')
            self.__forecasts = aux_forecast
        else:
            self.__forecasts = aux_forecast

    def __generate_vector(self, file_name):
        n_cols = 'ncols'
        raster_path = folder_utils.join_path(self.__folder_path, file_name)
        raster = geo_utils.read_raster(raster_path)
        row_up = math.floor(self.__top_cell / raster[n_cols])
        col_left = (self.__lower_cell % raster[n_cols] - 1)
        row_down = math.floor(self.__lower_cell / raster[n_cols]) + 1
        col_right = self.__lower_cell % raster[n_cols]
        return raster['mtrx'][row_up:row_down, col_left:col_right].ravel()

    @staticmethod
    def __generate_date_format(file_name: str) -> datetime:
        data = file_name.split('.')
        year = 1
        month_and_day = 2
        year = data[year]
        month = data[month_and_day][0:2]
        day = data[month_and_day][2:4]
        return datetime_utils.get_date_of_str(f"{day}/{month}/{year}", FormatDates.DAY_MONTH_YEAR)
    # endregion

    def gauge(self):
        pass

    def basin(self):
        pass
