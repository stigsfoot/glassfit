from os import path
from collections import namedtuple
import jinja2

workouts_base = path.join(path.dirname(__file__), '../', 'templates/workouts/')
image_base = path.join('static', 'images')

jinja = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path.dirname(workouts_base)))

class Exercise(object):
    def __init__(self, name): self.name = name
    def fname(self): return self.name.replace(' ','_').lower()
    def animation_path(self): return path.join(image_base, self.name + '.gif')

def timer_path(duration):
    valid_durations = set([5, 10, 15, 20 ,25])
    if duration not in valid_durations:
        raise ValueError('Invalid duration: {d}'.format(d=duration))
    fname = "%d.gif" % duration 
    return path.join(image_base, fname)

valid_exercises = set()

warmup  = Exercise(name='Warmup')
squats  = Exercise(name='Squats')
pushups = Exercise(name='Pushups')
situps  = Exercise(name='Situps')

WorkoutSet = namedtuple('WorkoutSet', ['reps', 'time', 'exercise'])

class WorkoutTemplate(object):
    def __init__(self, workout_set):
        self.workout_set = workout_set
    def render_template(self):
        template_path = self.workout_set.exercise.fname() + '.json'
        template = jinja.get_template(template_path)
        return template.render({
            'workout_name': self.workout_set.exercise.name,
            'duration': self.workout_set.time,
            'num_reps': self.workout_set.reps,
            'time_path': timer_path(self.workout_set.time),
            'image_path': self.workout_set.exercise.animation_path()
        })

workout = [ 
    WorkoutSet(exercise=warmup, reps=15, time=20),
    WorkoutSet(exercise=squats, reps=10, time=15),
    WorkoutSet(exercise=situps, reps=20, time=5),
    WorkoutSet(exercise=pushups, reps=11, time=10),
]
