from flask import Flask, request
from flask_restful import Api, Resource
from Request import Request
from Schedule import Schedule
import json
import os
app = Flask(__name__)
api = Api(app)


class Register(Resource):

    def post(self):
        reg = request.data
        reg_json = json.loads(reg)
        taken_string = reg_json['courses']
        taken = taken_string.split(",")
        taken = [c.strip() for c in taken]
        major = reg_json['major']
        tecno = int(reg_json['techCourses'])
        min_credits = int(reg_json['minimumCredits'])
        max_credits = int(reg_json['maximumCredits'])
        year = reg_json['year']
        semester = reg_json['semester']
        req = Request(year, semester)

        sched = Schedule(req, major, taken, tecno, min_credits, max_credits)
        sched.build_this_term()
        sched.get_open_this_sem()
        sched.build_times()
        r = {}
        for key, val in sched.times.items():
            sub, num = key
            r[sub + ' ' + num] = list(val)
        for key, val in r.items():
            temp = []
            for c in val:
                crn, t = c
                s, e, d = t
                temp.append((crn, s, e, d))
            r[key] = list(temp)
        r = json.dumps(r)
        r_e = json.loads(r)
        f = open("temp.txt", "w+")
        with f as outfile:
            json.dump(r_e, outfile)
        f.close()
        return 200

    def get(self):
        with open("temp.txt", "r") as json_file:
            to_send = json.load(json_file)
        print(to_send)
        return to_send, 200


api.add_resource(Register, "/register")
app.run(host='0.0.0.0')
