from uiucapi.query import *
from requests_xml import XMLSession
from URLBuilder import *

session = XMLSession()


class Request(object):

    def __init__(self, in_year, in_semester):
        self.subjects = list()
        self.course_list = list()
        self.year = in_year
        self.semester = in_semester
        self.subject_code = ""
        self.course_num = ""
        self.u = URLBuilder(self.year, self.semester)

    def set_subject_code(self, in_subject):
        """
        method to set subject code
        :param in_subject: input subject
        """
        self.subject_code = in_subject
        self.u.set_subject_code(self.subject_code)

    def set_course_num(self, in_course_num):
        """
        method to set particular course
        :param in_course_num: input course number
        """
        self.course_num = in_course_num
        self.u.set_course_num(self.course_num)

    def build_course_str(self):
        course_str = self.subject_code + ' ' + self.course_num + ' '
        if self.semester == 'fall':
            course_str += 'FA'
        elif self.semester == 'spring':
            course_str += 'SP'
        course_str += self.year[2:]
        return course_str

    def get_subjects(self):
        """
        method to build a list of all subjects
        """
        for i in range(1, 200):
            s = '//subject[%s]/@id' % (str(i))
            r = session.get(self.u.get_url())
            item = r.xml.xpath(s, first=True)
            if item is None:
                break
            self.subjects.append(item)

    def get_courses(self):
        """
        method to set all courses
        """
        r = session.get(self.u.get_url())
        for i in range(1, 200):
            xp = '//course[%s]/@id' % (str(i))
            l = r.xml.xpath(xp, first=True)
            if l is None:
                break
            self.course_list.append(l)

    def course_description(self):
        """
        method to get course description
        :return: description of the course
        """
        r = session.get(self.u.get_url())
        desc = r.xml.xpath("//description/text()", first=True)
        return desc

    def get_prereq(self):
        """
        get all prerequisites for a given course
        :return: prerequisites of the given course
        """
        s = self.course_description()
        temp = "Prerequisite:"
        index = s.find(temp)
        s = s[index: len(s)]
        s = s[len(temp):]
        parts = s.split(";")
        parts = [part.strip() for part in parts]
        pre_reqs = [list() for _ in parts]
        for j in range(len(parts)):
            s = parts[j]
            i = len(s) - 1
            while i >= 0:
                if s[i].isdigit() or s[i] == " " or s[i].isupper():
                    end = i + 1
                    while i >= 0 and (s[i].isdigit() or s[i] == " " or s[i].isupper()):
                        i -= 1
                    i += 1
                    pre_reqs[j].append(s[i:end])
                i -= 1
        for i in range(len(pre_reqs)):
            temp = []
            for option in pre_reqs[i]:
                option = option.strip()
                if len(option) > 1:
                    temp.append(option)
            pre_reqs[i] = temp
        return pre_reqs

    def get_open_sections(self):
        """
        get a list of all open sections for the course
        :return: a list of all open sections for the course
        """
        course_str = self.build_course_str()
        course = get_course(course_str)
        open_sections = []
        lec_r = False
        labs_r = False
        disc_r = False

        if ('Lecture' or 'Lecture-Discussion') in self.get_types():
            lec_r = True
        if ('Discussion' or 'Lecture-Discussion' or 'Discussion/Recitation') in self.get_types():
            disc_r = True
        if ('Laboratory' or 'Laboratory-Discussion') in self.get_types():
            labs_r = True

        for section in course.sections:

            if "open" in section.registration_status.lower():
                open_sections.append(tuple((section.section_number, section.crn)))
        lec_open = False
        disc_open = False
        labs_open = False
        for sec in open_sections:
            x, y = sec
            if 'lecture' in self.get_section_type(y).lower() or not lec_r:
                lec_open = True
            if 'discussion' in self.get_section_type(y).lower() or not disc_r:
                disc_open = True
            if 'lab' in self.get_section_type(y).lower() or not labs_r:
                labs_open = True
        if lec_open and disc_open and labs_open:
            return open_sections
        else:
            raise Exception("Course not available")

    def get_credit_hours(self):
        """
        method to get number of credit hours the course is
        :return: the number of credit hours
        """
        r = session.get(self.u.get_url())
        credit_hours = r.xml.xpath("//creditHours/text()", first=True)
        return int(credit_hours)

    def get_no_lectures(self):
        """
        method to get number of lecture sections for the course
        :return: the number of open lecture sections
        """
        sections = self.get_open_sections()
        count_lec = 0
        for name, crn in sections:
            if 'lecture' in self.req.get_section_type(crn).lower():
                count_lec += 1
        return count_lec

    def get_no_disc(self):
        """
        method to get number of discussion sections for the course
        :return: the number of open discussion sections
        """
        sections = self.get_open_sections()
        count_disc = 0
        for name, crn in sections:
            if 'discussion' in self.req.get_section_type(crn).lower():
                count_disc += 1
        return count_disc

    def get_no_lab(self):
        """
        method to get number of lab sections for the course
        :return: the number of open lab sections
        """
        sections = self.get_open_sections()
        count_disc = 0
        for name, crn in sections:
            if 'lab' in self.req.get_section_type(crn).lower():
                count_disc += 1
        return count_disc

    def get_time(self, section_str):
        """
        method to get the starting and ending times
        :param section_str: the CRN of the section
        :return: the starting and ending times of the section
        """
        r = session.get(self.u.url + str(section_str) + ".xml")
        start_time = r.xml.xpath("//meetings/meeting/start/text()", first=True)
        end_time = r.xml.xpath("//meetings/meeting/end/text()", first=True)
        s = ""
        e = ""
        if start_time[6] == 'P':
            s += str(12 + int(start_time[1]))
            e += str(12 + int(end_time[1]))
        else:
            s += start_time[0]
            e += end_time[0]
            s += start_time[1]
            e += end_time[1]
        s += start_time[2:5]
        e += end_time[2:5]
        classes_on_day = self.get_days(section_str).strip()
        return tuple((s.strip(), e.strip(), classes_on_day))

    def get_location(self, section_str):
        """
        method to get the location
        :param section_str: the CRN of the section
        :return: the room number and building of the section
        """
        r = session.get(self.u.url + str(section_str) + ".xml")
        building = r.xml.xpath("//meetings/meeting/buildingName/text()", first=True)
        room = r.xml.xpath("//meetings/meeting/roomNumber/text()", first=True)
        return room + ' ' + building

    def get_instructor(self, section_str):
        """
        method to get the name of the instructor
        :param section_str: the CRN of the section
        :return: the name of the instructor
        """
        r = session.get(self.u.url + str(section_str) + ".xml")
        instructor = r.xml.xpath("//meetings/meeting/instructor/text()", first=True)
        return instructor

    def get_days(self, section_str):
        """
        method to get days of the week
        :param section_str: the CRN of the section
        :return: the days of the week on which there is class
        """
        r = session.get(self.u.url + str(section_str) + ".xml")
        days = r.xml.xpath("//meetings/meeting/daysOfTheWeek/text()", first=True)
        return days

    def get_section_type(self, section_str):
        """
        method to get type of the section
        :param section_str: the CRN of the section
        :return: the type of the section
        """
        r = session.get(self.u.url + str(section_str) + ".xml")
        type = r.xml.xpath("//meetings/meeting/type/text()", first=True)
        return type

    def get_types(self):
        """
        method to return all required classes
        :return:
        """
        types = []
        r = session.get(self.u.get_url())
        for i in range(1, 200):
            crn = '//section[%s]/@id' % (str(i))
            item = r.xml.xpath(crn, first=True)
            if item is None:
                break
            types.append(self.get_section_type(item))
        return types
