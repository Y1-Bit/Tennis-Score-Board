from wsgiref.simple_server import make_server

from src.tennis_score_board.adapters.presentation.wsgi import application

if __name__ == "__main__":
    port = 8000
    with make_server("", port, application) as httpd:
        print(f"Serving on port {port}...")
        httpd.serve_forever()
