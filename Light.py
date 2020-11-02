from flask import Flask, render_template, request, make_response
import requests
import json

app = Flask(__name__)
app.config.from_object('config')
userName = app.config["PHILLIPS_USERNAME"]
ipaddr = app.config["BRIDGE_IP"]
baseIp = "http://" + ipaddr + "/api/" + userName + "/"


def getBridgeIP():
    """
    Retrieves bridge IP
    ToDo: Figure out a programmatic way to get this, right now
    I'm just hardcoding a value in the config file
    """

    return ipaddr


@app.route('/', methods=['GET'])
def setup():
    """
    Initial setup method. Returns class of data representing
    data for first light in dropdown list. When page loads,
    the sliders are set to the data for the first light in the
    drop down that is displayed.
    """
    lights = []

    r = requests.get(baseIp + "lights")
    content = json.loads(r.content.decode())
    num_of_lights = len(content)
    # our light numbering system starts at 1, so using that instead of 0 for the range
    for light in range(1, num_of_lights + 1):
        if content[str(light)]['state']['on']:
            lights.append(light)
    lights.append("All Lights")
    num = lights[0]  # get the current light that's first in the drop down list
    # Class to send the light data for setting the sliders to the .html
    light_list = LightInfo(num, content[str(num)]['state']['bri'], content[str(num)]['state']['sat'],
                           content[str(num)]['state']['hue'])
    resp = make_response(render_template('simple.html', data=lights, lightInfo=light_list))
    resp.headers.set("Access-Control-Allow-Origin", "*")
    resp.headers.set("Access-Control-Allow-Headers", "*")
    resp.headers.set("Access-Control-Allow-Methods", "*")
    return resp


@app.route('/update', methods=['POST'])
def update():
    """
    Function called when a different light is selected from the dropdown
    and the sliders need to be changed to a different state. Still in progress.
    :return:
    """
    num = request.form['num']

    r = requests.get(baseIp + "lights")
    content = json.loads(r.content.decode())
    light_list = LightInfo(num, content[str(num)]['state']['bri'], content[str(num)]['state']['sat'],
                           content[str(num)]['state']['hue'])

    # TODO: How to actually return updated data


@app.route('/hue', methods=['POST'])
def hue():
    """
    Function called when the hue is changed via the slider.
    Actually calls the API to change light state.
    :return:
    """

    hue_light = request.form['hue']
    lights = request.form['light']
    if lights == "All":
        lights = 0
    payload = {'hue': int(hue_light), 'transitiontime': 0}
    if lights != 0:

        r = requests.put(baseIp + "lights/" + lights + "/state/", data=json.dumps(payload))
    else:

        r = requests.put(baseIp + "groups/0/action", data=json.dumps(payload))

    content = json.loads(r.content.decode())
    # TODO: How to return status of API call
    return str([content])


@app.route('/sat', methods=['POST'])
def sat():
    """
    Function called when the sat is changed via the slider.
    Actually calls the API to change light state.
    :return:
    """

    saturation = request.form['sat']
    lights = request.form['light']

    if lights == "All":
        lights = 0
    payload = {'sat': int(saturation), 'transitiontime': 0}
    if lights != 0:
        r = requests.put(baseIp + "lights/" + lights + "/state/", data=json.dumps(payload))
    else:
        r = requests.put(baseIp + "groups/0/action", data=json.dumps(payload))
    content = json.loads(r.content.decode())
    resp = make_response(json.dumps(content))
    resp.headers.set("Access-Control-Allow-Origin", "*")
    resp.headers.set("Access-Control-Allow-Headers", "*")
    resp.headers.set("Access-Control-Allow-Methods", "*")
    return resp


@app.route('/bri', methods=['POST'])
def bri():
    """
    Function called when the bri is changed via the slider.
    Actually calls the API to change light state.
    :return:
    """

    bright = request.form['bri']
    lights = request.form['light']
    if lights == "All":
        lights = 0
    payload = {'bri': int(bright), 'transitiontime': 0}
    if lights != 0:
        r = requests.put(baseIp + "lights/" + lights + "/state/", data=json.dumps(payload))
    else:
        r = requests.put(baseIp + "groups/0/action", data=json.dumps(payload))
    content = json.loads(r.content.decode())
    resp = make_response(json.dumps(content))
    resp.headers.set("Access-Control-Allow-Origin", "*")
    resp.headers.set("Access-Control-Allow-Headers", "*")
    resp.headers.set("Access-Control-Allow-Methods", "*")
    return resp


@app.route('/off', methods=['POST'])
def off():
    """
    Function called when the the lights are toggled on and off.
    Actually calls the API to change light state.
    :return:
    """

    toggle = request.form['on']
    lights = request.form['light']
    if lights == "All":
        lights = 0
    if toggle == "False":
        payload = {'on': False, 'transitiontime': 0}
    else:
        payload = {'on': True, 'transitiontime': 0}
    if lights != 0:
        r = requests.put(baseIp + "lights/" + lights + "/state/", data=json.dumps(payload))
    else:
        r = requests.put(baseIp + "groups/0/action", data=json.dumps(payload))
    content = json.loads(r.content.decode())
    resp = make_response(json.dumps(content))
    resp.headers.set("Access-Control-Allow-Origin", "*")
    resp.headers.set("Access-Control-Allow-Headers", "*")
    resp.headers.set("Access-Control-Allow-Methods", "*")
    return resp


@app.route('/effect', methods=['POST'])
def effect():
    """
    This function calls the colorloop demo that comes with the Phillips Hue light system.
    :return:
    """

    state = request.form['state']
    lights = request.form['light']
    if lights == "All":
        lights = 0

    if state == "colorloop":
        payload = {'effect': 'colorloop'}
    else:
        payload = {'effect': 'none'}
    if lights != 0:
        r = requests.put(baseIp + "lights/" + lights + "/state/", data=json.dumps(payload))
    else:
        r = requests.put(baseIp + "groups/0/action", data=json.dumps(payload))
    content = json.loads(r.content.decode())
    resp = make_response(json.dumps(content))
    resp.headers.set("Access-Control-Allow-Origin", "*")
    resp.headers.set("Access-Control-Allow-Headers", "*")
    resp.headers.set("Access-Control-Allow-Methods", "*")
    return resp


@app.route('/get', methods=['POST'])
def get_initial_data():
    """
    Function for returning dump of initial data for when page initially loads.
    :return:
    """

    lights = []
    r = requests.get(baseIp + "lights")
    content = json.loads(r.content.decode())
    num_of_lights = len(content)
    for light in range(1, num_of_lights + 1):
        if content[str(light)]['state']['on']:
            lights.append(light)
    resp = make_response(str(content))
    resp.headers.add("Access-Control-Allow-Origin", "*")
    resp.headers.add("Access-Control-Allow-Headers", "*")
    resp.headers.add("Access-Control-Allow-Methods", "*")

    return resp


class LightInfo:
    """
    Class for organizing light data.
    """

    def __init__(self, lightnum, bri, sat, hue):
        self.lightnum = lightnum
        self.bri = bri
        self.sat = sat
        self.hue = hue


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
