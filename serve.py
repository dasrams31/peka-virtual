#!/usr/bin/env python3
"""Static server for the Peka Virtual Office (virtual.peka.ai.id).

Serves the single-page site with gzip compression for text assets and
long-lived caching for heavy static files (the Three.js module and the
mascot image), while the HTML page itself always revalidates so updates
go live immediately.
"""
import gzip
import http.server
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8093

GZIP_EXTS = {".html", ".js", ".css", ".xml", ".txt", ".json", ".svg"}
LONG_CACHE_EXTS = {".js", ".png", ".jpg", ".jpeg", ".webp", ".ico"}
_cache = {}


def gzipped(path):
    """Return gzip-compressed bytes for path, cached by (path, mtime)."""
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return None
    key = (path, mtime)
    if key not in _cache:
        try:
            with open(path, "rb") as fh:
                _cache[key] = gzip.compress(fh.read(), compresslevel=6)
        except OSError:
            return None
        if len(_cache) > 8:
            _cache.pop(next(iter(_cache)))
    return _cache[key]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        ext = os.path.splitext(self.path.split("?")[0])[1].lower()
        if ext in LONG_CACHE_EXTS:
            self.send_header("Cache-Control", "public, max-age=604800")
        else:
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            for index in ("index.html", "index.htm"):
                candidate = os.path.join(path, index)
                if os.path.isfile(candidate):
                    path = candidate
                    break
        ext = os.path.splitext(path)[1].lower()
        if (
            ext in GZIP_EXTS
            and os.path.isfile(path)
            and "gzip" in self.headers.get("Accept-Encoding", "")
        ):
            data = gzipped(path)
            if data is not None:
                self.send_response(200)
                self.send_header("Content-Type", self.guess_type(path))
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self._gzip_body = data
                return _Body(self._gzip_body)
        return super().send_head()

    def copyfile(self, source, outputfile):
        if getattr(self, "_gzip_body", None) is not None:
            outputfile.write(self._gzip_body)
            self._gzip_body = None
            return
        super().copyfile(source, outputfile)

    def log_message(self, fmt, *args):
        pass


class _Body:
    """Minimal file-like wrapper so send_head can short-circuit."""

    def __init__(self, data):
        self._data = data

    def read(self, size=-1):
        data, self._data = self._data, b""
        return data

    def close(self):
        pass


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    server.serve_forever()
