#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Nick Ferguson'
SITENAME = 'piggah.xyz'
SITEURL = 'https://piggah.xyz'

PATH = 'content'
ARTICLE_PATHS = ['blog']
PAGE_PATHS = ['pages']
PATH_METADATA = '(?P<path_no_ext>.*)\..*'
ARTICLE_URL = ARTICLE_SAVE_AS = PAGE_URL = PAGE_SAVE_AS = '{path_no_ext}.html'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('eBook Server', 'https://books.piggah.xyz'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/NickCrew'),
          ('YouTube','https://www.youtube.com/channel/UC972wwbPrKXW-YlXCPGPbQw'),
          ('Twitter', 'https://twitter.com/piggahmonster'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
