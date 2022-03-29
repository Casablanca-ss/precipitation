# 该程序用于在csv文件第一行加入列名，只能运行一次，多运行会重复加表头
# 该程序用于在csv文件第一行加入列名，只能运行一次，多运行会重复加表头
# 该程序用于在csv文件第一行加入列名，只能运行一次，多运行会重复加表头
# 重要的事情说三遍！！！
import os


# os.mkdir(r"C:\Users\Casablanca\Desktop\aaa.txt")
# os.remove(r"C:\Users\Casablanca\Desktop\aaa.txt",)
#
# with open(r"C:\Users\Casablanca\Desktop\aaa.txt", "a+") as txt:
#     # txt.write("woaixuepython\n")
#
#     txt.write("ppp")
def csv_add(path1):
    with open(path1, "r") as txt:
        lines = txt.read()
    with open(path1, "w") as txt:
        txt.write("station,lat,lon,ele,year,month,day,20-8pre,8-20pre,20-20pre,20-8con,8-20con,20-20con\n")
    with open(path1, "a") as txt:
        txt.write(lines)


paths = []
for root, dirs, allfile_path in os.walk(r"F:\precipitation\降水(PRE2019)"):
    print(allfile_path)
    for path_all in allfile_path:
        if os.path.splitext(path_all)[1] == ".csv":
            paths.append(os.path.join(root, path_all))
print(paths)
for path in paths:
    print(path)
    csv_add(path)

# print(txt)
