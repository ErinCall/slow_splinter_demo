from __future__ import unicode_literals

from flask import Flask, render_template

app = Flask('slow_splinter_demo')


@app.route('/')
def index():
    return render_template('index.html')
