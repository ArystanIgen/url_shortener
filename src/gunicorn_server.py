import multiprocessing  # pragma: no cover
from gunicorn.app.wsgiapp import WSGIApplication  # pragma: no cover


class StandaloneApplication(WSGIApplication):  # pragma: no cover
    def __init__(self, app_uri, options=None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):  # pragma: no cover
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


if __name__ == '__main__':  # pragma: no cover
    options = {
        "bind": "0.0.0.0:8000",
        "workers": multiprocessing.cpu_count() // 2,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "max_requests": 20,
        "max_requests_jitter": 10
    }

    StandaloneApplication("app.main:main_app", options).run()
