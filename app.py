from flask import Flask
from os import getenv

app = Flask(__name__)
##app.secret_key = getenv("SECRET_KEY") tällä salataan jossain välissä

import routes