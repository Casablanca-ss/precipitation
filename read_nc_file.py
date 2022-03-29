import netCDF4
import numpy as np
import pandas as pd

file1 = r"F:\precipitation\data\cloud\cloud.nc"
# file2 = r"C:\Users\Casablanca\Desktop\3B42RT_Daily.20181231.7.nc4"
file_1 = netCDF4.Dataset(file1)
# file_2 = netCDF4.Dataset(file2)

print(file_1.variables.keys())
print(file_1["longitude"][:],len(file_1["longitude"][:]))
print(file_1["latitude"][:],len(file_1["latitude"][:]))
print(file_1["time"][:],len(file_1["time"][:]))
print(file_1["tcc"][4],len(file_1["tcc"][:]))
print(1051896-1043136)
print("*"*150)
