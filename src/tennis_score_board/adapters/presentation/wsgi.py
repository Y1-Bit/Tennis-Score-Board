from src.tennis_score_board.factory import create_app

app = create_app()


def application(environ, start_response):
    return app(environ, start_response)
