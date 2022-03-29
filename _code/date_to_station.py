# 此程序用于将按照月份分文件保存的站点数据重新组合为按照站点编号分文件保存，我的处理文件多了一列，因此date_to_station1()中增加了删除那一列的功能，使用者只需要调用date_to_station2()就可以了
# 此程序用于将按照月份分文件保存的站点数据重新组合为按照站点编号分文件保存，我的处理文件多了一列，因此date_to_station1()中增加了删除那一列的功能，使用者只需要调用date_to_station2()就可以了
# 此程序用于将按照月份分文件保存的站点数据重新组合为按照站点编号分文件保存，我的处理文件多了一列，因此date_to_station1()中增加了删除那一列的功能，使用者只需要调用date_to_station2()就可以了
# 由于存在同一站点经纬度存在偏差的情况，station_modify()用于修改这些偏差，使得同一站点经纬度统一
# 由于存在同一站点经纬度存在偏差的情况，station_modify()用于修改这些偏差，使得同一站点经纬度统一
# 由于存在同一站点经纬度存在偏差的情况，station_modify()用于修改这些偏差，使得同一站点经纬度统一
# all_station()用于将不同站点标号及对应坐标存放在一个csv文件中（ps：进行这一步之前需要先将经纬度存在偏差的坐标进行统一，即使用station_modify()函数）
# all_station()用于将不同站点标号及对应坐标存放在一个csv文件中（ps：进行这一步之前需要先将经纬度存在偏差的坐标进行统一，即使用station_modify()函数）
# all_station()用于将不同站点标号及对应坐标存放在一个csv文件中（ps：进行这一步之前需要先将经纬度存在偏差的坐标进行统一，即使用station_modify()函数）

def date_to_station1(file_path1, file_path2, col_name, ):
    # file_path1，字符串，表示初始csv文件所在文件夹的路径
    # file_path2， 字符串，表示重组后csv文件所在文件夹的路径
    # col_name，字符串，表示站点编号所在列的列名

    import numpy as np
    import pandas as pd
    import glob

    file_list = glob.glob(file_path1 + '\\' + '*.xls')  # 读取所有需要处理的xls文件路径及名称并存为列表
    list_list = []  # 创建一个空列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    for i in file_list:  # 遍历所有需要处理的csv文件
        table = pd.read_excel(i)  # 逐个读取csv文件
        list_list.append(table)  # 逐个将csv文件存入上面的空列表
    merge_list = pd.concat(list_list)  # 将所有csv文件拼接为一个

    for j in set(merge_list[col_name]):  # 将所有站点按照编号进行分类，并遍历所有站点编号
        station_data = merge_list.loc[merge_list[col_name] == j]  # 读取单个站点数据
        ppp = station_data.drop(labels="FID", axis=1, )  # 删除多余的一列
        file_path = file_path2 + "\\" + str(j) + ".csv"  # 设定重组后csv文件存储位置及名称
        np.savetxt(file_path, ppp,  # 保存csv文件
                   fmt='%.5' + 'f',
                   delimiter=',',
                   header=','.join(list(ppp.columns)),
                   comments='')
    print('处理完毕！')


r"""
处理调用实例
date_to_station1(file_path1=r'F:\precipitation\data\PRE_excel_csv',
                file_path2=r"C:\Users\Casablanca\Desktop\pp",
                col_name="station")
"""


# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

def date_to_station2(file_path1, file_path2, col_name, ):
    # file_path1，字符串，表示初始csv文件所在文件夹的路径
    # file_path2， 字符串，表示重组后csv文件所在文件夹的路径
    # col_name，字符串，表示站点编号所在列的列名

    import numpy as np
    import pandas as pd
    import glob

    file_list = glob.glob(file_path1 + '\\' + '*.xls')  # 读取所有需要处理的xls文件路径及名称并存为列表
    list_list = []  # 创建一个空列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    for i in file_list:  # 遍历所有需要处理的csv文件
        table = pd.read_excel(i)  # 逐个读取csv文件
        list_list.append(table)  # 逐个将csv文件存入上面的空列表
    merge_list = pd.concat(list_list)  # 将所有csv文件拼接为一个

    for j in set(merge_list[col_name]):  # 将所有站点按照编号进行分类，并遍历所有站点编号
        station_data = merge_list.loc[merge_list[col_name] == j]  # 读取单个站点数据

        file_path = file_path2 + "\\" + str(j) + ".csv"  # 设定重组后csv文件存储位置及名称
        np.savetxt(file_path, station_data,  # 保存csv文件
                   fmt='%.5' + 'f',
                   delimiter=',',
                   header=','.join(list(station_data.columns)),
                   comments='')
    print('处理完毕！')


