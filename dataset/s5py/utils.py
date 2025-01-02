import numpy as np
from h5py import File


class QueryS5():
    def __init__(self, f):
        self.f = f if not isinstance(f, str) else File(f)
        self.rad = f['BAND7_RADIANCE']['STANDARD_MODE']['OBSERVATIONS']['radiance'][:][0]
        self.longitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['longitude'][:][0]
        self.latitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['latitude'][:][0]
        self.wavelength = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
        self.solar_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_azimuth_angle'][:][0]
        self.solar_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_zenith_angle'][:][0]
        self.view_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_azimuth_angle'][:][0]
        self.view_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_zenith_angle'][:][0]
        self.wavelength = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)

    def query(self, lon, lat, wave, flag=False):
        wavId = nearest(self.wavelength, wave)
        diss = np.square(self.longitude-lon)+np.square(self.latitude-lat)
        row, col = np.unravel_index(np.argmin(diss), diss.shape)
        pixv = self.rad[row, col, wavId]
        if flag:
            so_azi = self.solar_azi[row, col]
            so_zen = self.solar_zen[row, col]
            v_azi = self.view_azi[row, col]
            v_zen = self.view_zen[row, col]
            return pixv, so_azi, so_zen, v_azi, v_zen, self.longitude[row, col], self.latitude[row, col]
        else:
            return pixv
    
    def queryAllBands(self, lon, lat, flag=False):
        # wavId = nearest(self.wavelength, wave)
        diss = np.square(self.longitude-lon)+np.square(self.latitude-lat)
        row, col = np.unravel_index(np.argmin(diss), diss.shape)
        pixv = self.rad[row, col, :]
        if flag:
            so_azi = self.solar_azi[row, col]
            so_zen = self.solar_zen[row, col]
            v_azi = self.view_azi[row, col]
            v_zen = self.view_zen[row, col]
            return *pixv, so_azi, so_zen, v_azi, v_zen, self.longitude[row, col], self.latitude[row, col]
        else:
            return pixv


def queryDoit(f, wave, lon, lat, flag=False):
    rad = f['BAND7_RADIANCE']['STANDARD_MODE']['OBSERVATIONS']['radiance'][:][0]
    longitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['longitude'][:][0]
    latitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['latitude'][:][0]
    wavelength = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
    # print(wavelength)
    # print(latitude)
    # print(longitude)
    wavId = nearest(wavelength, wave)

    diss = np.square(longitude-lon)+np.square(latitude-lat)
    row, col = np.unravel_index(np.argmin(diss), diss.shape)
    # minDis = diss[row, col]

    pixv = rad[row, col, wavId]
    # print(row, col)
    # print(rad[:,:,0])
    # print(pixv)
    if flag:
        solar_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_azimuth_angle'][:][0]
        solar_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_zenith_angle'][:][0]
        view_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_azimuth_angle'][:][0]
        view_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_zenith_angle'][:][0]
        so_azi = solar_azi[row, col]
        so_zen = solar_zen[row, col]
        v_azi = view_azi[row, col]
        v_zen = view_zen[row, col]
        return pixv, so_azi, so_zen, v_azi, v_zen, longitude[row, col], latitude[row, col]
    else:
        return pixv


def nearest(arr, num):
    diff = np.abs(arr-num)
    idx = np.argmin(diff)
    return idx