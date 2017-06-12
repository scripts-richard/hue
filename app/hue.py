import json
import requests

from secret import IP, USERNAME


BASE_ADDRESS = '/'.join(['http:/', IP, 'api', USERNAME, 'lights'])


def get_lights():
    return json.loads(requests.get(BASE_ADDRESS).content.decode())


def power_on():
    lights = get_lights()
    for light in lights:
        light_address = BASE_ADDRESS + '/' + light + '/state'
        requests.put(light_address, data='{"on": true}')


def power_off():
    lights = get_lights()
    for light in lights:
        light_address = BASE_ADDRESS + '/' + light + '/state'
        requests.put(light_address, data='{"on": false}')


def toggle_lights():
    lights = get_lights()
    for light in lights:
        if lights[light]['state']['on']:
            body = '{"on": false}'
        else:
            body = '{"on": true}'
        light_address = BASE_ADDRESS + '/' + light + '/state'
        requests.put(light_address, data=body)


def button_1():
    # All lights to bright white
    lights = get_lights()
    for light in lights:
        light_address = BASE_ADDRESS + '/' + light + '/state'
        body = '{"on": true, "hue": 33849, "sat": 200, "bri": 254, "ct": 153}'
        requests.put(light_address, data=body)


def button_2():
    # Savannah Sunset
    lights = get_lights()
    states = ['{"on": true, "hue": 1954, "sat": 227, "ct": 153, "bri": 195}',
              '{"on": true, "hue": 8394, "sat": 196, "ct": 500, "bri": 234}',
              '{"on": true, "hue": 18919, "sat": 212, "ct": 372, "bri": 234}']
    for i in range(1, len(lights) + 1):
        light_address = BASE_ADDRESS + '/' + str(i) + '/state'
        requests.put(light_address, data=states[i - 1])


def button_3():
    # Artic Aurora
    lights = get_lights()
    states = ['{"on": true, "hue": 42325, "sat": 252, "ct": 153, "bri": 168}',
              '{"on": true, "hue": 38779, "sat": 253, "ct": 153, "bri": 201}',
              '{"on": true, "hue": 33858, "sat": 254, "ct": 156, "bri": 188}']
    for i in range(1, len(lights) + 1):
        light_address = BASE_ADDRESS + '/' + str(i) + '/state'
        requests.put(light_address, data=states[i - 1])


def rgb_to_xy(r, g, b):
    rgb = [r, g, b]

    for i in range(3):
        rgb[i] /= 255
        if rgb[i] > 0.04045:
            rgb[i] = ((rgb[i] + 0.055) / 1.055) ** 2.4
        else:
            rgb[i] /= 12.92

    r, g, b = rgb

    x = r * 0.664511 + g * 0.154324 + b * 0.162028
    y = r * 0.283881 + g * 0.668433 + b * 0.047685
    z = r * 0.000088 + g * 0.072310 + b * 0.986039

    return x / (x + y + z), y / (x + y + z)


"""
Info about all lights:
http://192.168.1.64/api/UF2tbuOItC7lfaTyTaDmUxA6lxSREPuc7brFxQYY/lights

Infor about specific light:
http://192.168.1.64/api/UF2tbuOItC7lfaTyTaDmUxA6lxSREPuc7brFxQYY/lights/1


"""