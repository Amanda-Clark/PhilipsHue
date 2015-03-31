from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)


def getBridgeIP():
    """
    Retrieves bridge IP

    """
    #Get IP address of bridge. See http://www.developers.meethue.com/documentation/hue-bridge-discovery
    #for more details
    ip = requests.get("https://client-eastwood-dot-hue-prod-us.appspot.com/api/nupnp")
    ipcontent = json.loads(ip.content.decode())
    ipaddr = ipcontent[0]['internalipaddress']
    return ipaddr

@app.route('/', methods = ['GET'])
def setup():
    """
    Initial setup method. Returns class of data representing
    data for first light in dropdown list. When page loads,
    the sliders are set to the data for the first light in the
    drop down that is displayed.
    """
    lights =[]
    ipaddr = getBridgeIP()
    r = requests.get("http://"+ipaddr+"/api/amandapanda/lights")
    content = json.loads(r.content.decode())
    numOfLights = len(content)
    #our light numbering system starts at 1, so using that instead of 0 for the range
    for light in range(1, numOfLights+1):
        if content[str(light)]['state']['on']==True:
            lights.append(light)
    lights.append("All Lights")
    num = lights[0] # get the current light that's first in the drop down list
    #Class to send the light data for setting the sliders to the .html
    lightList = LightInfo(num, content[str(num)]['state']['bri'], content[str(num)]['state']['sat'],
                                   content[str(num)]['state']['hue'])
    return render_template('simple.html', data = lights, lightInfo = lightList)


@app.route('/update', methods = ['POST'])
def update():
    """
    Function called when a different light is selected from the dropdown
    and the sliders need to be changed to a different state. Still in progress.
    :return:
    """
    num = request.form['num']
    ipaddr = getBridgeIP()
    r = requests.get("http://"+ipaddr+"/api/amandapanda/lights")
    content = json.loads(r.content.decode())
    lightList = LightInfo(num, content[str(num)]['state']['bri'], content[str(num)]['state']['sat'],
                                   content[str(num)]['state']['hue'])

    # TODO: How to actually return updated data


@app.route('/hue', methods=['POST'])
def hue():
    """
    Function called when the hue is changed via the slider.
    Actually calls the API to change light state.
    :return:
    """
    ipaddr = getBridgeIP()
    hue=request.form['hue']
    lights = request.form['light']
    if lights == "All":
        lights =0
    payload = {'hue': int(hue), 'transitiontime': 0}
    if lights != 0:

        r = requests.put("http://"+ipaddr+"/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:

        r = requests.put("http://"+ipaddr+"/api/amandapanda/groups/0/action", data = json.dumps(payload))

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
    ipaddr = getBridgeIP()
    sat=request.form['sat']
    lights = request.form['light']

    if lights == "All":
        lights =0
    payload = {'sat': int(sat), 'transitiontime': 0}
    if lights != 0:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)


@app.route('/bri', methods=['POST'])
def bri():
    """
    Function called when the bri is changed via the slider.
    Actually calls the API to change light state.
    :return:
    """
    ipaddr = getBridgeIP()
    bri=request.form['bri']
    lights = request.form['light']
    if lights == "All":
        lights =0
    payload = {'bri': int(bri), 'transitiontime': 0}
    if lights != 0:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)


@app.route('/off', methods=['POST'])
def off():
    """
    Function called when the the lights are toggled on and off.
    Actually calls the API to change light state.
    :return:
    """
    ipaddr = getBridgeIP()
    toggle = request.form['on']
    lights = request.form['light']
    if lights == "All":
        lights =0
    if toggle == "False":
        payload = {'on': False, 'transitiontime': 0}
    else:
        payload = {'on': True, 'transitiontime': 0}
    if lights != 0:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)


@app.route('/effect', methods=['POST'])
def effect():
    """
    This function calls the colorloop demo that comes with the Phillips Hue light system.
    :return:
    """
    ipaddr = getBridgeIP()
    state = request.form['state']
    lights = request.form['light']
    if lights == "All":
        lights =0

    if state == "colorloop":
        payload = {'effect': 'colorloop'}
    else:
        payload = {'effect': 'none'}
    if lights != 0:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/lights/"+lights+"/state/", data = json.dumps(payload))
    else:
        r = requests.put("http://"+ipaddr+"/api/amandapanda/groups/0/action", data = json.dumps(payload))
    content = json.loads(r.content.decode())
    return str(content)


@app.route('/get', methods=['POST'])
def getInitialData():
    """
    Function for returning dump of initial data for when page initially loads.
    :return:
    """
    ipaddr = getBridgeIP()
    lights = []
    r = requests.get("http://"+ipaddr+"/api/amandapanda/lights")
    content = json.loads(r.content.decode())
    numOfLights = len(content)
    for light in range(1, numOfLights+1):
        if content[str(light)]['state']['on'] == True:
            lights.append(light)

    return str(content)


class LightInfo():
    """
    Class for organizing light data.
    """
    def __init__(self, lightnum, bri, sat, hue):
        self.lightnum = lightnum
        self.bri = bri
        self.sat = sat
        self.hue = hue


if __name__ == '__main__':
    app.run()
