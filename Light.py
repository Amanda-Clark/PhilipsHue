from flask import Flask, render_template, request, make_response
import requests
import json

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def setup():
    lights = []
    r = requests.get("http://10.1.11.222/api/amandapanda/lights")
    content = json.loads(r.content.decode())
    numOfLights = len(content)
    for light in range(1, numOfLights+1):
        if content[str(light)]['state']['on']==True:
            lights.append(light)
    lights.append("All Lights")

    return render_template('simple.html', data = lights)

@app.route('/hue', methods=['POST'])
def hue():
    hue=request.form['hue']
    lights = request.form['light']
    if lights == "All":
        lights =0
    payload = {'hue': int(hue), 'transitiontime': 0}
    if lights != 0:
        r = requests.put("http://10.1.11.222/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://10.1.11.222/api/amandapanda/groups/0/action", data = json.dumps(payload))

    content = json.loads(r.content.decode())

    return str([content])



@app.route('/sat', methods=['POST'])
def sat():
    sat=request.form['sat']
    lights = request.form['light']
    if lights == "All":
        lights =0
    payload = {'sat': int(sat), 'transitiontime': 0}
    if lights != 0:
        r = requests.put("http://10.1.11.222/api/amandapanda/lights/"+light+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://10.1.11.222/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)


@app.route('/bri', methods=['POST'])
def bri():
    bri=request.form['bri']
    lights = request.form['light']
    if lights == "All":
        lights =0
    payload = {'bri': int(bri), 'transitiontime': 0}
    if lights != 0:
        r = requests.put("http://10.1.11.222/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://10.1.11.222/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)


@app.route('/off', methods=['POST'])
def off():
    toggle = request.form['on']
    lights = request.form['light']
    if lights == "All":
        lights =0
    if toggle == "False":
        payload = {'on': False, 'transitiontime': 0}
    else:
        payload = {'on': True, 'transitiontime': 0}
    if lights != 0:
        r = requests.put("http://10.1.11.222/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://10.1.11.222/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)


@app.route('/effect', methods=['POST'])
def effect():
    state = request.form['state']
    lights = request.form['light']
    if lights == "All":
        lights =0

    if state == "colorloop":
        payload = {'effect': 'colorloop'}
    else:
        payload = {'effect': 'none'}
    if lights != 0:
        r = requests.put("http://10.1.11.222/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://10.1.11.222/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)

@app.route('/get', methods=['POST'])
def getInitialData():
    lights = []
    r = requests.get("http://10.1.11.222/api/amandapanda/lights")
    content = json.loads(r.content.decode())
    numOfLights = len(content)
    for light in range(1, numOfLights+1):
        if content[str(light)]['state']['on']==True:
            lights.append(light)

    return str(content)


if __name__ == '__main__':
    app.run()
