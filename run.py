#-*- coding: utf-8 -*-
import os,time,datetime,json,requests,base64,nculib,sys,random
from flask import Flask,redirect,url_for,render_template,request,send_file,send_from_directory
import numpy as np
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from array import array
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")
# from itsdangerous import JSONWebSignatureSerializer
# import pymysql.cursors

import tfmain,crawler


app = Flask(__name__)
@app.route('/', methods=['GET'])
def signin_form():
    return render_template("find.html")

@app.route('/find', methods=['POST'])
def signin():
    bookname = request.form['bookname']
    return nculib.get_book(bookname)

@app.route("/<bookname>", methods=['GET'])
def download_file(bookname):
    bk_data = nculib.get_book(bookname)
    return bk_data

@app.route('/break', methods=['GET'])
def break_img():
    return str(tfmain.break_imgs())

@app.route('/liblogin', methods=['POST'])
def liblogin():
    username = request.form['username']
    password = request.form['password']
    # res = crawler.ImgVerifier(str(username),str(password))
    # res.getLoginData()
    res = crawler.lib_login(username, password)
    return str(res)

'''
@app.route('/login', methods=['POST','GET'])
def my_page():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        user = request.form['username']
        psd = request.form['password']
        coki = nculib.login(user, psd)
        if nculib.my_rank(coki) == 'error':
            return 'error'
        else:
            s = JSONWebSignatureSerializer('spxyzqs')
            token = s.dumps({user: psd})
            connection = pymysql.connect(host = 'localhost',user = 'root',password = '123456',db = 'usertoken',charset = 'utf8mb4')
            connection.cursor()

            return render_template("my.html")
'''

print('begin')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=1026) #host='0.0.0.0', port=80, 
