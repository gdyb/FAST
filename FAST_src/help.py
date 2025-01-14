#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Help           : Help for all mode
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.11
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-09-20 - Version 2.11

from FAST_Print import PrintGDD
from GNSS_TYPE import gnss_type

version = [1.00, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25,
           2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11]

version_time = ['2022-03-27',
                '2022-04-12',
                '2022-04-22',
                '2022-04-30',
                '2022-05-24',
                '2022-05-31',
                '2022-07-03',
                '2022-07-13',
                '2022-07-22',
                '2022-07-28',
                '2022-08-04',
                '2022-09-11',
                '2022-09-16',
                '2022-09-20',
                '2022-09-28',
                '2022-10-10',
                '2022-11-02',
                '2022-11-09',
                '2022-11-10',
                '2022-11-15',
                '2022-12-02',
                '2022-12-04',
                '2023-01-14',
                '2023-02-10',
                '2023-03-17',
                '2023-06-30',
                '2023-08-11',
                '2023-09-20'
                ]


def Supported_Data():
    """
    2022-03-27 :    输出支持的数据类型
                    by Chang Chuntao  -> Version : 1.00
    2022-04-12 :    新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    by Chang Chuntao  -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-05-24 :    + 新增ION内资源WURG_ion、CODG_ion、CORG_ion、UQRG_ion、UPRG_ion、JPLG_ion、JPRG_ion、CASG_ion、
                    CARG_ion、ESAG_ion、ESRG_ion
                    by Chang Chuntao  -> Version : 1.13
    2022-05-31 :    + 新增BIA内资源MGEX_WHU_OSB_bia
                    > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
                    by Chang Chuntao  -> Version : 1.14
    2022-07-03 :    + 新增CLK内资源MGEX_WUHU_clk
                    + 新增ERP内资源WUHU_erp
                    + 新增OBX内资源MGEX_WUHU_obx
                    by Chang Chuntao  -> Version : 1.15
    2022-07-13 :    + 新增SpaceData一级类
                    + 新增SpaceData内资源SW_EOP
                    by Chang Chuntao  -> Version : 1.16
    2022-07-22 :    + 新增SP3内资源MGEX_WUH_Hour_sp3
                    + 新增CLK内资源MGEX_WUH_Hour_clk
                    + 新增ERP内资源WUH_Hour_erp
                    by Chang Chuntao  -> Version : 1.17
    2022-07-27 :    > 修正MGEX_GFZ_sp3 -> MGEX_GFZR_sp3
                    > 修正MGEX_GFZ_clk -> MGEX_GFZR_clk
                    > 修正MGEX_COD_clk资源
                    by Chang Chuntao  -> Version : 1.18
    2022-09-16 :    + 新增RINEX内MGEX_HK_cors资源
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    + 新增TROP内资源Meteorological，为需要站点的气象文件
                    by Chang Chuntao  -> Version : 1.22
    2022-09-28 :    + 新增COSMIC一级类
                    + 新增COSMIC内资源'C1_L1a_leoAtt', 'C1_L1a_opnGps', 'C1_L1a_podCrx','C1_L1b_atmPhs', 'C1_L1b_gpsBit',
                    'C1_L1b_ionPhs', 'C1_L1b_leoClk', 'C1_L1b_leoOrb', 'C1_L1b_podTec', 'C1_L1b_scnLv1', 'C2_L1a_leoAtt',
                    'C2_L1a_opnGps', 'C2_L1a_podCrx', 'C2_L1b_conPhs', 'C2_L1b_leoOrb', 'C2_L1b_podTc2'
    2022-10-10 :    + 新增Tables一级类
                    + 新增Tables内资源'Panda_jpleph_de405', 'Panda_poleut1', 'Panda_EGM','Panda_oceanload',
                    'Panda_oceantide', 'Panda_utcdif','Panda_antnam', 'Panda_svnav', 'Panda_nutabl',
                    'Panda_ut1tid', 'Panda_leap_sec',
                    'Gamit_pmu_bull', 'Gamit_ut1usno', 'Gamit_poleusno','Gamit_dcb_dat', 'Gamit_soltab', 'Gamit_luntab',
                    'Gamit_leap_sec', 'Gamit_nutabl', 'Gamit_antmod','Gamit_svnav', 'Gamit_rcvant'
                    by Chang Chuntao  -> Version : 1.24
    2022-11-09 :    ***自动输出支持的数据类型
                    by Chang Chuntao  -> Version : 2.01
    """
    print("     Supported Data:  BRDC : GPS_brdc / MGEX_brdm \n")
    max_long = 75
    for gs_list in gnss_type[1:]:
        str_len = 27
        str_print = gs_list[0].rjust(26) + ' : '
        for gs_type in gs_list[1]:
            str_print += gs_type
            str_len += len(gs_type)
            if gs_type == gs_list[1][-1]:
                if '\n' in str_print[-29:]:
                    print(str_print)
                else:
                    print(str_print)
                    print()
            if str_len > max_long:
                str_print += '\n                             '
                str_len = 29
            else:
                str_print += ' / '
                str_len += 3


