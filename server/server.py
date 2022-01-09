#!/usr/bin/env python
import time
import os
import json
#import logging
from uuid import uuid1 as uuid
from mimetypes import guess_type
from homebase import BaseTool

from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie as cookie
from urllib.parse import urlparse, parse_qs, urlencode, quote_plus
import urllib3
import ssl

token = uuid().hex
# fixed token for testing
token = "0"
token_cookie = cookie()
token_cookie['token'] = token
token_cookie['token']['httponly'] = True
token_cookie['token']['max-age'] = 7*24*60*60
token_cookie['token']['expires'] = BaseHTTPRequestHandler.date_time_string(time.time()+(7*24*60*60))
token_cookie['token']['secure'] = True

token_cookie_string = token_cookie.output().split(': ', 1)[1]
active_apps = {}
active_callbacks = {}


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _check_token_cookie(self):
        cookiestring = "\n".join(self.headers.get_all('Cookie', failobj=[]))
        c = cookie()
        c.load(cookiestring)
        global token

        for m in c:
            if m == 'token':
                if c[m].value == token:
                    return True
        return False

    def _check_token_query(self, parsed_query):
        global token
        if 'token' in parsed_query:
            ptoken = parsed_query['token'][0]
            if ptoken == token:
                return True
        return False

    def _set_headers(self, c=None):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        if c:
            cookiestring = c.output().split(': ', 1)[1]
            self.send_header('Set-Cookie', cookiestring)
        self.end_headers()

    def _return_file(self, filename):
        if not os.path.exists(filename):
            self.send_response(404)
            self.end_headers()
            return
        content_type = guess_type(filename)[0]
        global token_cookie_string
        self.send_response(200)
        self.send_header('Set-Cookie', token_cookie_string)
        self.send_header('Content-type', content_type)
        buf = open(filename, 'rb').read()
        self.send_header('Content-length', len(buf))
        self.end_headers()
        self.wfile.write(buf)

    def _return_json(self, code, data):
        self.send_response(code)
        self.send_header('Set-Cookie', token_cookie_string)
        self.send_header('Content-type', 'application/json')
        buf = json.dumps(data).encode('UTF-8')
        self.send_header('Content-length', len(buf))
        self.end_headers()
        self.wfile.write(buf)

    def _return_forbidden(self):
        self.send_response(403)
        self.end_headers()

    def do_GET(self):
        p = urlparse(self.path)
        path = p.path.replace('..', '.')

        global active_apps
        if path == '/' or path == '/index.html':
            query = p.query
            parsed_query = parse_qs(query)
            if self._check_token_query(parsed_query):
                self._return_file('html/index.html')
            else:
                self._return_forbidden()
        elif not self._check_token_cookie():
            self._return_forbidden()
        elif os.path.exists("html"+path):
            self._return_file("html"+path)
        elif path == '/listapps':
            apps_list = self._list_apps()
            self._return_json(200, {'appslist': apps_list})
        elif path.startswith('/events/'):
            callback_id = path.split('/')[-1]
            if not active_callbacks.get(callback_id):
                self._return_forbidden()
            else:
                self.send_events(callback_id)
        elif path.startswith('/apps/') and os.path.exists(path[1:]):
            # generate uuid for the app instance
            app_id = uuid().hex
            # load the class for the app
            app_name = path.split('/')[-1]
            klass = self._load_app(app_name)
            if not klass:
                self._return_json(404, {'error': 'App not found'})
                return
            app = klass(self)
            active_apps[app_id] = app
            # return the interface description to be rendered with the app_instance_id
            self._return_json(200, {'app_id': app_id, 'fields': app.fields, 'result_type': app.result_type, 'name': app.name})
        elif path.startswith('/jsapps/'):
            # generate uuid for the app instance
            app_id = uuid().hex
            # load the page for the app
            app_name = path.split('/')[-1]
            page_filename = 'apps/'+app_name+'/index.html'
            if not os.path.exists(page_filename):
                self._return_json(404, {'error': 'App not found'})
                return
            # read the page and replace $app_id
            page = open(page_filename, 'r').read().replace('$app_id', app_id)
            # return the page in the data structure
            self._return_json(200, {'app_id': app_id, 'page': page, 'name': app_name})
        elif path.startswith('/jspyapps/'):
            # generate uuid for the app instance
            app_id = uuid().hex
            # load the page for the app
            app_name = path.split('/')[-1]
            page_filename = 'apps/'+app_name+'/index.html'
            if not os.path.exists(page_filename):
                self._return_json(404, {'error': 'App not found'})
                return
            # read the page and replace $app_id
            page = open(page_filename, 'r').read().replace('$app_id', app_id)
            # now launch the python app
            klass = self._load_app(app_name)
            if not klass:
                self._return_json(404, {'error': 'App not found'})
                return
            app = klass()
            active_apps[app_id] = app

            # return the page in the data structure
            self._return_json(200, {'app_id': app_id, 'page': page, 'name': app_name})
        else:
            self._return_file('html/doesnotexist.html')

    def do_DELETE(self):
        p = urlparse(self.path)
        path = p.path.replace('..', '.')
        if not self._check_token_cookie():
            self.send_response(403)
            self.end_headers()
            return

        if path.startswith('/apps/'):
            _, cal, app_id = path.split('/')

            # check if the app_id exists and is active
            if not active_apps.get(app_id):
                self.send_header(404)
                self.end_headers()
                return

            # check if there are any active callbacks on this application instance
            for callback_id in active_callbacks.keys():
                if active_callbacks[callback_id]['app_id'] == app_id:
                    if active_callbacks[callback_id].get('thread'):
                        cb = active_callbacks[callback_id]
                        # shut down the websocket
                        cb['client']['handler'].send_close(1001)
                        # stop the thread
                        cb['status'] = 'cancelled'
                        # join the thread
                        cb['thread'].join()

                    # remove the callback_id from the active_callbacks
                    active_callbacks.pop(callback_id)

            active_apps.pop(app_id)
            self._return_json(200, {'status': 'success', 'app_id': app_id})
        else:
            self.send_header(404)
            self.end_headers()
            return

    def _load_app(self, app_name):
        name = 'apps.' + app_name
        mod = __import__(name, fromlist=[''])
        kls = [x for x in dir(mod) if '_' not in x and not x == 'BaseTool']
        for kl in kls:
            print("mod.%s" % kl)
            klass = eval("mod.%s" % kl)
            if issubclass(klass, BaseTool):
                return klass
        return None

    def _list_apps(self):
        apps_list = []
        import glob
        import os
        # go through each item in the apps directory
        # TODO: process all configured app directories
        for p in glob.glob('apps/*'):
            # check if the item is a directory
            if not os.path.isdir(p):
                continue
            # check if the
            regfile = p+os.sep+'app.json'
            if not os.path.exists(regfile):
                continue
            try:
                with open(regfile, 'r') as fh:
                    reg = json.load(fh)
                    if not reg.get('type'):
                        print("Cannot autodetect the application type, must be one of js, py, or jspy.")
                        continue
                    if not reg['type'] in ['js', 'py', 'jspy']:
                        print("Unknown application type: %s" % reg['type'])
                        continue
                    reg['path'] = os.path.basename(p)
                    apps_list.append(reg)
            except json.decoder.JSONDecodeError:
                print("Invalid JSON for %s" % regfile)
            except Exception as e:
                print(e)
        return apps_list

    def do_POST(self):
        p = urlparse(self.path)
        path = p.path.replace('..', '.')
        if not self._check_token_cookie():
            self.send_response(403)
            self.end_headers()
            return

        if path.startswith('/call/'):
            _, cal, app_id, function = path.split('/')
            self.call_function(app_id, function)
        elif path == '/proxy':
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            callback_id = uuid().hex
            data = json.loads(post_body)
            active_callbacks[callback_id] = {
                'fun': proxy,
                'data': data,
                'callback_id': callback_id,
                'status': 'pending'
            }
            self._return_json(200, {'status': 'success', 'app_id': '', 'callback_id': callback_id})
        else:
            self.send_header(404)
            self.end_headers()
            return

    def call_function(self, app_id, function):
        # check if the app_id exists and is active
        if not active_apps.get(app_id):
            self.send_response(404)
            self.end_headers()
            return

        app = active_apps[app_id]
        # check if the app responds to the function
        if not hasattr(app, function):
            return self._return_json(404, {'status': 'error', 'error': 'function does not exist'})

        # serialize the post data as parameters
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        callback_id = uuid().hex
        data = json.loads(post_body)

        # respond with the websocket address, the front end with connect to it
        fun = eval('app.%s' % function)
        active_callbacks[callback_id] = {
            'fun': fun,
            'data': data,
            'callback_id': callback_id,
            'status': 'pending'
        }

        self._return_json(200, {
            'status': 'success',
            'app_id': app_id,
            'callback_id': callback_id
        })

    def send_events(self, callback_id):
        self.send_response(200)
        self.send_header('Content-type', 'text/event-stream')
        self.end_headers()
        self.wfile.flush()

        cb = active_callbacks[callback_id]
        cb['status'] = 'running'
        gen = cb['fun'](**cb['data'])
        for res in gen:
            if cb['status'] != 'running':
                break
            buf = ("data: %s\n\n" % json.dumps(res)).encode('UTF-8')
            self.wfile.write(buf)
            self.wfile.flush()
        active_callbacks.pop(cb['callback_id'])
        cb['status'] = 'finished'


