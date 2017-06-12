import hue

from app import app
from flask import render_template


@app.route('/')
def index():
    lights = hue.get_lights()
    return render_template('index.html',
                           title='Hue Control',
                           lights=lights)