def cddhelp():
    """
    2022-03-27 :    引导模式输出帮助
                    by Chang Chuntao -> Version : 1.00
    2022-04-12 :    Version update
                    by Chang Chuntao -> Version : 1.10
    """
    print("==================================================================================")
    print("")
    print("     Python program: FAST(Fusion Abundant multi-Source data download Terminal)")
    print("     ©Copyright 2022.01 @ Chang Chuntao")
    print("     PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    Supported_Data()
    print("     Chang Chuntao | January 2020: FAST program is compiled in Python and used for GNSS data download.\n"
          "                                   It supports two modes with parameter input and terminal input, and\n"
          "                                   supports multi-threaded download mode. The user can specify the nu-\n"
          "                                   mber of download threads. The program supports multiple data downl-\n"
          "                                   oads (see above). If you have any questions, you can contact me th-\n"
          "                                   rough amst-jazz #wechat and 1252443496 #QQ")
    print("     Auther: Chang Chuntao")
    print("     Organization: The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping")
    print("     Current version date: " + version_time[0] + " - Version " + '%.2f' % version[0])
    print("     Initial version date: " + version_time[-1] + " - Version " + '%.2f' % version[-1])
    print("")


def arg_help():
    """
    2022-03-27 : 参数输入模式输出帮助 by Chang Chuntao -> Version : 1.00
    """
    print("==================================================================================")
    print("")
    print("  FAST : Fusion Abundant multi-Source data download Terminal")
    print("  ©Copyright 2022.01 @ Chang Chuntao")
    print("  PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    arg_options()


def arg_options():
    """
    2022-03-27 :    参数输入模式输出帮助，参数类型帮助
                    by Chang Chuntao -> Version : 1.00
    2023-06-29 :    + "-i", "-site", 输入站点
                    + "-h", "-hour", 输入小时
                    by Chang Chuntao -> Version : 2.09
    """
    print("  Usage: FAST <options>")
    print("")
    print("  Where the following are some of the options avaiable:")
    print("")
    print("  -v,  -version                   display the version of FAST and exit")
    print("  -h,  -help                      print this help")
    print('  -t,  -type                      GNSS type, if you need to download multiple data,')
    print('                                  Please separate characters with " , "')
    print("                                  Example : GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk")
    print("  -l,  -loc                       which folder is the download in [Default pwd]")
    print("  -y,  -year                      where year are the data to be download")
    print("  -d,  -day                       where day   is the   day  to be download")
    print("  -s,  -day1                      where day1  is start day  to be download")
    print("  -e,  -day2                      where day2  is end   day  to be download")
    print("  -hour                           where hour to be download [Default <0 - 23>]")
    print("  -m,  -month                     where month to be download")
    print("  -u,  -uncomprss                 Y - unzip file [Default Y]")
    print("                                  N - do not unzip files")
    print("  -f,  -file                      site file directory,The sites in the file are separated by spaces.")
    print("                                  Example : bjfs irkj urum ")
    print("  -i,  -site                      where sites to be download,The site names are separated by comma.")
    print("                                  Example : bjfs,irkj,urum")
    print("  -p   -process                   number of threads [Default 12]")
    print("")
    print(r"  Example: FAST -t Panda_svnav")
    print(r"           FAST -t GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk -y 2022 -s 22 -e 30 -p 30")
    print(r"           FAST -t MGEX_WHU_F_sp3 -y 2022 -d 22 -u N -l D:\code\CDD\Example")
    print(r"           FAST -t MGEX_IGS_rnx -y 2022 -d 22 -f D:\code\cdd\mgex.txt")
    print(r"           FAST -t MGEX_IGS_rnx -y 2022 -d 22 -i bjfs,abpo")
    print(r"           FAST -t IVS_week_snx -y 2022 -m 1")
    print("")
    PrintGDD("是否查看支持的数据类型？(y)", "input")
    cont = input("     ")
    if cont == "y" or cont == "Y":
        Supported_Data()


def fastSoftwareInformation():
    """
    2022-04-30 :    Software information by Chang Chuntao -> Version : 1.12
    """
    print("==================================================================================")
    print("     FAST           : Fusion Abundant multi-Source data download Terminal")
    print("     Author         : Chang Chuntao")
    print("     Copyright(C)   : The GNSS Center, Wuhan University & ")
    print("                      Chinese Academy of Surveying and mapping")
    print("     Contact        : QQ@1252443496 & WECHAT@amst-jazz GITHUB@ChangChuntao")
    print("     Git            : https://github.com/ChangChuntao/FAST")
    print("                      https://gitee.com/changchuntao/FAST")
    print("     Version        : " + version_time[-1] + " # " + '%.2f' % version[-1])
