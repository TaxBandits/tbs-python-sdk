from jinja2 import Environment

from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import messages


def environment(**options):
    env = Environment(**options)

    configs = {
        'static': staticfiles_storage.url,
        'get_messages': messages.get_messages,
    }

    env.globals.update(configs)

    return env