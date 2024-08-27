import os
from urllib.parse import unquote


def static_files_middleware(app, static_dir):
    def serve_static(environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path.startswith("/static/"):
            file_path = unquote(path[8:])
            abs_path = os.path.join(static_dir, file_path)
            if os.path.exists(abs_path) and os.path.isfile(abs_path):
                with open(abs_path, "rb") as file:
                    content = file.read()
                start_response(
                    "200 OK", [("Content-Type", get_content_type(file_path))]
                )
                return [content]
        return app(environ, start_response)

    return serve_static


def get_content_type(file_path):
    ext = os.path.splitext(file_path)[1]
    return {
        ".css": "text/css",
    }.get(ext, "application/octet-stream")
