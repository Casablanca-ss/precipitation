# 该程序用于合并多个csv文件为一个，安全起见注释掉第9行，使用时需要去掉注释


import glob


def hebing():
    # 下面一行要用的时候取消注释
    csv_list = glob.glob(r'F:\CUG\Temperature fusion\Code&Data\Data\*.csv')
    print(u'共发现%s个CSV文件' % len(csv_list))
    print(u'正在处理............')
    for i in csv_list:
        fr = open(i, 'r', encoding='ISO-8859-15')  # .read()
        # print(fr)
        lines = fr.readlines()

        for fr_line in lines:
            if "lat" not in fr_line:
                with open(r'C:\Users\Casablanca\Desktop\alldata.csv', 'a',
                          encoding='ISO-8859-15') as f:
                    f.write(fr_line)
                    print(f)
    print(u'合并完毕！')


"""
代码调用实例
hebing()
"""
hebing()