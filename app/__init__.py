from flask import Flask

webapp = Flask(__name__)

from app import registration
from app import login
from app import mainpage
from app import play_video
from app import homepage
from app import search
from app import userpage
from app import collection

