#!/usr/bin/python3
# -*- coding: utf-8 -*-
# CDD_Sub        : Format conversion subroutine
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.09
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-06-30 - Version 2.09

import os
import platform
import shutil
import subprocess
import sys
import time
from FAST_Print import PrintGDD
from Get_Ftp import ReplaceTimeWildcard
from GNSS_Timestran import gnssTime2datetime, datetime2GnssTime
from pubFuncs import mkdir, EmptyFolder
import pubFuncs


def isinpath(file):  # 判断相关文件是否存在
    """
    2022-03-27 :    判断文件在本地是否存在
                    by Chang Chuntao    -> Version : 1.00
    2022-09-09 :    > 修正广播星历文件判定
                    by Chang Chuntao    -> Version : 1.20
    2022-11-15 :    > 增加高采样率判定
                    by Chang Chuntao    -> Version : 2.03
    2023-01-14 :    > 修正SP3 CLK判定
                    by Chang Chuntao    -> Version : 2.06
    2023-03-17 :    > 重写本地文件判定
                    by Chang Chuntao    -> Version : 2.08
    2023-06-30 :    + 增加高采样率文件判断
                    + 增加igu文件的判断
                    by Chang Chuntao    -> Version : 2.09
    """
    orifile = str(file).split(".")[0]
    ionfile = file
    projectFileLow = file
    filelowo = file
    filelowd = file
    filelowp = file
    filelown = file
    fileprolow = file
    rtrFile = file
    rtsFile = file
    projectFileUpper = file
    if len(orifile) > 9:
        ionfile = file.lower()[0:4] + 'g' + file.lower()[16:20] + "." + file.lower()[14:16] + "i"
        if '.SP3' in file or '.CLK' in file or '.OBX' in file or '.ERP' in file or '.ION' in file \
                or '.BIA' in file or '.TRO' in file:
            year = file.lower()[11:15]
            doy = file.lower()[15:18]
            specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
            [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
            proType = str(file).split(".")[-2].lower()
            if 'IGS0OPS' in file:
                if 'FIN' in file:
                    sp3_flag = 's'
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + "." + proType
                elif 'RAP' in file:
                    sp3_flag = 'r'
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + "." + proType
                elif 'ULT' in file:
                    sp3_flag = 'u'
                    hh = file[18:20]
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + '_' + hh + "." + proType
                else:
                    sp3_flag = 's'
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + "." + proType

            elif 'COD0OPSRAP_' in file:
                projectFileLow = 'COD<GPSWD>.EPH_M'
                projectFileLow = ReplaceTimeWildcard(projectFileLow, specTime)
            else:
                projectFileLow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + "." + proType
        elif '.SNX' in file:
            year = file.lower()[11:15]
            doy = file.lower()[15:18]
            specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
            [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
            if '_SOL' in file:
                if 'IGS0OPSSNX' in file and '01D_01D_SOL' in file:
                    projectFileLow = file.lower()[0:3] + str(YearMonthDay[0])[:2] + 'P' + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + ".snx"
                elif 'IGS0OPSSNX' in file and '07D_07D_SOL' in file:
                    projectFileLow = file.lower()[0:3] + str(YearMonthDay[0])[:2] + 'P' + str(GPSWeekDay[0]) + ".snx"
                else:
                    projectFileLow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".snx"
            else:
                projectFileLow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".ssc"
        elif 'CH-OG-1-SST' in file:
            projectFileLow = str(file).replace('.zip', '') + '.rnx'
            filelowo = orifile[:27] + '.rnx'
        elif 'igu' in file and 'sp3' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            hour = file[9:11]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSULT_<YYYY><DOY><nowHour>00_02D_15M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
            projectFileUpper = str(projectFileUpper).replace('<nowHour>', hour)
        else:
            filelowo = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"
            filelowd = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
            filelowp = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
            fileprolow = file.lower()[0:4] + file.lower()[16:20] + ".bia"
            rtrFile = str(rtrFile).replace('_S_', '_R_')
            rtrFile = str(rtrFile).replace('_R_', '_R_')
            rtsFile = str(rtsFile).replace('_R_', '_S_')
            rtsFile = str(rtsFile).replace('_S_', '_S_')
    else:
        if 'igs' in file and '.sp3' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igr' in file and '.sp3' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igs' in file and '.clk' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSFIN_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igr' in file and '.clk' in file and '30s' not in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSRAP_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igr' in file and '.clk' in file and '30s' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'COD' in file and '.EPH_M.Z' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'COD0OPSRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'codg' in file and 'i.Z' in file:
            doy = file[4:7]
            yyyy = str(2000 + int(file[9:11]))
            specTime = gnssTime2datetime(yyyy + " " + doy, "YearDoy")
            projectFileUpper = 'COD0OPSFIN_<YYYY><DOY>0000_01D_01H_GIM.INX'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        filelowo = file.lower()[0:11] + "o"
        filelowd = file.lower()[0:11] + "d"
        filelowp = file.lower()[0:11] + "p"
        filelown = file.lower()[0:11] + "n"
        fileprolow = file.lower()[0:12]
    projectFileLowGz = projectFileLow + '.gz'
    projectFileLowZ = projectFileLow + '.Z'
    projectFileUpperGz = projectFileUpper + '.gz'
    projectFileUpperZ = projectFileUpper + '.Z'
    highrate_file = file.split('.tar')[0][:-1] + 'o'
    fileUnzip = str(file).replace('.' + file.split('.')[-1], '')
    highrate_file_mgex = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"
    filelowoZ = filelowo + '.Z'
    filelowogz = filelowo + '.gz'
    filelowdZ = filelowd + '.Z'
    filelowdgz = filelowd + '.gz'
    filelowpZ = filelowp + '.Z'
    filelowpgz = filelowp + '.gz'
    filelownZ = filelown + '.Z'
    filelowngz = filelown + '.gz'
    if os.path.exists(file[0:-2]) or os.path.exists(file[0:-3]) \
            or os.path.exists(file) or os.path.exists(file.replace('05M', '15M')) or os.path.exists(projectFileLowZ) or os.path.exists(projectFileLowGz) \
            or os.path.exists(file.replace('15M', '05M')) or os.path.exists(highrate_file) or os.path.exists(highrate_file_mgex) or os.path.exists(filelowo) \
            or os.path.exists(filelowd) or os.path.exists(filelowp) or os.path.exists(filelown) \
            or os.path.exists(fileprolow) or os.path.exists(ionfile) or os.path.exists(projectFileLow) \
            or os.path.exists(fileUnzip) or os.path.exists(projectFileUpperGz) or os.path.exists(projectFileUpperZ) \
            or os.path.exists(projectFileUpper) or os.path.exists(filelowoZ) or os.path.exists(filelowogz)\
            or os.path.exists(filelowdZ) or os.path.exists(filelowdgz) or os.path.exists(filelowpZ) \
            or os.path.exists(rtrFile) or os.path.exists(rtsFile) \
            or os.path.exists(filelowpgz) or os.path.exists(filelownZ) or os.path.exists(filelowngz):
        return True
    else:
        return False


"""
    2022-03-27 :    判断操作平台，获取bin下格式转换程序    
                    by Chang Chuntao    -> Version : 1.00
    2022-09-16 :    更新索引                           
                    by Chang Chuntao    -> Version : 1.21
    2022-11-15 :    增加teqc                          
                    by Chang Chuntao    -> Version : 2.03
    2022-12-04 :    增加tgz解压
                    by Chang Chuntao    -> Version : 2.05
    2023-03-18 :    增加zip解压
                    by Chang Chuntao    -> Version : 2.08
"""
tar = 'tar -xf '

if platform.system() == 'Windows':
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
    unzip = os.path.join(dirname, 'bin', 'gzip.exe')
    unzip += " -d "
    unzip_tgz = 'tar -xvzf'
    unzip_zip = os.path.join(dirname, 'bin', 'unzip.exe') + ' '
    crx2rnx = os.path.join(dirname, 'bin', 'crx2rnx.exe')
    crx2rnx += " "
    teqc = os.path.join(dirname, 'bin', 'teqc.exe')
    teqc += ' '
    gfzrnx_exe = os.path.join(dirname, 'bin', 'gfzrnx_win.exe')
    gfzrnx = gfzrnx_exe + ' '
elif platform.system() == 'Darwin':
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
    crx2rnx = os.path.join(dirname, 'mac_bin', 'crx2rnx')
    crx2rnx += ' '
    unzip_tgz = 'tar -xvzf '
    uncompress = os.path.join(dirname, 'mac_bin', 'gunzip')
    unzip_zip = os.path.join(dirname, 'mac_bin', 'gunzip') + ' '
    unzip = uncompress + ' '
    teqc = os.path.join(dirname, 'mac_bin', 'teqc')
    teqc += ' '
    gfzrnx_exe = os.path.join(dirname, 'mac_bin', 'gfzrnx')
    gfzrnx = gfzrnx_exe + ' '
else:
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
    crx2rnx = os.path.join(dirname, 'bin', 'crx2rnx')
    crx2rnx += ' '
    unzip_tgz = 'tar -xvzf '
    uncompress = os.path.join(dirname, 'bin', 'uncompress')
    unzip_zip = os.path.join(dirname, 'bin', 'unzip') + ' '
    unzip = uncompress + ' '
    teqc = os.path.join(dirname, 'bin', 'teqc')
    teqc += ' '
    gfzrnx_exe = os.path.join(dirname, 'bin', 'gfzrnx_linux')
    gfzrnx = gfzrnx_exe + ' '


def uncompresss(file):
    """
    2022-03-27 :    解压单个文件
                    by Chang Chuntao    -> Version : 1.00
    2022-11-15 :    支持CentOS
                    by Chang Chuntao    -> Version : 2.03
    2022-12-04 :    支持tgz解压/COD产品更名
                    by Chang Chuntao    -> Version : 2.05
    """
    if not os.path.isfile(file):
        return
    if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz" or file.split(".")[-1] == "tgz" or\
            file.split(".")[-1] == "ZIP" or file.split(".")[-1] == "zip":
        if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz":
            try:
                cmd_list = [unzip[:-1], file]
                p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except:
                cmd = unzip + file
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif file.split(".")[-1] == "ZIP" or file.split(".")[-1] == "zip":
            if platform.system() == 'Windows':
                cmd = unzip_zip + file
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                try:
                    cmd_list = [unzip_zip[:-1], file]
                    p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                except:
                    cmd = unzip_zip + file
                    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            try:
                cmd_list = [unzip_tgz[:-1], file]
                p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except:
                cmd = unzip_tgz + file
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        PID = p.pid
        completely = True
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                line = line.decode('gbk')
                if 'x ' in line:
                    PrintGDD("更名：" + line[2:], "normal")
                if 'unexpected end of file' in line:
                    completely = False
            if PID == 0:
                break
        if completely:
            # PrintGDD('压缩文件完好 -> ' + file + ', 已成功解压！', 'warning')
            if os.path.exists(file):
                os.remove(file)
            if file.split(".")[-1] == "tgz":
                if os.path.isfile(file):
                    os.remove(file)
        else:
            PrintGDD('压缩文件破损 -> ' + file + ', 未成功解压！', 'warning')


def crx2rnxs(file):
    """
    2022-03-27 : crx2rnx by Chang Chuntao -> Version : 1.00
    """
    if file[-3:-1].isdigit() and file[-1] == "d":
        ofile = file[:-1] + 'o'
        if not os.path.isfile(ofile):
            cmd = crx2rnx + file
            os.system(cmd)


def crx2d(file):
    """
    2022-03-27 :    crx更名为d by Chang Chuntao -> Version : 1.00
    """
    if file.split(".")[-1] == "crx":
        filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
        if not os.path.isfile(filelow):
            os.rename(file, filelow)
            PrintGDD("更名：" + filelow, "normal")
    return filelow


def renamebrdm(file):
    """
    2022-03-27 :    BRDM长名更名为brdm短名 by Chang Chuntao -> Version : 1.00
    """
    filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
    if not os.path.isfile(filelow):
        os.rename(file, filelow)
        PrintGDD("更名：" + filelow, "normal")


def unzip_vlbi(path, ftpsite):
    """
    2022-03-27 :    解压vlbi文件 by Chang Chuntao -> Version : 1.00
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开", "normal")
    dirs = os.listdir(path)
    for filename in dirs:
        if ftpsite[83:88] == filename[0:5] and filename.split(".")[-1] == "gz":
            uncompresss(filename)


def unzipfile(path, ftpsite):
    """
    2022.04.12 :    通过下载列表解压相应文件
                    by Chang Chuntao -> Version : 1.10
    2022.12.04 :    BRDC/BRDM/BRD4更名
                    by Chang Chuntao -> Version : 2.05
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    all_zip_file = []
    for ftp in ftpsite:
        zipfilename = str(ftp).split("/")[-1]
        if os.path.exists(zipfilename) and zipfilename not in all_zip_file:
            uncompresss(zipfilename)
            all_zip_file.append(zipfilename)
    dirs = os.listdir(path)
    for filename in dirs:
        if filename[-3:-1].isdigit() or filename.split(".")[-1] == "crx":
            if filename.split(".")[-1] == "crx" or filename[-1] == "d":
                PrintGDD("目录内含有crx文件，正在进行格式转换！", "normal")
                break
    for filename in dirs:
        if filename.split(".")[-1] == "crx":
            crx2d(filename)

    dirs = os.listdir(path)
    for filename in dirs:
        if filename[-1] == "d" and filename[-3:-1].isdigit():
            crx2rnxs(filename)
            time.sleep(0.1)
            os.remove(filename)

    dirs = os.listdir(path)
    for filename in dirs:
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRDM":
            renamebrdm(filename)
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRDC":
            renamebrdm(filename)
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRD4":
            renamebrdm(filename)
    os.chdir(nowdir)


def unzipfile_highrate_rinex2(path, ftpsite):
    """
    2022.11.15 : 通过下载列表解压高采样率文件并转换合并 by Chang Chuntao -> Version : 2.03
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    all_zip_file = []
    for ftp in ftpsite:
        zipfilename = str(ftp).split("/")[-1]
        if not os.path.exists(zipfilename):
            continue
        if zipfilename in all_zip_file:
            continue
        all_zip_file.append(zipfilename)

        # site_dir = os.path.join(nowdir, zipfilename.split('.')[0])
        # merge_file = os.path.join(nowdir, zipfilename.split('.tar')[0][:-1]) + 'o'
        # mkdir(site_dir, isdel=True)
        # shutil.copy2(zipfilename, site_dir)
        # os.chdir(site_dir)
        # tar_cmd = tar + zipfilename
        # os.system(tar_cmd)
        # now_gfz_cmd = gfzrnx + '-finp '
        # for root, dirs, files in os.walk(site_dir):
        #     for filename in files:
        #         if '.gz' not in filename:
        #             continue
        #         now_gz_file = os.path.join(root, filename)
        #         now_crx_file = os.path.join(root, filename.split('.gz')[0])
        #         now_rnx_file = filename.split('.gz')[0][:-1] + 'o'
        #
        #         now_zip_cmd = unzip + now_gz_file
        #         os.system(now_zip_cmd)
        #
        #         now_crx2rnx_cmd = crx2rnx + now_crx_file
        #         os.system(now_crx2rnx_cmd)
        #
        #         now_gfz_cmd += now_rnx_file + ' '
        # now_gfz_cmd += '-fout ' + merge_file
        # os.system(now_gfz_cmd)
    os.chdir(nowdir)


def unzipfile_highrate_rinex3(path, ftpsite):
    """
    2022.11.15 :    通过下载列表解压高采样率文件并转换合并
                    by Chang Chuntao -> Version : 2.03
    """
    from GNSS_Timestran import doy2datetime, datetime2doy
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    siteList = {}
    for ftp in ftpsite:
        zipfilename = os.path.basename(ftp)
        siteName = zipfilename[:9]
        if not os.path.exists(zipfilename):
            continue
        if siteName not in siteList:
            siteList[siteName] = {}
        siteYear = int(zipfilename[12:16])
        siteDoy = int(zipfilename[16:19])
        siteTime = doy2datetime(siteYear, siteDoy)
        if siteTime not in siteList[siteName]:
            siteList[siteName][siteTime] = []
        if zipfilename not in siteList[siteName][siteTime]:
            siteList[siteName][siteTime].append(zipfilename)
    for siteName in siteList:
        sitePath = os.path.join(path, siteName)
        mkdir(sitePath)
        for siteTime in siteList[siteName]:
            nowYear, nowDoy = datetime2doy(siteTime)
            siteTimePath = os.path.join(sitePath, str(nowYear) + '%03d' % nowDoy)
            mkdir(siteTimePath)
            merge_file = os.path.join(nowdir, siteList[siteName][siteTime][0].lower()[0:4] +
                                      siteList[siteName][siteTime][0].lower()[16:20] + "." +
                                      siteList[siteName][siteTime][0].lower()[14:16] + "o")
            now_gfz_cmd = gfzrnx + '-finp '
            for siteFileZ in siteList[siteName][siteTime]:
                siteFile = str(siteFileZ).replace('.gz', '')
                uncompresss(siteFileZ)
                siteFileInTimePath = os.path.join(siteTimePath, siteFile)
                pubFuncs.moveFile(siteFile, siteTimePath)
                dfile = siteFile.lower()[0:4] + siteFile.lower()[16:20] + siteFile[19:23] + "." + siteFile.lower()[14:16] + "d"
                ofile = siteFile.lower()[0:4] + siteFile.lower()[16:20] + siteFile[19:23] + "." + siteFile.lower()[14:16] + "o"
                dfileInPath = os.path.join(siteTimePath, dfile)
                ofileInPath = os.path.join(siteTimePath, ofile)
                pubFuncs.moveFile(siteFileInTimePath, dfileInPath)
                crx2rnxs(dfileInPath)
                os.remove(dfileInPath)
                now_gfz_cmd += ofileInPath + ' '
            now_gfz_cmd += ' -satsys GCRE -fout ' + merge_file
            os.system(now_gfz_cmd)
            EmptyFolder(siteTimePath)
        os.chdir(nowdir)