def proxy(**kwargs):
    if not kwargs.get('url'):
        return
    url = kwargs['url']
    if kwargs.get('params'):
        url += '?' + urlencode(kwargs['params'])

    method = 'GET'
    if kwargs.get('data'):
        method = 'POST'
    if kwargs.get('method'):
        method = kwargs['method']
    content = kwargs.get('content_type', 'application/json')
    accept = kwargs.get('accept', 'application/json')

    http = urllib3.PoolManager()

    encoded_data = None
    if kwargs.get('data'):
        if kwargs.get('data_type', 'json') == 'json':
            encoded_data = json.dumps(kwargs.get('data')).encode('utf-8')
        elif kwargs['data_type'] == 'raw':
            encoded_data = kwargs['data'].encode('utf-8')
        elif kwargs['data_type'] == 'urlencode':
            encoded_data = quote_plus(kwargs.get('data')).encode('utf-8')

    headers = kwargs.get('headers', {'Content-Type': content, 'Accept': accept})

    r = http.request(
        method,
        kwargs['url'],
        body=encoded_data,
        headers=headers
    )
    print(r.data)

    yield {'status': 'success', 'results': json.loads(r.data.decode('utf-8'))}


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('keys/cert.pem', 'keys/key.pem')
context.verify_mode = ssl.CERT_NONE
httpd = ThreadingServer(('localhost', 4443), SimpleHTTPRequestHandler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True, do_handshake_on_connect=False)

print("https://127.0.0.1:4443/?token="+token)
httpd.serve_forever()
