import http.server
import socketserver
import argparse
from pathlib import Path


def serve(directory: str = 'docs', port: int = 8000, host: str = '0.0.0.0'):
    import os
    path = Path(directory).resolve()
    # Change to the directory to serve it properly
    os.chdir(path)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((host, port), handler)

    print(f'Serving {path} at http://{host}:{port}/ (Ctrl+C to stop)')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serve the docs directory over HTTP.')
    parser.add_argument('--dir', default='docs', help='Directory to serve')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    args = parser.parse_args()
    serve(args.dir, args.port, args.host)
