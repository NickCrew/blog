#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Nick Ferguson'
AUTHOR_URL = 'author/nick-ferguson.html'

SITENAME = 'devbear.net'
SITEURL = 'http://blog.devbear.net'
SITESUBTITLE = 'Software Development for Bears'

TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

THEME = "pelican-themes/nice-blog"
# Theme-specific props
SIDEBAR_DISPLAY = ['about', 'tags', 'categories']
COPYRIGHT = 'Copyright 2020 Nick Ferguson'
SIDEBAR_ABOUT = "Build and Release Platform Developer located in Clearwater, FL. Special focus on Linux & Containerized Apps, .NET Core, PowerShell, Build & Automation."


SLUGIFY_SOURCE = 'title'

DELETE_OUTPUT_DIRECTORY = True

PATH = 'content'
PATH_METADATA = '(?P<path_no_ext>.*)\..*'

DEFAULT_ORPHANS = 0
SUMMARY_MAX_LENGTH = 65


PAGE_PATHS = ['pages']
PAGE_EXCLUDES = ['blog']
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'

ARTICLE_PATHS = ['blog']
ARTICLE_EXCLUDES = ['pages']
ARTICLE_SAVE_AS = 'blog/{slug}/index.html'
ARTICLE_URL = 'blog/{slug}/'
ARTICLE_ORDER_BY = 'date'

#DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'archives']
#PAGINATED_TEMPLATES = {'index': 6, 'tag': None, 'category': None, 'archives': 9}
#BLOG_INDEX_SAVE_AS = 'blog/index.html'

CATEGORY_URL = 'category/{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}.html'
DEFAULT_CATEGORY = 'News'

TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = 'tag/{slug}.html'

STATIC_PATHS = ['images', 'docbooks']

YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%b}/index.html'
ARCHIVES_SAVE_AS = 'blog/index.html'

NEWEST_FIRST_ARCHIVES = True

DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'
WITH_FUTURE_DATES = True

LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True

FORMATTED_FIELDS = ['summary','title']

# Feed generation is usually not desired when developing
FEED_ALL_RSS = 'blog/feeds/all.rss.xml'
FEED_ALL_ATOM = 'blog/feeds/all.atom.xml'
FEED_MAX_ITEMS = 15
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Social widget
SOCIAL = (('Github', 'https://github.com/NickCrew'),
          ('YouTube','https://www.youtube.com/channel/UC972wwbPrKXW-YlXCPGPbQw'),
          ('Twitter', 'https://twitter.com/piggahmonster'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = True
#USE_FOLDER_AS_CATEGORY = True

MENUITEMS = [
    ('Archives', 'blog'),
]


