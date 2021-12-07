from flask import Blueprint, request, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    
    return render_template("home.html", clientip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr))