import json
from glassfit.workout import jinja

def start_page_card():
    template = jinja.get_template('welcome.json')
    return json.loads(template.render({}))

