# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from nib import Processor, markup
from MarkdownPP import MarkdownPP
from MarkdownPP import modules as Modules

@markup(['.md', '.mkdn'])
class MarkdownPP_Processor(Processor):
    def __init__(self, options):
        self.options = options
        config = {
            'markdown.extensions.footnotes': {
                'UNIQUE_IDS': True,
            },
        }
        self.markdown = markdown.Markdown(output_format='html5',
                                          extensions=config.keys(),
                                          extension_configs=config,
                                          )

    def document(self, document):
        document.short = self.markdown.reset().convert(document.short)
        document.content = self.markdown.reset().convert(document.content)
        document.extension = '.html'
        return document
