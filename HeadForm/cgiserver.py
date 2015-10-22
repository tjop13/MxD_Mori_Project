#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer,CGIHTTPServer

CGIHTTPServer.CGIHTTPRequestHandler.cgi_directories=['/cgi-bin','/cgi-bin/img']
BaseHTTPServer.HTTPServer(( '', 8080 ), CGIHTTPServer.CGIHTTPRequestHandler ).serve_forever()
