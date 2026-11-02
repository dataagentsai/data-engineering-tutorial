"""Page registry: pages register with @page; the parent links make the tree."""
PAGES = {}


def page(pid, title, parent=None, blurb="", short=None):
    def deco(fn):
        PAGES[pid] = dict(id=pid, title=title, parent=parent, blurb=blurb, short=short or title, render=fn,
                          order=len(PAGES))
        return fn
    return deco


def href(pid):
    return f"{pid}.html"


def link(pid, text=None):
    """Link to another tutorial page by id (checked at build time)."""
    return f'<a href="{href(pid)}">{text or PAGES.get(pid, {}).get("short", pid)}</a>'


REPO = "https://github.com/dataagentsai/data-platform-catalog/blob/main/"


def src(path, text=None):
    """Link to a file in the public catalog repository."""
    return f'<a href="{REPO}{path}">{text or path}</a>'
