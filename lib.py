import requests, re, time
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

start = time.clock()


def say_num(cookie1=None):
    url = 'http://210.35.251.243/reader/captcha.php?'
    bd_session = requests.Session()
    if not cookie1:
        response = bd_session.get(url)
        cookii = requests.utils.dict_from_cookiejar(response.cookies)
    else:
        cookii = cookie1
        headers = {
            'Cookie': cookie1,
            'Referer': 'http://210.35.251.243/reader/book_lst.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }
        response = bd_session.get(url, headers=headers)
    img = Image.open(BytesIO(response.content))
    # print(img.format,img.size,img.mode)
    img = img.convert('L')
    box1 = (6, 16, 14, 26)
    box2 = (18, 16, 26, 26)
    box3 = (30, 16, 38, 26)
    box4 = (42, 16, 50, 26)
    img1 = img.crop(box1)
    img2 = img.crop(box2)
    img3 = img.crop(box3)
    img4 = img.crop(box4)
    imgs = [img1, img2, img3, img4]
    # img1.show()
    r_num = 0
    b = 1000
    for i in imgs:
        if i.getpixel((5, 5)) is 212:
            if i.getpixel((1, 7)) is 212:
                anum = 1
            elif i.getpixel((2, 2)) is 2:
                anum = 0
            elif i.getpixel((0, 7)) is 2:
                anum = 5
            elif i.getpixel((7, 0)) is 2:
                anum = 7
            else:
                anum = 9
        else:
            if i.getpixel((1,7)) is 2:
                if i.getpixel((5,3)) is 2:
                    anum = 8
                else:
                    anum = 6
            elif i.getpixel((0,1)) is 2:
                anum = 3
            elif i.getpixel((1,1)) is 212:
                anum = 4
            else:
                anum = 2
        r_num = r_num + (anum * b)
        b = b/10
    a = int(r_num)
    print(a)
    return a, cookii
# 这是一个识别验证码的函数，返回[验证码，cookie]


def login(user, psd):
    logi = say_num()
    captcha = logi[0]
    coki = 'PHPSESSID={}'.format(logi[1]['PHPSESSID'])
    headers = {
        'Cookie': coki,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    }

    data = {
        'number':'{}'.format(user),
        'passwd':'{}'.format(psd),
        'captcha':captcha,
        'select':'cert_no',
        'returnUrl':'',
    }
    Status = requests.post('http://210.35.251.243/reader/redr_verify.php', headers=headers, data=data).status_code
    print(Status)
    return coki
# 这是一个登入函数，传入学号和密码，返回有效cookie


def get_mynow_bk(cookie):
    bk_ls_url = 'http://210.35.251.243/reader/book_lst.php'
    headers = {
        'Cookie': '{}'.format(cookie),
    } 
    res = requests.get(bk_ls_url, headers=headers)
    my_datas = {}
    bk_data = []
    soup = BeautifulSoup(res.text,'lxml')
    bk_title = soup.select('a.blue')
    last_times = soup.select('font')
    all_td = soup.select('td.whitetext')
    student_name = last_times[0].get_text()
    my_datas['name'] = student_name
    string = str(list(all_td[7::8]))
    find_check = re.findall("getInLib\((.+?)\)", string)
    checks = str(find_check).replace('\'','').split(',')[1::3]

    for i, last_time, tiao_ma_hao, check in zip(bk_title, last_times[1:], all_td[0::8], checks):
        one_bk_data = []
        lib_bk_url = 'http://210.35.251.243/opac/item.php?marc_no='+ i.get('href')[25:]
        book_name = i.get_text()
        last_time = last_time.get_text().strip()
        tiao_ma_hao = tiao_ma_hao.get_text().strip()

        one_bk_data.append(book_name)
        one_bk_data.append(last_time)
        one_bk_data.append(lib_bk_url)
        one_bk_data.append(tiao_ma_hao)
        one_bk_data.append(check)
        bk_data.append(one_bk_data)

    my_datas['books'] = bk_data
    return str(my_datas)
# 这是一个获取当前借阅函数，返回{'name': '我的名字'， 'books': [['第一本书名', '截止时间', '书籍url', '条码号', '续借check号'],/
# ['第2本书名', '截止时间', '书籍url', '条码号', '续借check号'],[...]]}


def xu_jie(cookie, tiao_kuan_ma, check):
    captcha_num = say_num(cookie)[0]
    now_time = int(time.time())
    url = 'http://210.35.251.243/reader/ajax_renew.php?bar_code={}&check={}&captcha={}&time={}'.format(tiao_kuan_ma, check, captcha_num, now_time)
    headers = {
        'Cookie': cookie,
        'Referer': 'http://210.35.251.243/reader/book_lst.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    }
    re_data = requests.get(url, headers=headers)
    if '成功' in re_data.text:
        return 1
    elif '超过最大' in re_data.text:
        return 2
    else:
        return 3
# 传入cookie，条款码，确认码，返回状态码：1（续借成功），2（超过续借量），3（超时或不可续借或其他（错误））


def my_all_bk(cookie):
    url = 'http://210.35.251.243/reader/book_hist.php'
    headers = {
        'Cookie': cookie,
        'Referer': 'http://210.35.251.243/reader/book_hist.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    }
    data = {
        'para_string': 'all'
    }
    res = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(res.text, 'lxml')
    datas = soup.select('td')
    td_list = list(datas)
    bk_name_list = td_list[9::7]
    time1 = td_list[11::7]
    time2 = td_list[12::7]
    all_bk = []
    for name, t1, t2 in zip(bk_name_list, time1, time2):
        a_bk = []
        a_bk.append(name.get_text())
        a_bk.append(t1.get_text())
        a_bk.append(t2.get_text())
        all_bk.append(a_bk)
    return str(all_bk)
# 返回我的历史借阅，格式为[['C语言编程之道', '2018-09-18', '2018-10-09'], ['数学与人类文明', '2018-09-18', '2018-10-09']]


def book_no(seachname, xiaoqu=None):
    if not xiaoqu:
        xiaoqu = 'ALL'
    url0 = 'http://210.35.251.243/opac/openlink.php?dept={}&title={}&doctype=ALL&lang_code=ALL&match_flag=forward&displaypg=100&showmode=list&orderby=DESC&sort=CATA_DATE&onlylendable=no&with_ebook=on'.format(str(xiaoqu),str(seachname))#第一页
    wb_data = requests.get(url0)
    if '本馆没有' in wb_data.text:
        return 0
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('#search_book_list > li > h3')
    kejies = soup.select('#search_book_list > li > p > span')
    booknums = str(soup.select('strong.red')[0])[20:-9]
    n = 1
    bks = {}
    bks['allsum'] = booknums
    for title,kejie in zip(titles,kejies):
        atitle = str(title)
        try:
            titlesspace = list(title.stripped_strings)[2]
        except IndexError:
            titlesspace = ''
        except Exception as e:
            raise
            pass
        data = {
            'titlesname' : list(title.stripped_strings)[1],
            'titlesspace' : titlesspace,
            'titleslink' : 'http://210.35.251.243/opac/item.php?marc_no='+atitle[47:57],
            'kejie' : str(list(kejie.stripped_strings)[1])[-1]+'/'+str(list(kejie.stripped_strings)[0])[-1]

        }
        bks[n] = data
        n += 1
    return bks
# 全部搜索


def book_titles(seachname, xiaoqu=None):
    if not xiaoqu:
        xiaoqu = 'ALL'
    url0 = 'http://210.35.251.243/opac/openlink.php?dept={}&title={}&doctype=ALL&lang_code=ALL&match_flag=forward&displaypg=100&showmode=list&orderby=DESC&sort=CATA_DATE&onlylendable=yes&with_ebook=on'.format(str(xiaoqu),str(seachname))#第一页
    # 表格 快0.3s 但是没有可借数据 url1 = 'http://210.35.251.243/opac/openlink.php?strSearchType=title&match_flag=forward&historyCount=1&strText={}&doctype=ALL&with_ebook=on&displaypg=100&showmode=table&sort=CATA_DATE&orderby=desc&dept=ALL'.format(str(seachname))
    wb_data = requests.get(url0)
    if '本馆没有' in wb_data.text:
        return book_no(seachname,xiaoqu)
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('#search_book_list > li > h3')
    kejies = soup.select('#search_book_list > li > p > span')
    booknums = str(soup.select('strong.red')[0])[20:-9]
    n = 1
    bks = {}
    bks['allsum'] = booknums
    for title,kejie in zip(titles,kejies):
        atitle = str(title)
        try:
            titlesspace = list(title.stripped_strings)[2]
        except IndexError:
            titlesspace = ''
        except Exception as e:
            raise
            pass
        data = {
            'titlesname' : list(title.stripped_strings)[1],
            'titlesspace' : titlesspace,
            'titleslink' : 'http://210.35.251.243/opac/item.php?marc_no='+atitle[47:57],
            'kejie' : str(list(kejie.stripped_strings)[1])[-1]+'/'+str(list(kejie.stripped_strings)[0])[-1]

        }
        bks[n] = data
        n += 1
    return bks
# 只返回可借的，没有可借时才返回不可借的，格式为
# allsum:'149(检索到书的本书)', 1：{'titlesname' :'书名'，'titlesspace' :'索书号（位置）', 'titleslink' :'书籍链接', 'kejie':'可借分书'}}


def lib_bk(num):
    url = 'http://210.35.251.243/opac/item.php?marc_no={}'.format(num)
    res = requests.get(url).text
    soup = BeautifulSoup(res,'lxml')
    datas = soup.select('dl')
    all_data = {}
    for i in datas:
        one_line = i.get_text().split('\n')
        if len(one_line) == 4:
            what_name = one_line[1]
            what_thing = one_line[2]
            all_data['{}'.format(what_name)] = what_thing
    last_data = {}
    bk_name_au = all_data['题名/责任者:'].split('/')
    last_data['name'] = bk_name_au[0]
    last_data['author'] = bk_name_au[1][:-2]
    last_data['isbn'] = re.findall(r'\d+', all_data['ISBN及定价:'].replace('-', ''))[0]
    if '中图法分类号:' not in all_data:
        last_data['place'] = '不明'
    else:
        last_data['place'] = all_data['中图法分类号:']
    if '出版发行项:' not in all_data:
        last_data['pub'] = '不明'
        last_data['year'] = '不明'
    else:
        pub_year = all_data['出版发行项:'].split(',')
        pub = pub_year[0]
        year = pub_year[1]
        last_data['pub'] = pub
        last_data['year'] = year
    if '载体形态项:' not in all_data:
        last_data['pages'] = '不明'
    else:
        ye_site = all_data['载体形态项:'].find('页')
        last_data['pages'] = all_data['载体形态项:'][0:ye_site]
    if '学科主题:' not in all_data:
        last_data['bk_class'] = '不明'
    else:
        last_data['bk_class'] = all_data['学科主题:']
    if '提要文摘附注:' not in all_data:
        last_data['intro'] = '不明'
    else:
        last_data['intro'] = all_data['提要文摘附注:']
    return last_data


# coki = login(5701118133, 100428)
# # my_data = get_mynow_bk(coki)
# # print(my_data)
# print(my_all_bk(coki))
# xu_jie(coki, 'AN1468872', '160E2185')
print(lib_bk('0000777334'))


end = time.clock()
print('运行时间为 %s s' % (end-start))
