import enum


class Day(enum.Enum):
    monday = 'Monday'
    tuesday = 'Tuesday'
    wednesday = 'Wednesday'
    thursday = 'Thursday'
    friday = 'Friday'
    saturday = 'Saturday'
    sunday = 'Sunday'


class TermType(enum.Enum):
    lab = 'Laboratory'
    project = 'Project'
    seminary = 'Seminary'
    exercises = 'Exercises'
