from wsgiref.simple_server import make_server

from app.wsgi import application

if __name__ == "__main__":
    port = 8000
    with make_server("", port, application) as httpd:
        print(f"Serving on port {port}...")
        httpd.serve_forever()
