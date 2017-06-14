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


def toggle_light(light):
    lights = get_lights()
    if light in lights:
        if lights[light]['state']['on']:
            body = '{"on": false}'
        else:
            body = '{"on": true}'
        light_address = BASE_ADDRESS + '/' + light + '/state'
        requests.put(light_address, data=body)
    else:
        print('Invalid light.')


def toggle_lights():
    lights = get_lights()
    all_off = True
    for light in lights:
        if lights[light]['state']['on']:
            all_off = False

    for light in lights:
        light_address = BASE_ADDRESS + '/' + light + '/state'
        if lights[light]['state']['on']:
            requests.put(light_address, data='{"on": false}')
        elif all_off:
            requests.put(light_address, data='{"on": true}')


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

    # Apply gamma correction
    for i in range(3):
        rgb[i] /= 255
        if rgb[i] > 0.04045:
            rgb[i] = ((rgb[i] + 0.055) / 1.055) ** 2.4
        else:
            rgb[i] /= 12.92

    r, g, b = rgb

    # Convert RGB to XYZ using Wide RGB D65 conversion
    X = r * 0.664511 + g * 0.154324 + b * 0.162028
    Y = r * 0.283881 + g * 0.668433 + b * 0.047685
    Z = r * 0.000088 + g * 0.072310 + b * 0.986039

    # Calcualte xy values
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)

    # Y is the brightness value
    return x, y, int(Y * 254)


def xy_to_rgb(x, y, brightness):
    # xy values to XYZ
    z = 1 - x - y
    Y = brightness
    X = Y / y * x
    Z = Y / y * z

    # Convert to RGB using Wide RGB D65 conversion
    r = X * 1.656492 - Y * 0.354851 - Z * 0.255038
    g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
    b = X * 0.051713 - Y * 0.121364 + Z * 1.011530

    # Apply reverse gamma correction
    rgb = [r, g, b]
    for i in range(3):
        if rgb[i] <= 0.0031308:
            rgb[i] *= 12.92
        else:
            rgb[i] = 1.055 * (rgb[i] ** (1 / 2.4)) - 0.055

    r, g, b = rgb
    return int(r * 255), int(g * 255), int(b * 255)


def update_lights_rgb(lights):
    print(lights)
    for light, val in lights.items():
        r = int(val['r'])
        g = int(val['g'])
        b = int(val['b'])
        bri = int(val['y'])
        x, y, _ = rgb_to_xy(r, g, b)
        xy = '[' + str(x) + ', ' + str(y) + ']'
        light_address = BASE_ADDRESS + '/' + light + '/state'
        body = '{"bri": ' + str(bri) + ', "xy": ' + xy + '}'
        requests.put(light_address, data=body)


"""
Info about all lights:
http://192.168.1.64/api/UF2tbuOItC7lfaTyTaDmUxA6lxSREPuc7brFxQYY/lights

Infor about specific light:
http://192.168.1.64/api/UF2tbuOItC7lfaTyTaDmUxA6lxSREPuc7brFxQYY/lights/1


"""
