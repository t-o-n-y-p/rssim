import json
import codecs

with codecs.open('resources.json', 'r', 'utf-8-sig') as resource_file:
    I18N_RESOURCES = json.load(resource_file)
