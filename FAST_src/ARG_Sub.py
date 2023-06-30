#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ARG_Sub        : Identify program arguments
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.08
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-03-12 - Version 2.08
import datetime
import sys
from FAST_Print import PrintGDD
from FTP_Source import FTP_S
from Format import unzipfile, unzipfile_highrate_rinex2, unzipfile_highrate_rinex3
from GNSS_TYPE import isinGNSStype, yd_type, yds_type, ym_type, s_type, no_type, ydsh_type, ydh_type
import getopt
from Get_Ftp import getftp, getSite, replaceSiteStr, ReplaceTimeWildcard
from help import Supported_Data, arg_options, arg_help, version, version_time


def GET_ARG(cddarg):
    """
    2022-03-27 :    * 获取输入参数
                    by Chang Chuntao -> Version : 1.00
    2023-06-30 :    * 更换参数读取方式， -start 对应为 -s
                    + "-i", "-site", 输入站点
                    + "-h", "-hour", 输入小时
                    by Chang Chuntao -> Version : 2.09
    """
    args = sys.argv
    for argIndex in range(len(args)):
        nowArg = args[argIndex]
        if '-h' == nowArg:
            arg_help()
            sys.exit()
        elif nowArg == '-v' or nowArg == '-version' or nowArg == '-V':
            print(version[-1])
            print(version_time[-1])
            sys.exit()
        elif nowArg in ["-t", "-type"]:
            cddarg["datatype"] = args[argIndex + 1]
        elif nowArg in ["-y", "-year"]:
            cddarg["year"] = int(args[argIndex + 1])
        elif nowArg in ["-l", "-loc"]:
            cddarg["loc"] = args[argIndex + 1]
        elif nowArg in ["-d", "-day"]:
            cddarg["day1"] = int(args[argIndex + 1])
            cddarg["day2"] = int(args[argIndex + 1])
        elif nowArg in ["-s", "-day1", "-start"]:
            cddarg["day1"] = int(args[argIndex + 1])
        elif nowArg in ["-e", "-day2", "-end"]:
            cddarg["day2"] = int(args[argIndex + 1])
        elif nowArg in ["-m", "-month"]:
            cddarg["month"] = int(args[argIndex + 1])
        elif nowArg in ["-hour"]:
            cddarg["hour"] = int(args[argIndex + 1])
        elif nowArg in ["-f", "-file"]:
            cddarg["file"] = args[argIndex + 1]
        elif nowArg in ["-p", "-process"]:
            cddarg["process"] = int(args[argIndex + 1])
        elif nowArg in ["-u", "-uncompress"]:
            cddarg["uncompress"] = int(args[argIndex + 1])
        elif nowArg in ["-i", "-site"]:
            cddarg["file"] = args[argIndex + 1].replace(',', ' ')
    return cddarg


def ARG_ifwrong(cddarg):  # 判断输入参数正确性
    """
    2022-03-27 : 判断输入参数正确性 by Chang Chuntao -> Version : 1.00
    """
    datatype = str(cddarg['datatype']).split(",")
    for dt in datatype:
        if isinGNSStype(dt):  # 判断输入数据类型是否正确
            if dt in ym_type:
                if cddarg['year'] == 0 or cddarg['month'] == 0:
                    PrintGDD("本数据类型需输入年与月，请指定[-y <year>] [-m <month>]！", "fail")
                    sys.exit(2)
            else:
                if dt in yd_type:  # 输入为年， 起始年积日， 终止年积日的数据类型, 判断输入时间是否正确
                    if cddarg['year'] == 0:
                        PrintGDD(
                            "本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！",
                            "fail")
                        sys.exit(2)
                    else:
                        if cddarg['day1'] == 0 and cddarg['day2'] == 0:
                            PrintGDD(
                                "本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！",
                                "fail")
                            sys.exit(2)
                if dt in yds_type or dt in s_type:
                    if cddarg['file'] == "" and cddarg['site'] == "":
                        PrintGDD("本类型需要输入文件位置参数或站点参数，请指定[-f <file>]或者[-i <site>]！", "fail")
                        sys.exit(2)
        else:
            PrintGDD(dt + "数据类型不存在！", "fail")
            PrintGDD("是否需要查看支持数据？(y)", "input")
            cont = input("     ")
            if cont == "y" or "Y":
                Supported_Data()
                sys.exit(2)
            else:
                sys.exit(2)