r"""
代码调用实例
date_to_station2(file_path1=r'F:\precipitation\data\PRE_excel_csv',
                 file_path2=r"C:\Users\Casablanca\Desktop\pp",
                 col_name="station")
"""


# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

def station_modify(file_path1, file_path2, lat, lon):  # 该程序用于修改同一站点经纬度的偏差，统一修改为该站点所有经纬度的均值
    # file_path1，字符串，表示初始csv文件所在文件夹的路径
    # file_path2， 字符串，表示修改后后csv文件所在文件夹的路径
    # lat，字符串，表示纬度所在列的列名
    # lon，字符串，表示经度所在列的列名

    import numpy as np
    import pandas as pd
    import glob
    import os

    file_list = glob.glob(file_path1 + '\\' + '*.csv')  # 读取所有需要处理的csv文件路径及名称并存为列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    for i in file_list:
        table = pd.read_csv(i)

        table.loc[:, [lat, lon]] = [np.mean(list(set(table[lat]))), np.mean(list(set(table[lon])))]

        file_path = file_path2 + "\\" + os.path.basename(i)  # 设定重组后csv文件存储位置及名称
        np.savetxt(file_path, table,  # 保存csv文件
                   fmt='%.5' + 'f',
                   delimiter=',',
                   header=','.join(list(table.columns)),
                   comments='')
    print('处理完毕！')


r"""
代码运用实例
station_modify(file_path1=r'F:/precipitation/data/date_to_station',
               file_path2=r'C:\Users\Casablanca\Desktop\qqq',
               lat="lat",
               lon="lon")
"""


# **********************************************************************************************************************
#                                   分                   隔                     符
# **********************************************************************************************************************

def all_station(file_path1, file_path2, station, lat,
                lon):  # 该程序用于将不同站点标号及对应坐标存放在一个csv文件中（ps：进行这一步之前需要先将经纬度存在偏差的坐标进行统一）
    # file_path1，字符串，表示初始csv文件所在文件夹的路径
    # file_path2，字符串，表示生成csv文件路径，注意要在最后指定生成文件类型，例如文件名应为std.csv而不是std
    # station，字符串，表示站点编号所在列的列名
    # lat，字符串，表示纬度所在列的列名
    # lon，字符串，表示经度所在列的列名

    import numpy as np
    import pandas as pd
    import glob

    file_list = glob.glob(file_path1 + '\\' + '*.csv')  # 读取所有需要处理的csv文件路径及名称并存为列表
    print(u'共发现%s个csv文件' % len(file_list))
    print(u'正在处理............')
    list1 = []  # 创建一个空列表用来存储各个站点编号
    list2 = []  # 创建一个空列表用来存储各个站点纬度
    list3 = []  # 创建一个空列表用来存储各个站点经度
    for i in file_list:  # 遍历所有csv文件
        table = pd.read_csv(i)  # 逐个读取csv文件
        aaa = list(set(table["station"]))  # 获取逐个站点编号
        bbb = list(set(table["lat"]))  # 获取逐个站点纬度
        ccc = list(set(table["lon"]))  # 获取逐个站点经度
        list1.append(aaa[0])  # 将获取的站点编号存为列表
        list2.append(bbb[0])  # 将获取的站点纬度存为列表
        list3.append(ccc[0])  # 将获取的站点经度存为列表

    tt = [list1, list2, list3]  # 将三个列表进行合并
    qq = np.array(tt).T  # 将合并后列表进行转置，并且转换为数组
    np.savetxt(file_path2, qq,  # 保存csv文件
               fmt='%.5' + 'f',
               delimiter=',',
               header=station + "," + lat + "," + lon,
               comments='')
    print('处理完毕！')


r"""
代码调用实例
all_station(file_path1=r'F:\precipitation\data\station_modify',
            file_path2=r'C:\Users\Casablanca\Desktop\qqq\ppp.csv',
            station="station",
            lat="lat",
            lon="lon")
"""
