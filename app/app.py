from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from util.generator import Generator
app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
generator = Generator()
import routes

# heroku start
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')