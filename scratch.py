from Schedule import *
from Request import *
req = Request('2019', 'spring')
sched = Schedule(req, 'CS', ['MATH 221', 'MATH 231', 'PHYS 211', 'MATH 241'], 5, 12, 16)
sched.build_this_term()
sched.get_open_this_sem()
sched.times[('CS', '101')] = frozenset([(31018,('12:00', '12:50', 'MW'))])
sched.times[('RHET', '105')] = frozenset([(43441,('09:00', '09:50', 'MWF'))])
sched.build_times()
print(sched.times)
req.set_subject_code('RHET')
req.set_course_num('105')
print(req.get_open_sections())
for section in req.get_open_sections():
    name, crn = section
    print(req.get_time(str(crn)))