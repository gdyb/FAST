#!/usr/bin/python3
# Help           : Help for all mode
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.10
# Creation Date  : 2022.03.27 - Version 1.0
# Date           : 2022.04.12 - Version 1.11

from FAST_Print import PrintGDD


# 2022-03-27 : 输出支持的数据类型 by Chang Chuntao -> Version : 1.00
# 2022-04-12 : 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
#              by Chang Chuntao  -> Version : 1.10
# 2022-04-22 : 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
#              by Chang Chuntao  -> Version : 1.11
def Supported_Data():
    print("     Supported Data:  BRDC : GPS_brdc / MGEX_brdm ")
    print("")
    print("                       SP3 : GPS_IGS_sp3 / GPS_IGR_sp3 / GPS_IGU_sp3 / GPS_GFZ_sp3 / GPS_GRG_sp3 / ")
    print("                             MGEX_WUH_sp3 / MGEX_WUHU_sp3 / MGEX_GFZ_sp3 / MGEX_COD_sp3 / ")
    print("                             MGEX_SHA_sp3 / MGEX_GRG_sp3 ")
    print("                             GLO_IGL_sp3 ")
    print("")
    print("                     RINEX : GPS_IGS_rnx / MGEX_IGS_rnx / GPS_USA_cors / GPS_HK_cors / GPS_EU_cors / ")
    print("                             GPS_AU_cors")
    print("")
    print("                       CLK : GPS_IGS_clk / GPS_IGR_clk / GPS_IGU_clk / GPS_GFZ_clk / GPS_GRG_clk /  ")
    print("                             GPS_IGS_clk_30s  ")
    print("                             MGEX_WUH_clk / MGEX_COD_clk / MGEX_GFZ_clk / MGEX_GRG_clk / WUH_PRIDE_clk ")
    print("")
    print("                       ERP : IGS_erp / WUH_erp / COD_erp / GFZ_erp/ IGR_erp")
    print("")
    print("                       BIA : MGEX_WHU_bia / GPS_COD_bia / MGEX_COD_bia / MGEX_GFZ_bia")
    print("")
    print("                       ION : IGS_ion / WUH_ion / COD_ion ")
    print("")
    print("                     SINEX : IGS_day_snx / IGS_week_snx / IVS_week_snx / ILS_week_snx / IDS_week_snx ")
    print("")
    print("                    CNES_AR : CNES_post / CNES_realtime ")
    print("")
    print("                       ATX : MGEX_IGS_atx")
    print("")
    print("                       DCB : GPS_COD_dcb / MGEX_CAS_dcb / MGEX_WHU_OSB / P1C1 / P1P2 / P2C2")
    print("")
    print("               Time_Series : IGS14_TS_ENU / IGS14_TS_XYZ / Series_TS_Plot")
    print("")
    print("           Velocity_Fields : IGS14_Venu / IGS08_Venu / PLATE_Venu")
    print("")
    print("                       SLR : HY_SLR / GRACE_SLR / BEIDOU_SLR")
    print("")
    print("                       OBX : GPS_COD_obx / GPS_GRG_obx / MGEX_WUH_obx / MGEX_COD_obx / MGEX_GFZ_obx")
    print("")
    print("                       TRO : IGS_zpd / COD_tro / JPL_tro / GRID_1x1_VMF3 / GRID_2.5x2_VMF1 / GRID_5x5_VMF3")


# 2022-03-27 : 引导模式输出帮助 by Chang Chuntao -> Version : 1.00
def cddhelp():
    print("==================================================================================")
    print("")
    print("     Python program: FAST(Fusion Abundant multi-Source data download Terminal)")
    print("     ©Copyright 2022.01 @ Chang Chuntao")
    print("     PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    Supported_Data()
    print("")
    print("     Chang Chuntao | January 2020: FAST program is compiled in Python and used for GNSS data download.\n"
          "                                   It supports two modes with parameter input and terminal input, and\n"
          "                                   supports multi-threaded download mode. The user can specify the nu-\n"
          "                                   mber of download threads. The program supports multiple data downl-\n"
          "                                   oads (see above). If you have any questions, you can contact me th-\n"
          "                                   rough amst-jazz #wechat and 1252443496 #QQ")
    print("     Auther: Chang Chuntao")
    print("     Organization: The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping")
    print("     Current version date: 2022.03.27 - Version 1.0")
    print("     Initial version date: 2022.04.12 - Version 1.1")
    print("")


# 2022-03-27 : 参数输入模式输出帮助 by Chang Chuntao -> Version : 1.00
def arg_help():
    print("==================================================================================")
    print("")
    print("  FAST : Fusion Abundant multi-Source data download Terminal")
    print("  ©Copyright 2022.01 @ Chang Chuntao")
    print("  PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    arg_options()


# 2022-03-27 : 参数输入模式输出帮助，参数类型帮助 by Chang Chuntao -> Version : 1.00
def arg_options():
    print("  Usage: FAST <options>")
    print("")
    print("  Where the following are some of the options avaiable:")
    print("")
    print("  -v,  --version                   display the version of GDD and exit")
    print("  -h,  --help                      print this help")
    print('  -t,  --type                      GNSS type, if you need to download multiple data,')
    print('                                   Please separate characters with " , "')
    print("                                   Example : GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk")
    print("  -l,  --loc                       which folder is the download in")
    print("  -y,  --year                      where year are the data to be download")
    print("  -d,  --day                       where day are the data to be download")
    print("  -o,  --day1                      where first day are the data to be download")
    print("  -e,  --day2                      where last day are the data to be download")
    print("  -m,  --month                     where month are the data to be download")
    print("  -u,  --uncomprss Y/N             Y - unzip file (default)")
    print("                                   N - do not unzip files")
    print("  -f,  --file                      site file directory,The site names in the file are separated by spaces.")
    print("                                   Example : bjfs irkj urum ")
    print("  -p   --process                   number of threads (default 12)")
    print("")
    print(r"  Example: FAST -t MGEX_IGS_atx")
    print(r"           FAST -t GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk -y 2022 -d 22 -p 30")
    print(r"           FAST -t MGEX_WUH_sp3 -y 2022 -d 22 -u N -l D:\code\CDD\Example")
    print(r"           FAST -t MGEX_IGS_rnx -y 2022 -d 22 -f D:\code\cdd\mgex.txt")
    print(r"           FAST -t IVS_week_snx -y 2022 -m 1")
    print("")
    PrintGDD("是否查看支持的数据类型？(y)", "input")
    cont = input("     ")
    if cont == "y" or cont == "Y":
        Supported_Data()
