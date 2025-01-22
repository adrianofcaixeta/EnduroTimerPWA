from flask import Flask
from flask_assets import Environment, Bundle
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

assets = Environment(app)

css = Bundle('css/style.css', output='gen/packed.css')
js = Bundle('js/app.js', output='gen/packed.js')
assets.register('css_all', css)
assets.register('js_all', js)

from app import routes