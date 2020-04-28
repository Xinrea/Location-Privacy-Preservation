import sys
import os
sys.path.append("..")
from flask import Flask,render_template,request,redirect,json,send_file
from os import path
import hashlib
import MainProcess
import _thread
import time

app = Flask('Feature-base LPP')

@app.route('/',methods=['POST','GET'])
@app.route('/index',methods=['POST','GET'])
def index():
    if (request.method == 'POST'):
        options = request.form.getlist('op')
        f = request.files['file']
        base_path = path.abspath(path.dirname(__file__))
        upload = path.join(base_path,'upload/')
        process = path.join(base_path,'processed/')
        m = hashlib.md5()
        m.update((f.filename+str(time.time())).encode())
        fname = upload + m.hexdigest() + '.txt'
        rname = process + m.hexdigest() + '.txt'
        f.save(fname)
        _thread.start_new_thread(MainProcess.DoProcess,(fname,rname))
        return redirect('/result?id='+m.hexdigest())
    return render_template('index.html')

@app.route('/result')
def result():
    rid = request.args.get('id')
    if (rid == None):
        return redirect('/')
    base_path = path.abspath(path.dirname(__file__))
    process = path.join(base_path,'processed/')
    if (os.path.exists(process+rid+'.txt')):
        return render_template('result.html',id=rid,rfile=rid)
    return render_template('processing.html',id=rid)

@app.route('/download')
def download():
    fid = request.args.get('id')
    if (fid == None):
        return redirect('/')
    base_path = path.abspath(path.dirname(__file__))
    process = path.join(base_path,'processed/')
    if (os.path.exists(process+fid+".txt")):
        return send_file(process+fid+".txt",as_attachment=True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)