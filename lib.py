import requests as req
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
import time
from bs4 import BeautifulSoup

#image.show()
start = time.clock()
def say_num(url):
    response = req.get('{}'.format(url))
    img = Image.open(BytesIO(response.content))
    #print(img.format,img.size,img.mode)
    img = img.convert('L')
    img.show()
    box1 = (6,16,14,26)
    box2 = (18,16,26,26)
    box3 = (30,16,38,26)
    box4 = (42,16,50,26)
    img1 = img.crop(box1)
    img2 = img.crop(box2)
    img3 = img.crop(box3)
    img4 = img.crop(box4)
    imgs = [img1,img2,img3,img4]
    # img1.show()
    #print(str(num) + '====' + str(img.getpixel((5,3))))
    r_num = 0
    b = 1000
    for i in imgs:
        if i.getpixel((5,5)) is 212:
            if i.getpixel((1,7)) is 212:
                anum = 1
            elif i.getpixel((2,2)) is 2:
                anum = 0
            elif i.getpixel((0,7)) is 2:
                anum = 5
            elif i.getpixel((7,0)) is 2:
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
        r_num = r_num+anum*b
        b = b/10
    a=int(r_num)
    print(a)
say_num('http://210.35.251.243/reader/captcha.php?')
end = time.clock()
print('运行时间为 %s s'%(end-start))
#江财图书馆http://210.35.206.99:8080/reader/login.php
#江西高校http://cbsx.cbelib.jxufe.cn/

# login_url = 'http://210.35.251.243/reader/redr_verify.php'
# bd_session = requests.Session()
# what = bd_session.post(url,headers=headers,data=data)
# #print(type(what.cookies))
# cookii = requests.utils.dict_from_cookiejar(what.cookies)

bk_ls_url = 'http://210.35.251.243/reader/book_lst.php'
headers = {
    'Cookie': 'PHPSESSID=448oe7iebr7i8ot2eupbspr602',
} 
res = req.get(bk_ls_url,headers=headers)
soup = BeautifulSoup(res.text,'lxml')
bk_title = soup.select('a.blue')
my_now_bk = {}
for i in bk_title:
    lib_bk_url = 'http://210.35.251.243/opac/item.php?marc_no='+ i.get('href')[25:]
    book_name = i.get_text()
    print(lib_bk_url,book_name)