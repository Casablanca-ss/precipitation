import date_to_station as dts
import station_tran as st

dts.all_station(file_path1=r'F:\precipitation\data\station_modify',
                file_path2=r'C:\Users\Casablanca\Desktop\ppp\ppp.csv',
                station="station",
                lat="lat",
                lon="lon")

st.degree_to_digit(file_path1=r"C:\Users\Casablanca\Desktop\ppp\ppp.csv",
                   file_path2=r"C:\Users\Casablanca\Desktop\SURF_CLI_CHN_MUL_DAY-PRE-13011-201905.1.csv",
                   col_name=['lat', 'lon'])
