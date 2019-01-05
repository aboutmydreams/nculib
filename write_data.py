#-*- coding: utf-8 -*-
import os,time,datetime,xlrd
from xlrd import open_workbook
from xlutils.copy import copy
def get_timemin():
    now_time0 = '[\''+time.ctime().replace(':','\',\'').replace(' ','\',\'')+'\']'
    now_time = eval(now_time0)
    return now_time
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=str(today-oneday).replace('-','')
    return yesterday
def today():
    today = str(datetime.date.today()).replace('-','')
    return today
'''
# 定义要创建的目录
#mkpath="data"
#mkdir(mkpath)
'''
def write_actname(time1):
    fa = open('data/allact.txt','a')
    fa.write(time1+'\n')
    fa.close()

def read_actname():
    fa = open('data/allact.txt','r')
    ac_list = eval(str(fa.readlines()).replace('\\n',''))
    return ac_list

def write_set(time1,time2,title,num):
    f = open('data/time.txt','w')
    f.write(time1+'\n'+time2+'\n'+title+'\n'+num)
    f.close()
    is_e = os.path.exists('data/log/{}.txt'.format(time1))
    if is_e:
        pass
        print('存在')
    else:
        f1 = open('data/log/{}.txt'.format(time1),'w')
        f1.write('[]')
        f1.close()
        write_actname(time1)

def read_set():
    f = open('data/time.txt','r')
    sets = eval(str(f.readlines()).replace('\\n',''))
    f.close()
    return sets

def now_num():
    near_time = read_set()[0]
    f = open('data/log/{}.txt'.format(near_time),'r')
    data = eval(f.read())
    num = len(data)
    f.close()
    return str(num) 

def baoming(name,phone):
    data = []
    hour = get_timemin()[-4]
    near_time = read_set()[0]
    f = open('data/log/{}.txt'.format(near_time),'r')
    data0 = eval(f.read())
    name_list = []
    if len(data0)!=0:
        for i in data0:
            name_list.append(i[0])
        if name in name_list:
            name_site = name_list.index(name)
            data0[name_site][-1]=phone
            print(name_site)
            f.close()
            f = open('data/log/{}.txt'.format(near_time),'w')
            fs = open('data/ban.json','r')
            f.write(str(data0))
            f.close()
        else:
            pass
            f.close()
            f = open('data/log/{}.txt'.format(near_time),'w')
            fs = open('data/ban.json','r')
            ban_list_zidian = eval(fs.read())
            if name in ban_list_zidian:
                this_ban = ban_list_zidian['{}'.format(name)]
            else:
                this_ban = ''
            data.append(name)
            data.append(this_ban)
            data.append(phone)
            data0.append(data)
            f.write(str(data0))
            f.close()
    else:
        f.close()
        f = open('data/log/{}.txt'.format(near_time),'w')
        fs = open('data/ban.json','r')
        ban_list_zidian = eval(fs.read())
        if name in ban_list_zidian:
            this_ban = ban_list_zidian['{}'.format(name)]
        else:
            this_ban = ''
        data.append(name)
        data.append(this_ban)
        data.append(phone)
        data0.append(data)
        f.write(str(data0))
        f.close()

def get_qinkuang():
    near_time = read_set()[0]
    f = open('data/log/{}.txt'.format(near_time),'r')
    data = eval(f.read())
    f.close()
    return data

def get_qian1():
    hour = get_timemin()[-4]
    f = open('data/time.txt','r')
    data = eval(str(f.readlines()).replace('\\n',''))
    if len(data)!=4:
        return [0,['1','2','设置错误，联系开发者调试','20']]
    starttime = int(data[0])#开始时间
    deadtime = int(data[1])#结束时间
    today1 = int(today())#今天日期
    setnum = int(data[-1])#设定名额
    now_num1 = now_num()#当前名额
    if (starttime > today1) or ((starttime==today1) and (int(hour)<21)):
    	return [4,data,now_num1]
    if setnum > int(now_num1):
        if (today1 < deadtime):
            return [1,data,now_num1]
        elif (today1 == deadtime) and int(hour) < 21:
            return [1,data,now_num1]
        else:
            return [0,[]]
    else:
        return [3,[]]

def wri_ex():
    data = xlrd.open_workbook('data/2.xls', formatting_info=True)
    table = data.sheets()[0]   #通过索引顺序获取
    w=copy(data)
    mydata = get_qinkuang()
    n=3
    for i in mydata:
        w.get_sheet(0).write(n,2,i[0])
        w.get_sheet(0).write(n,3,i[1])
        w.get_sheet(0).write(n,4,i[2])
        n+=1
    filename = read_actname()[-1]
    w.save('book2.xls')
    w.save('data/excels/{}.xls'.format(filename))
    data1 = xlrd.open_workbook('book2.xls')
    table1 = data1.sheets()[0]
    for i in range(0,18):
        pass
        a = table1.row_values(i)
        print(a)
# write_set('20181103','20181104','大爱心','20')
# print(read_set()[0])
# wri_ex()
# print(now_num())
# write_set('10181102','20181103','title','num')
# print(get_qian1())
# baoming('dws0h','151ne4')
# print(get_timemin(),today())