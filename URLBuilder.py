
class URLBuilder(object):

    def __init__(self, year, semester):
        '''
        Constructor to initialize URL Builder.
        :param year: Academic year for registration
        :param semester: Semester to register for
        '''
        self.url = "https://courses.illinois.edu/cisapp/explorer/schedule/"
        self.url += year + '/'
        self.url += semester + '/'
        self.subject_count = 0
        self.course_count = 0

    def set_subject_code(self, subject_code):
        if self.subject_count > 0 and self.course_count > 0:
            self.url = self.url[0:len(self.url) - 1]
            prev_index = self.url.rfind('/')
            self.url = self.url[0:prev_index]
            prev_index = self.url.rfind('/')
            self.url = self.url[0:prev_index] + '/' + subject_code + '/'
            self.course_count = 0
        elif self.subject_count > 0:
            self.url = self.url[0:len(self.url) - 1]
            prev_index = self.url.rfind('/')
            self.url = self.url[0:prev_index] + '/' + subject_code + '/'
        else:
            self.url += subject_code + '/'
            self.subject_count = 1

    def set_course_num(self, course_num):
        if self.course_count > 0:
            self.url = self.url[0:len(self.url) - 1]
            prev_index = self.url.rfind('/')
            self.url = self.url[0:prev_index + 1] + course_num + '/'
        else:
            self.url += course_num + '/'
            self.course_count = 1

    def get_url(self):
        temp_url = self.url
        temp_url = temp_url[0:len(temp_url) - 1].strip()
        temp_url += '.xml'
        return temp_url
