def write_json():
    f = open('名单.txt','r')
    f_line = f.readlines()
    f.close()
    class_zip = {}
    for i in f_line:
        ban_site = i.find('班')
        ban = i[0:ban_site+1]
        name = i[ban_site+1:].replace('\n','')
        print(name)
        class_zip[name] = '{}'.format(ban)
    f0 = open('ban.json','w')
    f0.write(str(class_zip))
    f0.close()

def read_json():
    f = open('ban.json','r')
    rf = f.read()
    f.close()
    return rf

def set_root():
    f = open('root.txt','w')
    f.write('spxyzqs:::lsl2016')
    f.close()
