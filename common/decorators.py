from config import base_settings


def ui_url(_url: str = None):
    def inner(page):
        page.url = f"{base_settings.protocol}://{base_settings.host}/{_url}"
        return page

    return inner
