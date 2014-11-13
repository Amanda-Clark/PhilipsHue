from flask import Flask, render_template, request, make_response
import requests
import json

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def setup():
    return render_template('simple.html')

@app.route('/hue', methods=['POST'])
def hue():
    hue=request.form['hue']
    payload = {'hue': int(hue), 'transitiontime': 0}
    r = requests.put("http://10.1.11.222/api/amandapanda/lights/3/state/", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    print(content)
    return content

@app.route('/sat', methods=['POST'])
def sat():
    sat=request.form['sat']
    payload = {'sat': int(sat), 'transitiontime': 0}
    r = requests.put("http://10.1.11.222/api/amandapanda/lights/3/state/", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    print(content)

@app.route('/bri', methods=['POST'])
def bri():
    bri=request.form['bri']
    payload = {'bri': int(bri), 'transitiontime': 0}
    r = requests.put("http://10.1.11.222/api/amandapanda/lights/3/state/", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    print(content)

@app.route('/off', methods=['POST'])
def off():
    toggle = request.form['on']
    if toggle == "False":
        payload = {'on': False}
    else:
        payload = {'on': True}
    r = requests.put("http://10.1.11.222/api/amandapanda/lights/3/state/", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    print(content, off)



if __name__ == '__main__':
    app.run()
