from . import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += (
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    'taggit',
    'modelcluster',
)

MIDDLEWARE += (
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
)

WAGTAIL_SITE_NAME = "WhereHoWhy"
