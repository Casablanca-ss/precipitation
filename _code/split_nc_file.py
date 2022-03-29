import numpy as np
import netCDF4 as nc
from osgeo import gdal, osr


data = r'F:\precipitation\data\cloud\cloud.nc'

f = nc.Dataset(data)
var_lon = f['longitude'][:]
var_lat = f['latitude'][:]
# data_arr = data_arr[::-1]  # 因为我的数据维度是正序排列，需要逆序一下
# 影像的左上角和右下角坐标
LonMin, LatMax, LonMax, LatMin = [var_lon.min(), var_lat.max(), var_lon.max(), var_lat.min()]
# 分辨率计算
N_Lat = len(var_lat)
N_Lon = len(var_lon)
Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)
Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)

# 创建.tif文件
driver = gdal.GetDriverByName('GTiff')

for i in range(len(f["tcc"])):
    data=f['tcc'][i]
    data_arr = np.asarray(data)
    out_tif_name = r'F:\precipitation\data\cloud\cloud_tif\cloud_tif{}.tif'.format(i+1)

    print(out_tif_name)
    out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)  # 创建框架

    # 设置影像的显示范围
    # Lat_Res一定要是-的
    geotransform = (LonMin-0.125, Lon_Res, 0, LatMax+0.125, 0, -Lat_Res)
    out_tif.SetGeoTransform(geotransform)



    # aaa='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'

    # 获取地理坐标系统信息，用于选取需要的地理坐标系统
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
    out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息
    # out_tif.SetProjection(aaa) #我定义的坐标
    # 数据写出
    out_tif.GetRasterBand(1).WriteArray(data_arr)  # 将数据写入内存，此时没有写入硬盘
    out_tif.FlushCache()  # 将数据写入硬盘

    out_tif = None  # 注意必须关闭tif文件
    # bbb=GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]
