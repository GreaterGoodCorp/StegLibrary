from StegLibrary.web import CoreWeb

@CoreWeb.route("/")
@CoreWeb.route("/index")
def index():
    return "Hello, world!"
