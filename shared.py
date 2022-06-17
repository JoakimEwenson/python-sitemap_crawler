class UrlObject:
    """ Set up a url object """
    origin: str
    url: str
    status: int

    def __init__(self, origin, url, status):
        self.origin = origin
        self.url = url
        self.status = status

class CrawlerResult:
    origin: str
    ok: int
    broken: list
    redirect: list
    server_err: list
    unknown: list

    def __init__(self, origin:str, ok:int, broken:list, redirect:list, server_err:list, unknown:list):
        self.origin = origin
        self.ok = ok
        self.broken = broken
        self.redirect = redirect
        self.server_err = server_err
        self.unknown = unknown

# Set up user agent
crawler_headers = {
    'User-Agent': '404 crawler by Joakim Ewenson'
}
