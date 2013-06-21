from os import path
import json
from collections import namedtuple
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

class WorkoutSet(namedtuple('WorkoutSet', ['reps', 'time', 'exercise'])):
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

class WorkoutTemplate(object):
    def __init__(self, workout_set):
        self.workout_set = workout_set

    def render_template(self):
        template = jinja.get_template('workout.json')
        return json.loads(template.render({
            'workout_name': self.workout_set.exercise.name,
            'duration': self.workout_set.time,
            'num_reps': self.workout_set.reps,
            'time_path': timer_path(self.workout_set.time),
            'image_path': self.workout_set.exercise.animation_path(),
            'background_path': random.choice(backgrounds)
        }))

# The sample workout we use for now
workout = [ 
    WorkoutSet(exercise=warmup, reps=15, time=20),
    WorkoutSet(exercise=squats, reps=10, time=15),
    WorkoutSet(exercise=situps, reps=20, time=5),
    WorkoutSet(exercise=pushups, reps=11, time=10),
]
