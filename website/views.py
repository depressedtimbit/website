from flask import Blueprint, request, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    
    return render_template("home.html", clientip=request.headers.get('X-Forwarded-For', request.remote_addr))