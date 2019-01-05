from flask import Flask,request,jsonify,url_for,render_template
import json,write_data
def check_root():
    payload = {"number":request.json['username'],"passwd":request.json['password']}
    data = str(payload['number'])+':::'+str(payload['passwd'])
    f0 =  open('data/root.txt','r')
    f00 = f0.read()
    f0.close()
    if len(data)>3:
        if data in f00:
            return '<h3>Bad username or password.</h3>'#render_template("set.html")
        else:
            return jsonify({'status':'error'})
    else:
    	return jsonify({'status':'error'})

def qianduan_get():
    
