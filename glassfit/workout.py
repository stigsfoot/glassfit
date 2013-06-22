from os import path
import json
import logging
import jinja2
import random

workouts_base = path.join(path.dirname(__file__), '../', 'templates/workouts/')

def imgur(k): return 'http://imgur.com/%s' % k

image_maps = {
    5         : imgur('12345.gif'),
    10        : imgur('asdfg.gif'),
    15        : imgur('zxcvb.gif'),
    20        : imgur('asdf.gif'),
    'Warmup'  : imgur('blah'),
    'Squats'  : imgur('blah'),
    'Pushups' : imgur('blah'),
    'Situps'  : imgur('blah'),
}

backgrounds = [imgur('bg1'), imgur('bg2'), imgur('bg3')]

jinja = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path.dirname(workouts_base)))

class Exercise(object):
    def __init__(self, name): self.name = name
    def animation_path(self): return image_maps[self.name]

def timer_path(duration): return image_maps[duration]

warmup  = Exercise(name='Warmup')
squats  = Exercise(name='Squats')
pushups = Exercise(name='Pushups')
situps  = Exercise(name='Situps')

class WorkoutSet(object):
    def __init__(self, reps, time, exercise):
        self.reps = reps
        self.time = time
        self.exercise = exercise

    @classmethod
    def of_json(cls, js):
        d = json.loads(js)
        return cls(reps=d['reps'],time=d['time'],
                exercise=Exercise(d['exercise']))
    def to_json(self):
        return json.dumps({
            'reps': self.reps,
            'time': self.time,
            'exercise': self.exercise.name
        })
    def template_vars(self):
        return {
                'workout_name': self.exercise.name,
                'duration': self.time,
                'num_reps': self.reps,
                'time_path': timer_path(self.time),
                'image_path': self.exercise.animation_path(),
                'background_path': random.choice(backgrounds)
                }
    @property
    def template_name(self): return 'workout.json'

class SimpleCard(object):
    def __init__(self, time, template_name):
        self.time = time
        self.template_name = template_name

    @classmethod
    def of_json(cls, js):
        d = json.loads(js)
        return cls(d['time'], d['template_name'])
    def to_json(self):
        return json.dumps({
            'template_name': self.template_name,
            'time': self.time
        })
    def template_vars(self): return {}


# TODO hacky. will fix later
def card_factory(js):
    js = json.loads(js)
    if 'exercise' in js: return WorkoutSet
    else: return SimpleCard

class WorkoutTemplate(object):
    def __init__(self, card): self.card = card

    def render_template(self):
        template = jinja.get_template(self.card.template_name)
        return json.loads(template.render(self.card.template_vars()))

TYPES = {
    'Exercise': Exercise,
    'SimpleCard': SimpleCard,
    'WorkoutSet': WorkoutSet,
}

class CustomTypeEncoder(json.JSONEncoder):
    """A custom JSONEncoder class that knows how to encode core custom
    objects.

    Custom objects are encoded as JSON object literals (ie, dicts) with
    one key, '__TypeName__' where 'TypeName' is the actual name of the
    type to which the object belongs.  That single key maps to another
    object literal which is just the __dict__ of the object encoded."""

    def default(self, obj):
        for cls in TYPES.values():
            if isinstance(obj, cls):
                key = '__%s__' % obj.__class__.__name__
                return { key: obj.__dict__ }
        logging.warn("Don't know how to encode %s", str(obj))
        return json.JSONEncoder.default(self, obj)


class CustomTypeDecoder(json.JSONDecoder):
    def default(self, dct):
        if len(dct) == 1:
            type_name, value = dct.items()[0]
            type_name = type_name.strip('_')
            if type_name in TYPES:
                return TYPES[type_name].from_dict(value)
        return dct

# The sample workout we use for now
workout = [ 
    WorkoutSet(exercise=warmup, reps=15, time=20),
    WorkoutSet(exercise=squats, reps=10, time=15),
    WorkoutSet(exercise=situps, reps=20, time=5),
    WorkoutSet(exercise=pushups, reps=11, time=10),
    SimpleCard(template_name='finish.json', time=0)
]
