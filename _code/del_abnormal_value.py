# 下面这块用于剔除数据中的异常值所在的行，默认异常值为32766，处理单个文件
# 下面这块用于剔除数据中的异常值所在的行，默认异常值为32766，处理单个文件
# 下面这块用于剔除数据中的异常值所在的行，默认异常值为32766，处理单个文件
def del_abnormal_value(file_path, abnormal_col, save_path, abnormal_value=32766, index=True):  # 剔除异常数据（单个文件）
    # file_path，字符串，表示处理文件路径
    # abnormal_col，字符串，表示异常值所在列的列名
    # abnormal_value，数值，表示异常值，默认为32766
    # save_path，字符串，表示处理后文件存储路径及名称
    # index，布尔类型，为True时处理后的文件添加行索引，为False时不添加行索引,默认为True

    import pandas as pd

    print(u'正在处理............')
    csv_read = pd.read_csv(file_path)  # 读取文件
    csv_read = csv_read[(True ^ csv_read[abnormal_col].isin([abnormal_value]))]  # 剔除数据
    csv_read.to_csv(save_path, index=False)  # 重新保存
    print('处理完毕！')


r"""
单个文件处理调用实例：
del_abnormal_value(file_path=r"F:\precipitation\data\PRE_csv_tran\SURF_CLI_CHN_MUL_DAY-PRE-13011-201901.csv",
                   abnormal_col='20-20pre',
                   save_path=r"C:\Users\Casablanca\Desktop\SURF_CLI_CHN_MUL_DAY-PRE-13011-201901.csv")
"""


# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

# 下面这块用于剔除数据中的异常值所在的行，默认异常值为32766，用于批量处理
# 下面这块用于剔除数据中的异常值所在的行，默认异常值为32766，用于批量处理
# 下面这块用于剔除数据中的异常值所在的行，默认异常值为32766，用于批量处理
def del_abnormal_value_all(file_path_walk1, file_path_walk2, abnormal_col, abnormal_value=32766,
                           index=True):  # 剔除异常数据（批量处理）
    # file_path_walk1，字符串，表示csv文件所在文件夹的路径
    # file_path_walk2，字符串，表示处理后csv文件所存储文件夹的路径
    # abnormal_col，字符串，表示异常值所在列的列名
    # abnormal_value，数值，表示异常值，默认为32766
    # index，布尔类型，为True时处理后的文件添加行索引，为False时不添加行索引,默认为True

    import glob
    import os
    file_list = glob.glob(file_path_walk1 + '\\' + '*.csv')  # 读取所有需要处理的csv文件路径及名称并存为列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')

    for file_path1 in file_list:  # 遍历上面读取的csv文件路径及名称列表
        file_name = os.path.basename(file_path1)  # 从csv文件路径中提取文件名
        file_path2 = file_path_walk2 + '\\' + file_name  # 设定转换坐标后csv文件存储位置及名称

        del_abnormal_value(file_path=file_path1,
                           abnormal_col=abnormal_col,
                           save_path=file_path2,
                           abnormal_value=abnormal_value,
                           index=index)
    print('处理完毕！')


r"""
批处理调用实例
import del_abnormal_value as dav

dav.del_abnormal_value_all(file_path_walk1=r'F:\precipitation\data\PRE_csv_tran', 
                           file_path_walk2=r'C:\Users\Casablanca\Desktop\新建文件夹 (2)',
                           abnormal_col='20-20pre', )

"""
