from website import create_app
import getpass
print(getpass.getuser())
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)