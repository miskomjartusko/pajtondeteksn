from flask import Flask,render_template,request,redirect
import requests
import json
from datetime import datetime

app = Flask(__name__)
 
@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        name = request.form['first_name']
        photo_url = request.form['last_name']
        requests.post('https://rasp-users.onrender.com/api/users', json={'name': name, 'photo_url': photo_url})
        return redirect('/')
 
 
@app.route('/')
def dashboard():
    req = requests.get('https://rasp-users.onrender.com/api/users')
    x = json.loads(req.content)

    return render_template('datalist.html', people=x)

@app.route('/logs')
def logs():
    req = requests.get('https://rasp-users.onrender.com/api/logs')
    x = json.loads(req.content)
    return render_template('logs.html', logs=x)

@app.route('/<int:id>')
def personinfo(id):
    person = requests.get(f'https://rasp-users.onrender.com/api/user/{id}')
    photos = json.loads(person.content)
    photos = photos['photo_url'].split('/*/')
    if person:
        return render_template('data.html', person = json.loads(person.content), photos=photos)
    return f"Employee with id ={id} Doenst exist"
 
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    if request.method == 'POST':
        requests.delete(f'https://rasp-users.onrender.com/api/user/{id}')
        return redirect('/')  
    return render_template('delete.html')