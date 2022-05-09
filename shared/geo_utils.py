# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 10:27:36 2022

@author: Rodian
"""

# =============================================================================
# Librerias
# =============================================================================

import numpy as np
from osgeo import gdal


# =============================================================================
# Funciones
# =============================================================================

def read_raster(path):
    u"""
    It loads a raster after identifiying the file extension

    Parameters
    ----------
    path : text
        Raster file direction in the hard disk

    Returns
    -------
    rst : dictionary
        Raster dictionary with the next attribute naming convention:
            - ncols : Number of columns
            - nrows : Number of rows
            - xll   : X-axis coordinate of the lower left corner
            - yll   : Y-axis coordinate of the lower left corner
            - xur   : X-axis coordinate of the upper right corner
            - yur   : Y-axis coordinate of the upper right corner
            - clsz  : Cell size
            - nodt  : Missing data value
            - mtrx  : Data matrix
    """
    # It identifies the file extension and reads the raster
    ext = path.lower().split('.')[-1]
    if ext == 'asc':
        rst = read_tif_raster(path)
    elif ext in ['tif', 'tiff']:
        rst = read_tif_raster(path)
    else:
        print('File format not recognized')
        rst = build_raster(0.0, 0.0, 0.0, 0.0, np.array(0))
    return rst


def read_tif_raster(path, missing=-9999.0):
    u"""
    It loads a GeoTiff raster file from the hard disk

    Parameters
    ----------
    path : text
        Raster file direction in the hard disk
    missing _ float
        Value to be used as a missing / no data value
    vrbl : text
        Variable to be loaded

    Returns
    -------
    rst : dictionary
        Raster dictionary with the next attribute naming convention:
            - ncols : Number of columns
            - nrows : Number of rows
            - xll   : X-axis coordinate of the lower left corner
            - yll   : Y-axis coordinate of the lower left corner
            - xur   : X-axis coordinate of the upper right corner
            - yur   : Y-axis coordinate of the upper right corner
            - clsz  : Cell size
            - nodt  : Missing data value
            - mtrx  : Data matrix
    """
    # It reads the georeferenciation properties and the data matrix
    tif = gdal.Open(path)
    mtrx = tif.GetRasterBand(1).ReadAsArray().astype(float)
    georef = tif.GetGeoTransform()
    if georef[1] < 0:
        xll = georef[0] + georef[1] * mtrx.shape[1]  # np.size(mtrx,1)
    else:
        xll = georef[0]
    if georef[5] < 0:
        yll = georef[3] + georef[5] * mtrx.shape[0]  # np.size(mtrx,0)
    else:
        yll = georef[3]
    clsz = 0.5 * (np.abs(georef[1]) + np.abs(georef[5]))
    nodt = tif.GetRasterBand(1).GetNoDataValue()
    tif = None

    # It builds the Raster dictionary and returns
    rst = build_raster(xll, yll, clsz, nodt, mtrx)
    rst['mtrx'][np.where(rst['mtrx'] == rst['nodt'])] = missing
    rst['nodt'] = missing
    return rst


def build_raster(xll, yll, clsz, nodt, mtrx):
    u"""
    It builds a Raster dictionary when all of its attributes are specified

    Parameters
    ----------
    xll : float
        X-axis coordinate of the lower left corner
    yll : float
        Y-axis coordinate of the lower left corner
    clsz : float
        Cell size
    nodt : number
        Missing data value
    mtrx : float
        Data array

    Returns
    -------
    rst : dictionary
        A dictionary with the raster information
    """
    # It calculates aditional necessary information
    nrows = np.size(mtrx, 0)
    ncols = np.size(mtrx, 1)
    nclls = nrows * ncols
    xur = xll + ncols * clsz
    yur = yll + nrows * clsz

    # It assambles the Raster dictinary and returns
    rst = {'ncols': ncols, 'nrows': nrows, 'nclls': nclls, 'xll': xll, 'yll': yll, \
           'xur': xur, 'yur': yur, 'clsz': clsz, 'nodt': nodt, 'mtrx': mtrx}
    return rst


def write_ascii_raster(path, rst):
    u"""
    It saves a Raster dictionary in the hard disk using the Arc/ASCII format

    Parameters
    ----------
    path: text
        Direction in the hard disk in which the Arc/ASCII file will be written
    rst: dictionary
        AsciiRaster dictionary to export
    """
    # It builds the header information string
    hdr = 'ncols        ' + str(rst['ncols']) \
          + '\nnrows        ' + str(rst['nrows']) \
          + '\nxllcorner    ' + str(rst['xll']) \
          + '\nyllcorner    ' + str(rst['yll']) \
          + '\ncellsize     ' + str(rst['clsz']) \
          + '\nnodata_value ' + str(rst['nodt'])

    # It saves data in the hard disk and finishes
    with open(path, 'w') as file:
        file.write(hdr)
        for row in rst['mtrx']:
            line = '\n' + ' '.join(row.astype('str'))
            file.write(line)


def write_tif_raster(path, rst, prcsn=gdal.GDT_Float32):
    u"""
    It saves a Raster dictionary in the hard disk using the GeoTiff format

    Parameters
    ----------
    path: text
        Direction in the hard disk in which the GeoTiff file will be written
    rst: dictionary
        AsciiRaster dictionary to export
    prcsn: optional, integer
        Data precision. By default gdal.GDT_Float32, but any other data type
        can be specified
    """
    # It creates the driver and the file
    driver = gdal.GetDriverByName("GTiff")
    tif = driver.Create(path, rst['ncols'], rst['nrows'], 1, prcsn)

    # It sets the metadata, band data and finishes
    tif.SetGeoTransform((rst['xll'], rst['clsz'], 0.0, rst['yur'], 0.0,
                         -rst['clsz']))
    band = tif.GetRasterBand(1)
    band.SetNoDataValue(rst['nodt'])
    band.WriteArray(rst['mtrx'], 0, 0)
    band.FlushCache()
    tif = None
    band = None


def write_raster(path, rst, prcsn=gdal.GDT_Float32):
    u"""
    It writes a raster after identifiying the file extension

    Parameters
    ----------
    path : text
        Raster file direction in the hard disk

    rst : dictionary
        Raster dictionary with the next attribute naming convention:
            - ncols : Number of columns
            - nrows : Number of rows
            - xll   : X-axis coordinate of the lower left corner
            - yll   : Y-axis coordinate of the lower left corner
            - xur   : X-axis coordinate of the upper right corner
            - yur   : Y-axis coordinate of the upper right corner
            - clsz  : Cell size
            - nodt  : Missing data value
            - mtrx  : Data matrix
    """
    # It identifies the file extension and writes the raster
    ext = path.lower().split('.')[-1]
    if ext == 'asc':
        rst = write_ascii_raster(path, rst)
    elif ext in ['tif', 'tiff']:
        rst = write_tif_raster(path, rst, prcsn)
    else:
        print('File format not recognized')


def nulls_in_bounds(rst):
    u"""
    It sets no data values in the bounds of raster

    Parameters
    ----------
    rst : dictionary
        Raster dictionary
    """
    # It sets no data values in the bounds
    rst['mtrx'][0, :] = rst['nodt']
    rst['mtrx'][rst['nrows'] - 1, :] = rst['nodt']
    rst['mtrx'][:, 0] = rst['nodt']
    rst['mtrx'][:, rst['ncols'] - 1] = rst['nodt']
