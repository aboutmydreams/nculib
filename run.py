#-*- coding: utf-8 -*-
import os,time,datetime,json,requests,base64,nculib
from flask import Flask,redirect,url_for,render_template,request,send_file,send_from_directory
from itsdangerous import JSONWebSignatureSerializer, URLSafeSerializer


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
            return render_template("my.html")



if __name__ == '__main__':
    app.run(debug=True) #host='0.0.0.0', port=80, 
