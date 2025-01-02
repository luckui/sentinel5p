import numpy as np
from h5py import File
import pandas as pd
from tqdm import tqdm, trange
import geopandas as gpd
from shapely.geometry import Point


class S5():
    def __init__(self, f):
        if isinstance(f, File):
            self.f = f
            self.rad = f['BAND7_RADIANCE']['STANDARD_MODE']['OBSERVATIONS']['radiance'][:][0]
            self.longitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['longitude'][:][0]
            self.latitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['latitude'][:][0]
            self.wavelength = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
            self.solar_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_azimuth_angle'][:][0]
            self.solar_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_zenith_angle'][:][0]
            self.view_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_azimuth_angle'][:][0]
            self.view_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_zenith_angle'][:][0]
            self.wavelength = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
            f.close()
            print('初始化完成')
        else:
            with File(f) as fs:
                self.f = fs
                f = fs
                # self.f = f if not isinstance(f, str) else File(f)
                self.rad = f['BAND7_RADIANCE']['STANDARD_MODE']['OBSERVATIONS']['radiance'][:][0]
                self.longitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['longitude'][:][0]
                self.latitude = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['latitude'][:][0]
                self.wavelength = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
                self.solar_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_azimuth_angle'][:][0]
                self.solar_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['solar_zenith_angle'][:][0]
                self.view_azi = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_azimuth_angle'][:][0]
                self.view_zen = f['BAND7_RADIANCE']['STANDARD_MODE']['GEODATA']['viewing_zenith_angle'][:][0]
                self.wavelength = np.mean(f['BAND7_RADIANCE']['STANDARD_MODE']['INSTRUMENT']['nominal_wavelength'][0, :, :], axis=0)
                print('初始化完成')

    def query(self, lon, lat, wave, flag):
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
        
    def queryByIndex(self, row, col, wave, flag):
        wavId = nearest(self.wavelength, wave)
        row = int(row)
        col = int(col)
        # diss = np.square(self.longitude-lon)+np.square(self.latitude-lat)
        # row, col = np.unravel_index(np.argmin(diss), diss.shape)
        pixv = self.rad[row, col, wavId]
        if flag:
            so_azi = self.solar_azi[row, col]
            so_zen = self.solar_zen[row, col]
            v_azi = self.view_azi[row, col]
            v_zen = self.view_zen[row, col]
            return pixv, so_azi, so_zen, v_azi, v_zen, self.longitude[row, col], self.latitude[row, col]
        else:
            return pixv
        
    
    def regionIndex(self, xmin, ymin, xmax, ymax):
        row1, col1 = self.nnp(lon=xmin, lat=ymin) #row1>row2,col2>col1
        row2, col2 = self.nnp(lon=xmax, lat=ymax)
        rowMin = row1 if row1<row2 else row2
        rowMax = row1 if row1>row2 else row2
        colMin = col1 if col1<col2 else col2
        colMax = col1 if col1>col2 else col2
        return rowMin, rowMax, colMin, colMax
    
    def maskout(self, xmin, ymin, xmax, ymax, wavePath, output):
        records = []
        rowmin, rowmax, colmin, colmax = self.regionIndex(xmin, ymin, xmax, ymax)
        waves = pd.read_csv(wavePath).values.ravel()
        columns = np.concatenate((waves, ['so_azi', 'so_zen', 'v_azi', 'v_zen', 'longitude', 'latitude']), axis=0)
        for row in trange(rowmin, rowmax):
            for col in range(colmin, colmax):
                rec = []
                lon = self.longitude[row, col]
                lat = self.latitude[row, col]
                for idx, wav in enumerate(waves):
                    if idx==len(waves)-1:
                        pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude = self.query(lon, lat, wave=wav, flag=True)
                        rec = rec+[pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude]
                    else:
                        pixv = self.query(lon,lat,wav,flag=False)
                        rec.append(pixv)
                records.append(rec)
        df = pd.DataFrame(records, columns=columns)
        df.to_csv(output, index=False)


    def nnp(self, lon, lat):
        diss = np.square(self.longitude-lon)+np.square(self.latitude-lat)
        row, col = np.unravel_index(np.argmin(diss), diss.shape)
        return row, col
    
    def getLonLat(self, output):
        lon = self.longitude.reshape(-1,1)
        lat = self.latitude.reshape(-1,1)
        lonlat = np.concatenate((lon, lat), axis=1)
        ps = [Point(lon, lat) for lon, lat in lonlat]
        gdf = gpd.GeoDataFrame(geometry=ps, crs='EPSG:4326')
        gdf.to_file(output)

    def maskIndex(self, output):
        lon = self.longitude.reshape(-1,1)
        lat = self.latitude.reshape(-1,1)
        lonlat = np.concatenate((lon, lat), axis=1)
        df = pd.DataFrame(lonlat, columns=['lon', 'lat'])
        xmin = 116.355183
        xmax = 122.834203
        ymin = 27.143423
        ymax = 35.127197
        print('开始切片')
        selected = df[(df['lon']>xmin)&(df['lon']<xmax)&(df['lat']>ymin)&(df['lat']<ymax)]
        print('切片完成')
        idx = selected.index.tolist()
        rowcols = []
        shape = self.longitude.shape
        for i in idx:
            row, col = np.unravel_index(i, shape)
            rowcols.append([row, col, lonlat[i, 0], lonlat[i, 1]])
        sdf = pd.DataFrame(rowcols, columns=['row', 'col', 'lon', 'lat'])
        sdf.to_csv(output, index=False)
        # ps = [Point(lon, lat) for lon, lat in lonlat]
        # gdf = gpd.GeoDataFrame(geometry=ps, crs='EPSG:4326')

        # gdf.to_file(output)

    def queryby(self, idxPath, wavePath, output):
        idx = pd.read_csv(idxPath).values
        waves = pd.read_csv(wavePath).values.ravel()
        records = []
        columns = np.concatenate((waves, ['so_azi', 'so_zen', 'v_azi', 'v_zen', 'longitude', 'latitude']), axis=0)
        for item in tqdm(idx):
            rec = []
            row, col = item[0], item[1]
            for count, wav in enumerate(waves):
                if count==len(waves)-1:
                    pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude = self.queryByIndex(row, col, wav, flag=True)
                    rec = rec+[pixv, so_azi, so_zen, v_azi, v_zen, longitude, latitude]
                else:
                    pixv = self.queryByIndex(row, col, wav, flag=False)
                    rec.append(pixv)
            records.append(rec)
        df = pd.DataFrame(records, columns=columns)
        df.to_csv(output, index=False)


def nearest(arr, num):
    diff = np.abs(arr-num)
    idx = np.argmin(diff)
    return idx