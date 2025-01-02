from h5py import File
import numpy as np
from .utils import queryDoit


def getLongitude(path):
    with File(path, 'r') as f:
        print(f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['longitude'])
        return f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['longitude'][:]
    

def getLatitude(path):
    with File(path, 'r') as f:
        print(f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['latitude'])
        return f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['latitude'][:]
    

def getRadiance(path):
    with File(path, 'r') as f:
        print(f['BAND7_RADIANCE']['STANDARD_MODE']['OBSERVATIONS']['radiance'])
        return f['BAND7_RADIANCE']['STANDARD_MODE']['OBSERVATIONS']['radiance'][:]


def getRadianceByWaveLength(path, length):
    with File(path, 'r') as f:
        waveCenter = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
        diff = np.abs(waveCenter-length)
        idx = np.argmin(diff)
        rad = f['BAND7_RADIANCE']['STANDARD_MODE']['OBSERVATIONS']['radiance'][:]
        return rad[0, :, :, idx]
    
def wave2channel(f, wave):
    waveCenter = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
    diff = np.abs(waveCenter-wave)
    idx = np.argmin(diff)
    return idx


def getWaveLength(path):
    with File(path, 'r') as f:
        print(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'])
        return np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)


def query(path, **kwargs):
    lon = kwargs.get('lon')
    lat = kwargs.get('lat')
    wave = kwargs.get('wave')
    flag = kwargs.get('flag', False) # 是否要求返回其他值,默认不返回
    if isinstance(path, str):
        with File(path, 'r') as f:
            return queryDoit(f, wave, lon, lat, flag=flag)
    else:
        return queryDoit(path, wave, lon, lat, flag=flag)
    
