# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from os import path

from nib import Resource, Processor, after

apache_redirects = b"""
RewriteCond %{DOCUMENT_ROOT}/$1/index.html -f
RewriteRule ^(.*)$ /$1/index.html [L]

RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.*)$ /$1.html [L]

RewriteCond %{DOCUMENT_ROOT}/$1/index.html -f
RewriteRule ^(.*)/$ /$1 [L,R]

RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.*)/$ /$1 [L,R]
"""

apache_redirects_base = b"""
RewriteEngine on
RewriteBase /
"""

nginx_rules = b"""
location / {
    #root {0};
    index index.html;
    try_files $uri $uri.html $uri/index.html;
}
"""


@after
class PrettyURLProcessor(Processor):
    def process(self, documents, resources):
        for document in documents:
            filename = path.basename(document.uri)
            if filename == 'index.html':
                document.uri = path.dirname(document.path)
            elif document.extension == '.html':
                document.uri = document.path

        htaccess = None
        for resource in resources:
            if resource.path == '.htaccess':
                htaccess = resource

        if not htaccess:
            htaccess = Resource(path='.htaccess',
                                content=apache_redirects_base)
            resources.append(htaccess)

        htaccess.content += apache_redirects

        nginx = Resource(path='.nginx',
                         content=nginx_rules)
        resources.append(nginx)

        return documents, resources
