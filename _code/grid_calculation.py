# 用于进行栅格计算
# 用于进行栅格计算
# 用于进行栅格计算

import gdal
import glob
import os
import numpy as np

cloud_file_path = r"F:\precipitation\data\cloud\cloud_tif\*.tif"
file_list = glob.glob(cloud_file_path)
file_list_sort = []


def date_list():
    date_list1 = []
    import datetime
    start = datetime.datetime(2019, 1, 1)
    end = datetime.datetime(2020, 1, 1)

    for day in range((end - start).days):
        date = (start + datetime.timedelta(days=day)).date()
        # print(date)
        date_list1.append(date)
    return date_list1


def read_tiff(file_path):
    # 打开GeoTIFF波段1，索引为1
    # 波段索引从1开始，而不是0
    tiff = gdal.Open(file_path)
    tiff_width = tiff.RasterXSize  # 栅格矩阵的列数
    tiff_height = tiff.RasterYSize  # 栅格矩阵的行数
    # tiff_bands = tiff.RasterCount  # 波段数
    tiff_data = tiff.ReadAsArray(0, 0, tiff_width, tiff_height)  # 获取数据

    # tiff_geotrans = tiff.GetGeoTransform()  # 获取仿射矩阵信息
    # tiff_proj = tiff.GetProjection()  # 获取投影信息
    return tiff, tiff_data


def create_tif(tif_path, tif_name, row, col, geotransform, projection, matrix_name):
    # 生成tif
    out_file_tif_path = os.path.join(tif_path, "cloud_tif" + tif_name + ".tif")
    driver = gdal.GetDriverByName("GTiff")
    out_tif = driver.Create(out_file_tif_path, row, col, 1, gdal.GDT_Float64)
    out_tif.SetGeoTransform(geotransform)  # 仿射矩阵信息
    out_tif.SetProjection(projection)  # 地图投影信息
    # out_tif.GetRasterBand(1).WriteArray(np.where(tiff_array < 0, np.nan, tiff_array))
    out_tif.GetRasterBand(1).WriteArray(matrix_name)  # 写入文件
    del out_tif


for i in range(0, len(file_list)):
    aa = os.path.basename(file_list[i])  # 路径中提取文件名
    bb = os.path.join(r"F:\precipitation\data\cloud\cloud_tif", aa[0:9] + str(i + 1) + ".tif")  # 重新命名路径，原来的有问题

    file_list_sort.append(bb)  # 重命名后的路径加入列表
    # file_list_sort.append()

ss = []
for k in range(0, len(file_list_sort), 24):  # 将路径分割为24个一组
    # print(i)
    ss.append(file_list_sort[k:k + 24])
# ss为24个一组的文件路径列表


for i, name in zip(list(range(len(ss))), date_list()):
    tiff24, tiff24_data1 = read_tiff(ss[i][0])  # 读取第一个数据，后续从中提取创建tif所需信息
    """
        # 下面这段用于将24个矩阵相加
        tiff24111, tiff24_data2 = read_tiff(ss[i][0])  # 读取第一个数据，后续从中提取创建tif所需信息,测试
        tiff24_,tiff24_data = read_tiff(ss[i][0])

        for j in ss[i][1:24]:
            tiff,tiff_data=read_tiff(j)

            tiff24_data2+=tiff_data
            # tiff24.append(tiff_data)
        tiff24_merge__fuben = np.array(tiff24_data2) / 24  # 求均值
    """
    tiff_matrix = []
    for j in ss[i]:
        tiffone, tiffData2 = read_tiff(j)
        tiff_matrix.append(tiffData2)
    tiff24_data = sum(tiff_matrix)  # 将24个矩阵相加
    tiff24_merge = np.array(tiff24_data) / 24  # 求均值

    create_tif(tif_path=r"F:\precipitation\data\cloud\cloud_tif24", tif_name=str(name), row=tiff24.RasterXSize,
               col=tiff24.RasterYSize, geotransform=tiff24.GetGeoTransform(), projection=tiff24.GetProjection(),
               matrix_name=tiff24_merge)
