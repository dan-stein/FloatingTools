
__all__ = [
    'SiteUtils'
]

# register this path
import site
import os
site.addsitedir(os.path.dirname(__file__))

# package imports
import wordpress_xmlrpc as SiteUtils
