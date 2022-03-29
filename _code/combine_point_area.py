# 此程序用于将站点降雨数据和遥感产品组合
# 此程序用于将站点降雨数据和遥感产品组合
# 此程序用于将站点降雨数据和遥感产品组合
import os


def combine_point_area():  # 点面结合
    import pandas as pd
    import numpy as np
    import glob

    pd.set_option('display.max_columns', None)
    file_path_walk = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud"
    excel_path = r"F:\precipitation\data2\fusion_precipitation\all_station_precipitation_daily.xlsx"
    file_list = glob.glob(file_path_walk + '\\' + '*.csv')  # 读取所有需要处理的csv文件路径及名称并存为列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    table2 = pd.read_excel(excel_path)
    station_list = list(set(table2["station"]))
    for table1, station_num in zip(file_list, sorted(station_list)):
        table_1 = pd.read_csv(table1)
        table_2 = table2[table2.station == station_num]
        # col1 = table_1.loc[:, ["20_8pre", "8_20pre", "20_20pre"]]
        # col1 = col1 * 0.1
        # table_1.loc[:, ["20_8pre", "8_20pre", "20_20pre"]] = col1
        col2 = table_2.iloc[0, 4:]
        table_1["day2"] = pd.Series(list(range(1, 366)) * 36)
        table_1["daily_fusion_extract"] = col2.T.values
        save_path = r"F:\\precipitation\\data2\\combine_all_data\\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_daily\\" + str(
            station_num) + ".csv"
        np.savetxt(save_path, table_1, fmt='%.7f', delimiter=',',
                   header="station,lat,lon,ele,year,month,day,20_8pre,8_20pre,20_20pre,20_8con,8_20con,20_20con,gpm,trmm,cdr,tem,ndvi,cloud,day2,daily_fusion_extract",
                   comments='')  # 保存为csv文件
    print('处理完毕！')


def combine_point_area2():  # 点面结合,这个用于随机日期的站点
    import pandas as pd
    import numpy as np
    import glob

    pd.set_option('display.max_columns', None)
    file_path_walk = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test"
    excel_path = r"F:\precipitation\data2\fusion_precipitation\all_station_precipitation_daily2.xlsx"
    file_list = glob.glob(file_path_walk + '\\' + '*.csv')  # 读取所有需要处理的csv文件路径及名称并存为列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    table2 = pd.read_excel(excel_path)
    station_list = list(set(table2["station"]))
    for table1, station_num in zip(file_list, sorted(station_list)):
        table_1 = pd.read_csv(table1)
        table_2 = table2[table2.station == station_num]
        # col1 = table_1.loc[:, ["20_8pre", "8_20pre", "20_20pre"]]
        # col1 = col1 * 0.1
        # table_1.loc[:, ["20_8pre", "8_20pre", "20_20pre"]] = col1
        # col2 = table_2.iloc[0, 4:]
        col2 = table_2.iloc[0, [i + 3 for i in table_1["day2"]]]
        table_1["daily_fusion_extract"] = col2.T.values
        save_path = r"F:\\precipitation\\data2\\combine_all_data\\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test_daily\\" + str(
            station_num) + ".csv"
        np.savetxt(save_path, table_1, fmt='%.7f', delimiter=',',
                   header="station,lat,lon,ele,year,month,day,20_8pre,8_20pre,20_20pre,20_8con,8_20con,20_20con,gpm,trmm,cdr,tem,ndvi,cloud,day2,daily_fusion_extract",
                   comments='')  # 保存为csv文件
    print('处理完毕！')


def combine_point_point():  # 点点结合
    import pandas as pd
    import numpy as np

    point_tem_path = r"F:\precipitation\data\TEM\station_modify_add_nulldata"
    point_pre_path = r"C:\Users\Casablanca\Desktop\pre_gpm_trmm_cdr"
    save_path = r"C:\Users\Casablanca\Desktop\ceshi"

    file_name_list = os.listdir(point_tem_path)
    print(u'共发现%s个csv文件' % len(file_name_list))
    print(u'正在处理............')
    for i in file_name_list:
        point_tem_filename_path = os.path.join(point_tem_path, i)
        point_pre_filename_path = os.path.join(point_pre_path, i)
        save_filename_path = os.path.join(save_path, i)

        tem = pd.read_csv(point_tem_filename_path)
        pre = pd.read_csv(point_pre_filename_path)
        col = tem.loc[:, "tem"]
        col = col * 0.1
        pre["tem"] = col
        np.savetxt(save_filename_path, pre, fmt='%.7f', delimiter=',',
                   header="station,lat,lon,ele,year,month,day,20_8pre,8_20pre,20_20pre,20_8con,8_20con,20_20con,gpm,trmm,cdr,tem",
                   comments='')
    print('处理完毕！')


# combine_point_point()

def all_data():  # 组合所有数据
    import numpy as np
    import pandas as pd
    import glob

    file_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_daily\*.csv"
    file_list = glob.glob(file_path)
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    table1 = pd.read_csv(file_list[0])
    for i in file_list[1:]:
        t = pd.read_csv(i, )
        table1 = pd.concat((table1, t), axis=0)
        # table1["day2"]=pd.Series(list(range(1,366))*36)
    print("生成表格为：\n", table1)
    np.savetxt(r"F:\precipitation\data2\all_data\all_data.csv", table1, fmt='%.7f', delimiter=',',
               header="station,lat,lon,ele,year,month,day,20_8pre,8_20pre,std,20_8con,8_20con,20_20con,gpm,trmm,cdr,tem,ndvi,cloud,day2,daily_fusion_extract",
               # header="Std,Lat,Lon,Ele,Year,Month,Day,Mean,Max,Min,MeanQC,MaxQC,MinQC,Albedo,AT,SSM,UW,VW,LST,NDVI,DOY",
               comments='')
    print('处理完毕！')



