# 此程序用于将csv文件中度为单位的坐标转换为小数形式，直接调用14行（单个文件）或35行（批量处理）
# 此程序用于将csv文件中度为单位的坐标转换为小数形式，直接调用14行（单个文件）或35行（批量处理）
# 此程序用于将csv文件中度为单位的坐标转换为小数形式，直接调用14行（单个文件）或35行（批量处理）


# 下面这块函数用于处理单个文件
# 下面这块函数用于处理单个文件
# 下面这块函数用于处理单个文件
def degree_to_digit(file_path1, file_path2, col_name, point='5'):  # 对单个csv文件进行坐标转换
    # file_path1，字符串，表示初始csv文件路径及名称
    # file_path2，字符串，表示处理后数据存放路径及名称
    # col_name，列表，表示纬度度所在列名，设置为一个元素为字符串的列表，每个字符表示列名
    # point,字符串，表示要保留的小数位数，建议十位以内，默认为五位

    import pandas as pd
    import numpy as np
    import glob
    import os

    table = pd.read_csv(file_path1, header=0, index_col=None, )  # 导入csv文件，并将第一行作为表头
    table_sat = table.loc[:, col_name]  # 将需要变换坐标的两列提取出来
    table_float = table_sat / 100  # 将原来的整数中加入小数点，如将5258变为52.58
    table_int = table_float.astype(int)  # 提取整数部分52
    table_float_point = (table_float - table_int) * 100 / 60  # 将小数部分由度转变为小数点(小数部分/60）
    table_float_point2 = round(table_float_point, 50)  # 保留5位小数
    table_sat_over = table_int + table_float_point2  # 结合生成新的坐标
    table.loc[:, col_name] = table_sat_over  # 用修改过的坐标列替换原来的坐标列
    np.savetxt(file_path2, table, fmt='%.' + point + 'f', delimiter=',',
               header=','.join(list(table.columns)), comments='')  # 重新保存为csv文件


r"""
单个文件处理调用实例：
degree_to_digit(file_path1=r"C:\Users\Casablanca\Desktop\SURF_CLI_CHN_MUL_DAY-PRE-13011-201905.csv",
                file_path2=r"C:\Users\Casablanca\Desktop\SURF_CLI_CHN_MUL_DAY-PRE-13011-201905.1.csv",
                col_name=['lat', 'lon'])
"""


# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

# 下面这块函数用于处理批量文件
# 下面这块函数用于处理批量文件
# 下面这块函数用于处理批量文件
def degree_to_digit_all(file_path_walk1, file_path_walk2, col_name, point='5'):  # 对csv文件进行批量坐标转换
    # file_path_walk1，字符串，表示初始csv文件所在文件夹的路径
    # file_path_walk2,字符串，表示转换后csv文件所在文件夹的路径
    # col_name，列表，表示纬度度所在列名，设置为一个元素为字符串的列表，每个字符表示列名
    # point,字符串，表示要保留的小数位数，建议十位以内，默认为五位

    import pandas as pd
    import numpy as np
    import glob
    import os

    file_list = glob.glob(file_path_walk1 + '\\' + '*.csv')  # 读取所有需要处理的csv文件路径及名称并存为列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')

    for file_path1 in file_list:  # 遍历上面读取的csv文件路径及名称列表
        file_name = os.path.basename(file_path1)  # 从csv文件路径中提取文件名
        file_path2 = file_path_walk2 + '\\' + file_name  # 设定转换坐标后csv文件存储位置及名称
        degree_to_digit(file_path1, file_path2, col_name, point)  # 调用坐标转换函数
    print('处理完毕！')


r"""
批处理调用实例
degree_to_digit_all(file_path_walk1=r'F:\precipitation\data\PRE_csv', 
                    file_path_walk2=r'F:\precipitation\data\PRE_csv_tran', 
                    col_name=['lat', 'lon'])
"""
