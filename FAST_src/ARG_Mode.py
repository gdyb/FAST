#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ARG_Mode       : Program running with arguments
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.09
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-06-30 - Version 2.09
import datetime
import os
from ARG_Sub import GET_ARG, ARG_ifwrong, geturl
from Dowload import argpooldownload, lftps
from FTP_Source import FTP_S
from Format import unzip_vlbi
from Get_Ftp import ReplaceMMM


def ARG_Mode():
    """
    2022-03-27 :    输入参数模式主函数 by Chang Chuntao -> Version : 1.00
    2022-04-12 :    新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    by Chang Chuntao  -> Version : 1.10
    2022-11-09 :    > 修改索引: yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month
                    >         s_type -> site
                    > 删除旧索引: objneedydqd2 / objneedyd1d2loc / objneedloc / objneedn
                    by Chang Chuntao  -> Version : 2.01
    2023-06-30 :    + 增加小时参数
                    by Chang Chuntao  -> Version : 2.09
    """
    # PrintGDD("GDD 下载程序启动!", "important")
    cddarg = {"datatype": "", "year": 2022, "loc": "", "day1": 1, "day2": 1, "month": 1, "file": "", "process": 4,
              "site": "", "uncompress": "y", 'hour': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                                      18, 19, 20, 21, 22, 23]}
    cddarg = GET_ARG(cddarg)  # 获取参数内容
    if cddarg is None:
        return
    ARG_ifwrong(cddarg)  # 判断输入参数正确性

    # 数据类型为IVS_week_snx, lftp下载
    if cddarg['datatype'] == "IVS_week_snx":
        nowdir = os.getcwd()
        if len(cddarg["loc"]) == 0:
            os.chdir(nowdir)
        else:
            os.chdir(cddarg["loc"])
        ftpsite = FTP_S[cddarg['datatype']][0]
        ftpsite = ftpsite.replace('<YY>', str(cddarg['year'])[2:4])
        ftpsite = ReplaceMMM(ftpsite, cddarg['month'])
        lftps(ftpsite)
        if cddarg["uncompress"] == "y" or cddarg["uncompress"] == "Y":
            unzip_vlbi(cddarg["loc"], ftpsite)
    else:
        urllist = geturl(cddarg)  # 判断下载列表
        argpooldownload(urllist, cddarg["process"], cddarg["loc"], cddarg["uncompress"], cddarg['datatype'])  # 并行下载
