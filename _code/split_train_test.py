# 将36个站点数据随机划分为训练集和测试集
import glob
import os
import pandas as pd
import random
import numpy as np
from _code.del_abnormal_value import del_abnormal_value


def split_train_test1():  # 此处按照每个站点提取相同的日期进行分割
    print(u'正在处理............')
    # 设置随机天数
    seq = list(range(1, 366))
    train_day2 = random.sample(seq, 305)  # 训练集天数
    test_day2 = []  # 测试集天数
    for i in seq:
        if i not in train_day2:
            test_day2.append(i)

    file_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud\*.csv"
    path_list = glob.glob(file_path)  # 所有文件路径列表
    for i in path_list:
        file = pd.read_csv(i)  # 读取文件
        file["day2"] = pd.Series(list(range(1, 366)) * 36)  # 给每个csv文件加上天数day2（1~365）
        csv_name = os.path.basename(i)  # 提取文件名用于输出

        file_train = file[file["day2"].isin(train_day2)]  # 根据上面的训练集天数选择训练集
        file_train.to_csv(
            rf"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_train\{csv_name}",
            index=False)  # 保存训练集
        file_test = file[file["day2"].isin(test_day2)]  # 根据上面的测试集天数选择测试集
        file_test.to_csv(
            rf"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test\{csv_name}",
            index=False)  # 保存测试集

    print('处理完毕！')


# 将36个站点数据随机划分为训练集和测试集


def split_train_test2():  # 此处按照每个站点不同的日期进行分割
    print(u'正在处理............')
    # 设置随机天数


    file_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud\*.csv"
    path_list = glob.glob(file_path)  # 所有文件路径列表
    for i in path_list:
        # 设置随机天数
        seq = list(range(1, 366))
        train_day2 = random.sample(seq, 250)  # 训练集天数
        test_day2 = []  # 测试集天数
        for p in seq:
            if p not in train_day2:
                test_day2.append(p)

        file = pd.read_csv(i)  # 读取文件
        file["day2"] = pd.Series(list(range(1, 366)) * 36)  # 给每个csv文件加上天数day2（1~365）
        csv_name = os.path.basename(i)  # 提取文件名用于输出

        file_train = file[file["day2"].isin(train_day2)]  # 根据上面的训练集天数选择训练集
        file_train.to_csv(
            rf"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_train\{csv_name}",
            index=False)  # 保存训练集
        file_test = file[file["day2"].isin(test_day2)]  # 根据上面的测试集天数选择测试集
        file_test.to_csv(
            rf"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test\{csv_name}",
            index=False)  # 保存测试集

    print('处理完毕！')


def all_data_train():  # 组合所有数据

    file_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_train\*.csv"
    file_list = glob.glob(file_path)
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    table1 = pd.read_csv(file_list[0])
    for i in file_list[1:]:
        t = pd.read_csv(i, )
        table1 = pd.concat((table1, t), axis=0)
        # table1["day2"]=pd.Series(list(range(1,366))*36)
    print("生成表格为：\n", table1)
    np.savetxt(r"F:\precipitation\data2\train_model\all_data_train.csv", table1, fmt='%.7f', delimiter=',',
               header="station,lat,lon,ele,year,month,day,20_8pre,8_20pre,std,20_8con,8_20con,20_20con,gpm,trmm,cdr,tem,ndvi,cloud,day2",
               # header="Std,Lat,Lon,Ele,Year,Month,Day,Mean,Max,Min,MeanQC,MaxQC,MinQC,Albedo,AT,SSM,UW,VW,LST,NDVI,DOY",
               comments='')
    print('处理完毕！')


def all_data_test():  # 组合所有数据

    file_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test\*.csv"
    file_list = glob.glob(file_path)
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    table1 = pd.read_csv(file_list[0])
    for i in file_list[1:]:
        t = pd.read_csv(i, )
        table1 = pd.concat((table1, t), axis=0)
        # table1["day2"]=pd.Series(list(range(1,366))*36)
    print("生成表格为：\n", table1)
    np.savetxt(r"F:\precipitation\data2\test_model\all_data_test.csv", table1, fmt='%.7f', delimiter=',',
               header="station,lat,lon,ele,year,month,day,20_8pre,8_20pre,std,20_8con,8_20con,20_20con,gpm,trmm,cdr,tem,ndvi,cloud,day2",
               # header="Std,Lat,Lon,Ele,Year,Month,Day,Mean,Max,Min,MeanQC,MaxQC,MinQC,Albedo,AT,SSM,UW,VW,LST,NDVI,DOY",
               comments='')
    print('处理完毕！')


def start():
    split_train_test2()
    all_data_train()
    all_data_test()
    del_abnormal_value(file_path=r"F:\precipitation\data2\train_model\all_data_train.csv",
                       abnormal_col='std',
                       save_path=r"F:\precipitation\data2\train_model\all_data_train_del_abnormal.csv",
                       abnormal_value=3276.6)
    del_abnormal_value(file_path=r"F:\precipitation\data2\test_model\all_data_test.csv",
                       abnormal_col='std',
                       save_path=r"F:\precipitation\data2\test_model\all_data_test_del_abnormal.csv",
                       abnormal_value=3276.6)


# if __name__ == "__main__":
#     start()
#     split_train_test1()
