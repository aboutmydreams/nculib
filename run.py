#-*- coding: utf-8 -*-
import os,time,datetime,json,requests,nculib
from flask import Flask,redirect,url_for,render_template,request,send_file,send_from_directory
import base64

app = Flask(__name__)
@app.route('/', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    bookname = request.form['username']
    return nculib.get_book(bookname)

@app.route("/<bookname>", methods=['GET'])
def download_file(bookname):
    bk_data = nculib.get_book(bookname)
    return bk_data

if __name__ == '__main__':
    app.run(debug=True) #host='0.0.0.0', port=80, 