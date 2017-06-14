import json

import hue

from app import app
from flask import render_template, request
from flask_wtf import FlaskForm


@app.route('/', methods=['GET', 'POST'])
def index():
    lights = hue.get_lights()
    colors = {}
    form = FlaskForm()
    on = False
    count = len(lights)

    for light in lights:
        x = lights[light]['state']['xy'][0]
        y = lights[light]['state']['xy'][1]
        brightness = lights[light]['state']['bri'] / 254
        r, g, b = hue.xy_to_rgb(x, y, brightness)
        colors[light] = {'r': r, 'g': g, 'b': b}
        if lights[light]['state']['on']:
            on = True

    return render_template('index.html',
                           title='Hue Control',
                           lights=lights,
                           colors=colors,
                           form=form,
                           on=on,
                           count=count)


@app.route('/toggle/<light>', methods=['GET', 'POST'])
def toggle(light):
    hue.toggle_light(light)
    return json.dumps({'success': True})


@app.route('/toggle_all', methods=['GET', 'POST'])
def toggle_all():
    hue.toggle_lights()
    return json.dumps({'success': True})


@app.route('/apply_changes', methods=['POST'])
def apply_changes():
    data = request.form
    colors = {}
    for key, val in data.items():
        if key != 'csrf_token':
            light_id = key[1]
            color = key[0]
            if light_id not in colors:
                colors[light_id] = {}
            colors[light_id][color] = val
    hue.update_lights_rgb(colors)
    return json.dumps({'success': True})
