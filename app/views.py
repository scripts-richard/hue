import hue

from app import app
from flask import render_template


@app.route('/')
def index():
    lights = hue.get_lights()
    colors = {}

    for light in lights:
        x = lights[light]['state']['xy'][0]
        y = lights[light]['state']['xy'][1]
        brightness = lights[light]['state']['bri'] / 254
        r, g, b = hue.xy_to_rgb(x, y, brightness)
        colors[light] = {'r': r, 'g': g, 'b': b}

    return render_template('index.html',
                           title='Hue Control',
                           lights=lights,
                           colors=colors)
