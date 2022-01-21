import sys
sys.path.insert(0, '/var/www/html/website')
activate_this = '/home/ubuntu/website/virt/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from main import app as application