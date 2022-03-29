# 此程序用于将站点txt文件转换为csv文件,并增加表头
# 此程序用于将站点txt文件转换为csv文件,并增加表头
# 此程序用于将站点txt文件转换为csv文件,并增加表头
# 转换单个文件时调用txt_csv()函数，设置变量
# 转换多个文件时调用file_path_cycle()函数，设置变量


# 下面这行是txt文件存放路径，用于单个文件使用
# txt_path = "路径"
# 下面这行是生成csv文件的表头，用于单个文件使用
# header_name = 'station,lat,lon,ele,year,month,day,20-8pre,8-20pre,20-20pre,20-8con,8-20con,20-20con'
# 下面这三行是txt文件转csv文件
def txt_csv(txt_path, csv_path, header_name):  # 将单个txt文件转换为csv文件
    # txt_path，字符串，表示需要转换的站点txt文件的路径
    # csv_path，字符串，表示转换后csv文件的存储路径
    # header_name，字符串，表示所需要添加的表头，用","分割

    import numpy as np

    table_2 = np.loadtxt(txt_path).astype(int)  # 读取txt文件
    np.savetxt(csv_path, table_2, fmt='%d', delimiter=',', header=header_name, comments='')  # 保存为csv文件


r"""
# 单个文件处理调用实例：
txt_csv(txt_path=r"C:\Users\Casablanca\Desktop\SURF_CLI_CHN_MUL_DAY-PRE-13011-201905.TXT",
        csv_path=r"C:\Users\Casablanca\Desktop\SURF_CLI_CHN_MUL_DAY-PRE-13011-201905.csv",
        header_name="station,lat,lon,ele,year,month,day,20-8pre,8-20pre,20-20pre,20-8con,8-20con,20-20con")
"""


# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

def txt_csv_all(path1, path2, header_name):  # 这个结合了上面文件路径循环和下面文件名循环，调用了最上面的txt_csv
    # path1，字符串，表示txt文件所在文件夹的路径
    # path2，字符串，表示生成csv文件所存储文件夹的路径
    # header_name，字符串，表示表头名字

    import numpy as np
    import glob
    import os

    txt_list = glob.glob(path1 + '\\*.TXT')  # 将文件夹中所有文件路径存储为列表
    print(u'共发现%s个TXT文件' % len(txt_list))
    print(u'正在处理............')
    for txt_path in txt_list:  # 遍历所有文件路径
        file_name = os.path.basename(txt_path)  # 从文件路径中提取文件名
        csv_path = path2 + "\\" + file_name[:-3] + "csv"  # 指定生成csv文件的路径及名称
        txt_csv(txt_path, csv_path, header_name)  # 调用转换函数
    print('处理完毕！')


r"""
批处理调用实例
txt_csv_all(path1=r'C:\Users\Casablanca\Desktop',
            path2=r'C:\Users\Casablanca\Desktop',
            header_name="station,lat,lon,ele,year,month,day,20-8pre,8-20pre,20-20pre,20-8con,8-20con,20-20con")
"""

# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

# 下面这片用于循环读取同一文件夹下txt（或者其他）文件路径名
# 下面这片用于循环读取同一文件夹下txt（或者其他）文件路径名
# 下面这片用于循环读取同一文件夹下txt（或者其他）文件路径名
"""
def file_path_cycle():  # 循环读取同一文件夹下txt（或者其他）文件路径名
    # 下面一行要用的时候取消注释
    # txt_list = glob.glob('F:\\precipitation\\PRE_txt\\*.txt')
    print(txt_list)
    print(u'共发现%s个txt文件' % len(txt_list))
    print(u'正在处理............')
    for txt_path in txt_list:
        print(txt_path)
"""

# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

# 下面这片用于循环读取同一文件夹下所有文件名
# 下面这片用于循环读取同一文件夹下所有文件名
# 下面这片用于循环读取同一文件夹下所有文件名
"""
def file_name_cycle():  # 循环读取同一文件夹下所有文件名
    # 下面一行要用的时候取消注释
    dir = 'F:\\precipitation\\PRE_txt'
    for root, dir, file_names in os.walk(dir):
        print(u'共发现%s个文件' % len(file_names))
        print(u'正在处理............')
        for file_name in file_names:
            print(file_name)  # 只打印名字
            print(dir, file_names)  #打印路径和名字
"""
