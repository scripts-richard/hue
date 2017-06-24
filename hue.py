import json
import requests

from secret import USERNAME


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


class Hue:
    def __init__(self):
        self.ip = self.get_hue_ip()
        self.base_address = self.make_base_address()
        self.lights = self.get_lights()

    def get_hue_ip(self):
        url = 'https://www.meethue.com/api/nupnp'
        data = json.loads(requests.get(url).content.decode())
        return data[0]['internalipaddress']

    def make_base_address(self):
        return '/'.join(['http:/', self.ip, 'api', USERNAME, 'lights'])

    def get_lights(self):
        return json.loads(requests.get(self.base_address).content.decode())

    def power_on(self):
        for light in self.lights:
            light_address = self.base_address + '/' + light + '/state'
            requests.put(light_address, data='{"on": true}')

    def power_off(self):
        for light in self.lights:
            light_address = self.base_address + '/' + light + '/state'
            requests.put(light_address, data='{"on":false}')

    def toggle_light(self, light):
        if light in self.lights:
            if self.lights[light]['state']['on']:
                body = '{"on": false}'
            else:
                body = '{"on": true}'

            light_address = self.base_address + '/' + light + '/state'
            requests.put(light_address, data=body)
        else:
            print('Invalid light.')

    def toggle_lights(self):
        all_off = True
        for light in self.lights:
            if self.lights[light]['state']['on']:
                all_off = False

        if all_off:
            self.power_on()
        else:
            self.power_off()

    def update_via_rgb(self, lights):
        for light in lights:
            for light, val in lights.items():
                r = int(val['r'])
                g = int(val['g'])
                b = int(val['b'])
                bri = val['y']

                x, y, _ = rgb_to_xy(r, g, b)
                xy = '[' + str(x) + ', ' + str(y) + ']'

                light_address = self.base_address + '/' + light + '/state'
                body = '{"bri": ' + bri + ', "xy": ' + xy + '}'
                requests.put(light_address, data=body)