def geturl(cddarg):
    """
    2022.04.12 :    获取下载列表 by Chang Chuntao -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-09-16 :    新增站点字符串替换子程序
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    + 新增TROP内资源Meteorological，为需要站点的气象文件
                    by Chang Chuntao  -> Version : 1.22
    2022-10-10 :    > 修复无需其他参数输入下载类下载
                    by Chang Chuntao  -> Version : 1.24
    2022-11-09 :    > 修改索引: yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month
                    >         s_type -> site
                    > 删除旧索引: objneedydqd2 / objneedyd1d2loc / objneedloc / objneedn
                    by Chang Chuntao  -> Version : 2.01
    2023-03-12 :    > 修复仅需站点模式
                    by Chang Chuntao  -> Version : 2.08
    2023-06-30 :    + 增加输入小时模式
                    by Chang Chuntao  -> Version : 2.09
    """
    urllist = []
    for dt in str(cddarg['datatype']).split(","):
        typeurl = []
        PrintGDD("数据类型为:" + dt, "normal")

        # 数据类型为无需输入
        if dt in no_type:
            ftpsitelist = getftp(dt, 2022, 1)
            typeurl.append(ftpsitelist)

        # 数据类型为输入年日
        elif dt in yd_type:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(
                cddarg['day2']) + "\n",
                     "normal")
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                url = []
                if len(ftpsitelist) != 0:
                    for ftpsite in ftpsitelist:
                        url.append(ftpsite)
                    typeurl.append(url)

        # 数据类型为输入年日站点文件
        elif dt in yds_type:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(
                cddarg['day2']) + "\n",
                     "normal")
            print("")
            cddarg['site'] = getSite(cddarg['file'], dt)

            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                for siteInList in cddarg['site']:
                    siteftp = []
                    for ftpInList in ftpsitelist:
                        ftpInList = replaceSiteStr(ftpInList, siteInList)
                        siteftp.append(ftpInList)
                    typeurl.append(siteftp)  # 按天下载

        # 数据类型为输入年月文件
        elif dt in ym_type and dt != "IVS_week_snx":
            PrintGDD("下载时间为" + str(cddarg['year']) + "年,月" + str(cddarg['month']) + "\n",
                     "normal")
            print("")
            for day in range(cddarg['month'], cddarg['month'] + 1):
                typeurl = []
                ftpsite = FTP_S[dt]
                ym_datetime = datetime.datetime(cddarg['year'], cddarg['month'], 1)
                for ftp in ftpsite:
                    ftp = ReplaceTimeWildcard(ftp, ym_datetime)
                    typeurl.append([ftp])

        # 数据类型为输入站点文件
        elif dt in s_type:
            cddarg['site'] = getSite(cddarg['file'], dt)
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                for siteInList in cddarg['site']:
                    siteftp = []
                    for ftpInList in ftpsitelist:
                        ftpInList = replaceSiteStr(ftpInList, siteInList)
                        siteftp.append(ftpInList)
                    typeurl.append(siteftp)  # 按天下载

        # 数据类型为输入年日时
        elif dt in ydh_type:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(
                cddarg['day2']) + "\n",
                     "normal")
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                url = []
                if len(ftpsitelist) != 0:
                    for ftpsite in ftpsitelist:
                        url.append(ftpsite)
                    typeurl.append(url)

        # 数据类型为输入年日小时站点文件
        elif dt in ydsh_type:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(
                cddarg['day2']) + "\n",
                     "normal")
            print("")
            cddarg['site'] = getSite(cddarg['file'], dt)
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day,
                                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                          22, 23])  # 通过数据类型与下载时间获取完整下载地址
                for siteInList in cddarg['site']:
                    siteftp = []
                    for ftpInList in ftpsitelist:
                        ftpInList = replaceSiteStr(ftpInList, siteInList)
                        siteftp.append(ftpInList)
                    typeurl.append(siteftp)  # 按天下载
        urllist.append(typeurl)

    return urllist


def uncompress_arg(path, urllist, data_type):
    """
    2022.04.12 :    传入需解压的文件至unzipfile
                    by Chang Chuntao -> Version : 1.10
    2022.11.15 :    新增GRE_IGS_01S判断
                    by Chang Chuntao -> Version : 2.03
    """
    ftpsite = []
    for a1 in urllist:
        for a2 in a1:
            for a3 in a2:
                ftpsite.append(a3)
    if data_type == "GRE_IGS_01S":
        unzipfile_highrate_rinex2(path, ftpsite)
    elif data_type == "GCRE_MGEX_01S":
        unzipfile_highrate_rinex3(path, ftpsite)
    else:
        unzipfile(path, ftpsite)


