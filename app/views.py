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

    for light in lights:
        x = lights[light]['state']['xy'][0]
        y = lights[light]['state']['xy'][1]
        brightness = lights[light]['state']['bri'] / 254
        r, g, b = hue.xy_to_rgb(x, y, brightness)
        colors[light] = {'r': r, 'g': g, 'b': b}
        if lights[light]['state']['on']:
            on = True

    if form.validate_on_submit():
        print(request.args.get())

    return render_template('index.html',
                           title='Hue Control',
                           lights=lights,
                           colors=colors,
                           form=form,
                           on=on)


@app.route('/toggle/<light>', methods=['GET', 'POST'])
def toggle(light):
    hue.toggle_light(light)
    return json.dumps({'success': True})
