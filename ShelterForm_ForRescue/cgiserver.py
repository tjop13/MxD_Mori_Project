#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer,CGIHTTPServer

BaseHTTPServer.HTTPServer(( '', 8000 ), CGIHTTPServer.CGIHTTPRequestHandler ).serve_forever()
