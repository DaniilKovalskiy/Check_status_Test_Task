import http.server
import socketserver
from jinja2 import Environment, FileSystemLoader

from check_status_func import check_status
from lists_for_test import new_list, old_list

env = Environment(loader=FileSystemLoader(''))
template = env.get_template('template.html')


def generate_report(old_list, new_list):
    all_objects, added_objects, deleted_objects, modified_objects = check_status(
        old_list, new_list)

    rendered_template = template.render(
        all_objects=all_objects,
        added_objects=added_objects,
        deleted_objects=deleted_objects,
        modified_objects=modified_objects,
    )

    return rendered_template


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(generate_report(
                old_list, new_list).encode('utf-8'))
        else:
            super().do_GET()


PORT = 8000
Handler = CustomHandler
Handler.extensions_map.update({
    '.html': 'text/html',
})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Сервер запущен на порту", PORT)
    httpd.serve_forever()
