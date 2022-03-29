# 绘制折线图
import glob
import os.path
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

foder_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_daily\*.csv"
flie_list = glob.glob(foder_path)

xdates = []  # 创建日期列表
for i in range(1, 13, 1):
    if i in [4, 6, 9, 11]:
        days = 31
    elif i == 2:
        days = 29
    else:
        days = 32
    for j in range(1, days, 1):
        xdates.append(str(i).zfill(2) + "/" + str(j).zfill(2) + "/2019")

for i in tqdm(flie_list):
    station_number = os.path.basename(i)[:-4]  # 提取站点名称作为图表名称
    table = pd.read_csv(i)
    table[table[["20_20pre", "gpm", "trmm", "cdr", "daily_fusion_extract"]] >= 70] = 0  # 将大于等于70的降雨值替换为0
    plt.figure(figsize=(15, 5), dpi=60)  # 设置图表长宽比
    # plt.xticks(xdates[k] for k in range(len(xdates)))
    x = xdates  # 将日期作为x轴
    y1 = table["20_20pre"]  # 站点数据
    y2 = table["daily_fusion_extract"]  # 融合数据
    y3 = table["trmm"]  # trmm数据
    y4 = table["cdr"]  # cdr数据
    y5 = table["gpm"]  # gpm数据

    plt.title(f"station-{station_number}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式

    # 设置x轴数据
    plt.plot(x, y1, ".", color="k", markersize=10, label="gauge precipitation")
    plt.plot(x, y2, ".", color="r", lw=0.3, label="Fusinon precipitation")
    plt.plot(x, y3, "-.", color="y", lw=0.7, label="TRMM")
    plt.plot(x, y4, "--", color="blue", lw=1, label="PERSIANN-CDR")
    plt.plot(x, y5, "-", color="purple", lw=0.7, label="GPM")

    plt.axis([-5, 370, -2, 70])  # 设置xy轴显示范围
    plt.xticks(xdates[::60], fontproperties='Times New Roman', size=15)  # 设置x轴刻度
    plt.yticks(list(range(0, 75, 10)), fontproperties='Times New Roman', size=15)  # 设置y轴刻度
    plt.xlabel("Date", fontproperties='Times New Roman', size=20)  # 设置x轴标签
    plt.ylabel("precipitation(mm)", fontproperties='Times New Roman', size=20)  # 设置y轴标签
    plt.legend(loc="upper right")  # 显示图例
    plt.grid(b=True, which='major', axis='both', linestyle='--')  # 设置网格线
    # plt.savefig(fr"C:\Users\Casablanca\Desktop\新建文件夹\{station_number}.png", dpi=1500, bbox_inches='tight')  # 保存文件

    # plt.show()
    plt.close()
