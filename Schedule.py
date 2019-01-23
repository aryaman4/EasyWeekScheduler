class Schedule(object):

    def __init__(self, req_obj, in_major, in_taken=['MATH 112'], in_tec=0, min_credits=14, max_credits=16):
        """
        constructor to initialize variables
        :param req_obj: object of Request class
        :param in_major: given major of the user
        :param in_taken: courses user has taken
        :param in_tec: number of technical courses user wants to take
        :param min_credits: minimum number of credits user wants to take as indicated
        :param max_credits: maximum number of credits user wants to take as indicated
        :param in_minor: minor the user wants as indicated
        :param no_min: number of courses from minor user wants to take
        """
        self.days = ['M', 'T', 'W', 'R', 'F']
        self.times = {}
        self.week = {}
        self.req = req_obj
        self.tec_no = in_tec
        self.taken = in_taken
        self.taken.append('MATH 112')
        self.this_term = list()
        self.min_credits = min_credits
        self.max_credits = max_credits
        self.major = in_major
        self.req.set_subject_code(in_major)
        self.crns = {}
        self.geneds = list()
        # self.generate_geneds()

    def build_required(self, file, type):
        """
        builds required courses for a major if data is not previously stored
        :param file: file to store the required courses in
        :param type: type of input required
        """
        self.req.get_courses()
        sc = self.req.subject_code
        for course in self.req.course_list:
            if course[0] == '5':
                break
            x = input(f"Is {sc} {course} a requirement for your {type}")
            if 'y' in x.lower():
                file.write(sc + ' ' + course + '\n')
        course = ""
        while course is not "done":
            course = input("Add other required courses for your major")
            if "done" in course:
                break
            parts = course.split(" ")
            subject_code = parts[0]
            course_num = parts[1]
            file.write(subject_code + ' ' + course_num)
            file.write('\n')

    def build_this_term(self):
        """
        build the courses to be taken for this semester and store them
        """
        try:
            file = open(self.major + ".txt", "r+")
        except FileNotFoundError:
            file = open(self.major + ".txt", "w+")
            self.build_required(file, "major")
        file = open(self.major + ".txt", "r+")

        # getting technical courses
        count = 0
        for line in file:
            if count > int(self.tec_no):
                break
            if line.strip() in self.taken and line.strip() != "MATH 241":
                continue
            satisfied = True
            course = line.split(' ')
            subject = course[0]
            num = course[1]
            self.req.set_subject_code(subject)
            self.req.set_course_num(num)
            pre_reqs = self.req.get_prereq()
            for req in pre_reqs:
                temp = False
                if len(req) == 0:
                    satisfied = True
                    break
                for option in req:
                    if option in self.taken:
                        temp = True
                if not temp:
                    satisfied = False
            if not satisfied:
                continue
            self.this_term.append((subject.strip(), num.strip()))
            print(self.this_term)
            count += 1
        # self.get_geneds()

    def get_geneds(self):
        """
        method to return a list of all possible gen-ed classes for the major
        :return: list of possible courses
        """
        credits_done = 0
        for subject, course in self.this_term:
            self.req.set_subject_code(subject)
            self.req.set_course_num(course)
            credits_done += self.req.get_credit_hours()
        req_max = self.max_credits - credits_done
        req_min = self.min_credits - credits_done
        if req_min <= 0 <= req_max:
            return
        temp = []
        for gened in self.geneds:
            c = gened.strip().split(" ")
            sub = c[0]
            num = c[1]
            self.this_term.append((sub.strip(), num.strip()))
            temp.append(gened)
            self.req.set_subject_code(sub)
            self.req.set_course_num(num)
            cr = self.req.get_credit_hours()
            if req_min <= cr <= req_max:
                break
        for c in temp:
            self.geneds.remove(c)

    def get_open_this_sem(self):
        """
        build a list of CRNs of open sections of courses to be taken this semester
        """
        crns = {}
        for course in self.this_term:
            temp = []
            try:
                subject, num = course
                self.req.set_subject_code(subject)
                self.req.set_course_num(num)
                sections = self.req.get_open_sections()
            except Exception:
                continue
            for section_no, crn in sections:
                temp.append((section_no, crn))
            crns[course] = frozenset(temp)
        self.crns = crns

    def build_times(self):
        """
        method to build schedule from the courses to be taken this semester
        """
        for course in self.this_term:
            if course not in self.crns.keys():
                continue
            subject, code = course
            self.req.set_subject_code(subject)
            self.req.set_course_num(code)
            crn_list = list(self.crns[course])
            section_list = []
            for x, y in crn_list:
                if 'lecture-discussion' in self.req.get_section_type(y).lower().strip():
                    if self.has_time_conflict(y):
                        continue
                    section_list.append((x, y))
                    break
            for x, y in crn_list:
                if 'lecture' in self.req.get_section_type(y).lower().strip():
                    if self.has_time_conflict(y):
                        continue
                    section_list.append((x, y))
                    break
            for x, y in crn_list:
                if 'discussion' in self.req.get_section_type(y).lower().strip():
                    if self.has_time_conflict(y):
                        continue
                    section_list.append((x, y))
                    break
            for x, y in crn_list:
                if 'lab' in self.req.get_section_type(y).lower().strip():
                    if self.has_time_conflict(y):
                        continue
                    section_list.append((x, y))
                    break
            temp_times = []
            for name, crn in section_list:
                temp_times.append((crn, self.req.get_time(crn)))
            self.times[course] = frozenset(temp_times)

    def has_time_conflict(self, crn):
        """
        check if the passed section has a time conflict with any other scheduled class
        :param crn: the CRN number of the section to check
        :return: boolean value indicating whether or not there is a time conflict
        """
        start, end, days = self.req.get_time(crn)
        start = self.get_int_time(start)
        days = [c for c in days]
        time_list = []
        index = 0
        for course, time in self.times.items():
            time_list.append([])
            time = list(time)
            for crn, t in time:
                s, e, d = t
                time_list[index].append(s)
                time_list[index].append(e)
                time_list[index].append(d)
            index+=1
        for i in range(len(time_list)):
            i_start = self.get_int_time(time_list[i][0])
            i_end = self.get_int_time(time_list[i][1])
            i_days = time_list[i][2]
            for day in days:
                if day in i_days:
                    if i_start <= start <= i_end:
                        return True
        return False

    def get_int_time(self, time):
        """
        get time in float format
        :param time: time in hh:mm format
        :return: time in float format
        """
        hour = int(time[0:time.find(":")])
        minutes = int(time[time.find(":") + 1:])
        minutes /= 60
        hour += minutes
        return hour

    def generate_geneds(self):
        college = self.getCollege()
        if college == "eng":
            self.geneds = ["ECON 102", "CLCV 115", ""]
        elif college == "las":
            self.geneds = [""]
        elif college == "gies":
            self.geneds = [""]

    def getCollege(self):
        m = self.major.strip().lower()
        if m == "cs" or m == "ce" or m == "me" or m == "aero" or m == "chemical":
            return "eng"
        else:
            return "las"
