import shutil
import datetime as dt
from pandas import DataFrame
from dependency_injector.wiring import inject
import urllib.request as request
from contextlib import closing
import zipfile
import pandas as pd
import numpy as np
import math
from osgeo import gdal

from infrastructure.data_source_service.data_source_service import ExternalDataSourceService
from infrastructure.model_config.data_source_config_model import IdeamConfig
from infrastructure.model_config.model_config_service import ModelConfigService
from shared.constants_application import FormatDates, FileOpeningModes
from shared import datetime_utils, folder_utils


class IdeamService(ExternalDataSourceService):
    @inject
    def __init__(self, model_config: ModelConfigService):
        self.__ideam_config: IdeamConfig = model_config.get_config_ideam()
        self.__folder_path = self.__generate_folder_path()

    __current_date = datetime_utils.get_current_day()
    __PREFIX_FILE = "geoTIFFprechorario"
    __EXTENSION_FILE = "00Z.zip"

    def get_data(self):
        folder_utils.create_folder_with_subfolders(self.__folder_path)
        self.__download_data()

    def process_data(self):
        pronostico: DataFrame = self.__read_ideam_forecast(
            self.__list_files_ideam())
        pronostico.to_csv(folder_utils.join_path(
            self.__ideam_config.output_path + "\\", "ideam.csv"))
        folder_utils.delete_folder(self.__folder_path)

    def __generate_folder_path(self):
        date_str = datetime_utils.get_str_date_formatted(
            datetime_utils.get_current_date(), FormatDates.YEAR_MONTH_DAY)
        return folder_utils.join_path(self.__ideam_config.output_path, date_str)

    # region get_data
    def __download_data(self):
        file = self.__PREFIX_FILE + \
            datetime_utils.get_str_date_formatted(
                self.__current_date, FormatDates.DAY_MONTH_YEAR) + self.__EXTENSION_FILE

        file_servidor = self.__ideam_config.server_url + file
        path_file = folder_utils.join_path(
            self.__folder_path, file)
        with closing(request.urlopen(file_servidor)) as source:
            if not folder_utils.exist_folder(path_file):
                with open(path_file, FileOpeningModes.OPEN_AND_TRUNCATE.value) as destiny:
                    shutil.copyfileobj(source, destiny)
    # endregion

    # region process_data
    def __list_files_ideam(self):
        file = self.__PREFIX_FILE + \
            datetime_utils.get_str_date_formatted(
                self.__current_date, FormatDates.DAY_MONTH_YEAR) + self.__EXTENSION_FILE

        path_zip = folder_utils.join_path(
            self.__folder_path, file)
        zipe = zipfile.ZipFile(path_zip)
        files = zipe.namelist()

        list_file_siata = []
        for file in files:
            first_split = file.split('DIA')
            second_split = first_split[-1].split('HLC.')
            datei = second_split[0][0]
            timei = second_split[0][1:]
            timecorrection = dt.timedelta(days=int(datei)-1)
            datei_time = datetime_utils.get_str_date_formatted(
                self.__current_date, FormatDates.YEAR_MONTH_DAY) + "-" + timei
            date_time_obj = datetime_utils.get_date_of_str(
                datei_time, FormatDates.YEAR_MONTH_DAY_HOUR)
            date_time_obj = date_time_obj + timecorrection

            list_file_siata.append(date_time_obj)

        data = {'DATE': list_file_siata, 'FILE': files}
        data_frame = pd.DataFrame(data)
        data_frame = data_frame.set_index('DATE')
        return data_frame

    def __read_raster(self, path):
        ext = path.lower().split('.')[-1]
        if ext == 'asc':
            rst = self.__read_tif_raster(path)
        elif ext == 'tif' or ext == 'tiff':
            rst = self.__read_tif_raster(path)
        else:
            print('File format not recognized')
            rst = self.__build_raster(0.0, 0.0, 0.0, 0.0, np.array(0))
        return rst

    def __read_tif_raster(self, path):
        tif = gdal.Open(path)
        mtrx = tif.GetRasterBand(1).ReadAsArray().astype(float)
        georef = tif.GetGeoTransform()
        if georef[1] < 0:
            xll = georef[0]+georef[1]*mtrx.shape[1]
        else:
            xll = georef[0]
        if georef[5] < 0:
            yll = georef[3]+georef[5]*mtrx.shape[0]
        else:
            yll = georef[3]
        clsz = 0.5*(np.abs(georef[1])+np.abs(georef[5]))
        nodt = tif.GetRasterBand(1).GetNoDataValue()
        tif = None

        rst = self.__build_raster(xll, yll, clsz, nodt, mtrx)
        self.__change_no_data(rst, -9999.0)
        return rst

    def __build_raster(self, xll, yll, clsz, nodt, mtrx):
        nrows = np.size(mtrx, 0)
        ncols = np.size(mtrx, 1)
        nclls = nrows*ncols
        xur = xll+ncols*clsz
        yur = yll+nrows*clsz

        rst = {'ncols': ncols, 'nrows': nrows, 'nclls': nclls, 'xll': xll, 'yll': yll,
               'xur': xur, 'yur': yur, 'clsz': clsz, 'nodt': nodt, 'mtrx': mtrx}
        return rst

    def __change_no_data(self, rst, new_nodt):
        rst['mtrx'][np.where(rst['mtrx'] == rst['nodt'])] = new_nodt
        rst['nodt'] = new_nodt

    def __read_ideam_forecast(self, archivos):
        file = self.__PREFIX_FILE + \
            datetime_utils.get_str_date_formatted(
                self.__current_date, FormatDates.DAY_MONTH_YEAR) + self.__EXTENSION_FILE
        path_zip = folder_utils.join_path(
            self.__folder_path, file)

        path_temp = folder_utils.join_path(
            self.__folder_path, 'temp')

        if not folder_utils.exist_folder(path_temp):
            folder_utils.create_folder(path_temp)
        with zipfile.ZipFile(path_zip, 'r') as zipObj:
            zipObj.extractall(path_temp)

        results = []
        for n, archivo in enumerate(archivos.FILE):
            path_raster = folder_utils.join_path(
                self.__folder_path + '\\' + 'temp', archivo)

            raster = self.__read_raster(path_raster)

            row_up = math.floor(23749/249)
            col_left = (23749 % 249-1)
            row_down = math.floor(38214/249)+1
            col_right = (38214 % 249-1)+1
            vector = raster['mtrx'][row_up:row_down,
                                    col_left:col_right].ravel()
            results.append(vector)

        results = np.asarray(results)
        base = pd.read_excel(folder_utils.join_path(
            self.__ideam_config.output_path, self.__ideam_config.coordinates_path), sheet_name='ideam')
        names = np.asarray(base.COD)

        data_frame = pd.DataFrame(
            data=results, index=archivos.index, columns=names)
        shutil.rmtree(path_temp)
        return data_frame
    # endregion
