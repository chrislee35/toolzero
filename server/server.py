#!/usr/bin/env python
import time, os, json, logging
from uuid import uuid1 as uuid
from mimetypes import guess_type
from threading import Thread
from homebase import BaseTool

from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie as cookie
from urllib.parse import urlparse, parse_qs, urlencode, quote_plus
import urllib3
from websocket_server import WebsocketServer
import ssl

token = uuid().hex
token_cookie = cookie()
token_cookie['token'] = token
token_cookie['token']['httponly'] = True
token_cookie['token']['max-age'] = 7*24*60*60
token_cookie['token']['expires'] = BaseHTTPRequestHandler.date_time_string(time.time()+(7*24*60*60))
token_cookie['token']['secure'] = True

token_cookie_string = token_cookie.output().split(': ',1)[1]
active_apps = {}
active_callbacks = {}

ws_url = 'ws://127.0.0.1:13254'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _check_token_cookie(self):
        cookiestring = "\n".join(self.headers.get_all('Cookie',failobj=[]))
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

    def _set_headers(self, c = None):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        if c:
            cookiestring = c.output().split(': ',1)[1]
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
        path = p.path.replace('..','.')

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
            self._return_json(200, {'appslist': apps_list })
        elif path.startswith('/apps/') and os.path.exists(path[1:]):
            # generate uuid for the app instance
            app_id = uuid().hex
            # load the class for the app
            app_name = path.split('/')[-1]
            klass = self._load_app(app_name)
            if not klass:
                self._return_json(404, {'error': 'App not found'})
                return
            app = klass()
            active_apps[app_id] = app
            # return the interface description to be rendered with the app_instance_id
            self._return_json(200, { 'app_id': app_id, 'fields': app.fields, 'result_type': app.result_type, 'name': app.name })
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
            self._return_json(200, { 'app_id': app_id, 'page': page, 'name': app_name })
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
            self._return_json(200, { 'app_id': app_id, 'page': page, 'name': app_name })
        else:
            self._return_file('html/doesnotexist.html')

    def do_DELETE(self):
        p = urlparse(self.path)
        path = p.path.replace('..','.')
        if not self._check_token_cookie():
            self.send_response(403)
            self.end_headers()
            return

        if path.startswith('/apps/'):
            _,cal,app_id = path.split('/')

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
            self._return_json(200, { 'status': 'success', 'app_id': app_id })
        else:
            self.send_header(404)
            self.end_headers()
            return

    def _load_app(self, app_name):
        name = 'apps.'+  app_name
        mod = __import__(name, fromlist=[''])
        kls = [x for x in dir(mod) if not '_' in x and not x == 'BaseTool']
        for kl in kls:
            print("mod.%s" % kl)
            klass = eval("mod.%s" % kl)
            if issubclass(klass, BaseTool):
                return klass
        return None

    def _list_apps(self):
        apps_list = []
        import glob, os
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
        path = p.path.replace('..','.')
        if not self._check_token_cookie():
            self.send_response(403)
            self.end_headers()
            return

        if path.startswith('/call/'):
            _,cal,app_id,function = path.split('/')

            # check if the app_id exists and is active
            if not active_apps.get(app_id):
                self.send_header(404)
                self.end_headers()
                return

            app = active_apps[app_id]
            # check if the app responds to the function
            if not hasattr(app, function):
                return self._return_json(404, { 'status': 'error', 'error': 'function does not exist' } )

            # serialize the post data as parameters
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            callback_id = uuid().hex
            print(post_body)
            data = json.loads(post_body)

            # allocate a WebSocket and attach a thread with the function

            # respond with the websocket address, the front end with connect to it
            fun = eval('app.%s' % function)
            active_callbacks[callback_id] = { 'fun': fun, 'data': data, 'callback_id': callback_id, 'status': 'pending' }

            self._return_json(200, { 'status': 'success', 'websocket': ws_url, 'callback_id': callback_id })
        elif path == '/proxy':
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            callback_id = uuid().hex
            data = json.loads(post_body)
            print(data)
            active_callbacks[callback_id] = { 'fun': proxy, 'data': data, 'callback_id': callback_id, 'status': 'pending' }
            self._return_json(200, { 'status': 'success', 'websocket': ws_url, 'callback_id': callback_id })
        else:
            self.send_header(404)
            self.end_headers()
            return

def new_client(client, server):
    # determine the callback_id
    print("Accepting new client")

def new_message(client, server, message):
    callback_id = message
    # check the callback_id
    if not active_callbacks.get(callback_id):
        print("unknown callback id")
        client['handler'].send_close(1001)

    print("calling callback")
    # call the callback function, pass in the client and server
    cb = active_callbacks[callback_id]
    cb['server'] = server
    cb['client'] = client
    cb['thread'] = Thread(target=cb_runner, args=(client, server, cb))
    cb['thread'].start()

def cb_runner(client, server, cb):
    cb['status'] = 'running'
    gen = cb['fun'](**cb['data'])
    code = 1000
    for res in gen:
        res_json = json.dumps(res)
        server.send_message(client, res_json)
        if cb['status'] == 'cancelled':
            code = 1001
            break
    active_callbacks.pop(cb['callback_id'])
    cb['status'] = 'finished'
    client['handler'].send_close(code)

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
    content = kwargs.get('content_type','application/json')
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
        body = encoded_data,
        headers = headers
    )
    print(r.data)

    yield { 'status': 'success', 'results': json.loads(r.data.decode('utf-8')) }

server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)#, key="keys/key.pem", cert="keys/cert.pem")
server.set_fn_new_client(new_client)
server.set_fn_message_received(new_message)

httpd = HTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile="keys/key.pem",
        certfile='keys/cert.pem', server_side=True)

print("https://127.0.0.1:4443/?token="+token)
Thread(target=httpd.serve_forever).start()
server.run_forever()
