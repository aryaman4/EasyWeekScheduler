import React, {Component} from 'react';
import { Link } from 'react-router-dom';
import { Jumbotron, Grid, Row, Col, Image, Button} from 'react-bootstrap';
import './home.css';
import About from './about';



export default class Home extends Component {
  constructor() {
      super();
      this.handleSubmit = this.handleSubmit.bind(this);
      this.getData = this.getData.bind(this);
      const fetch = window.fetch.bind(window);
      this.state = {
        show: false
      };
    }

    getData = async () => {
      const request = {
        method: 'GET',
        mode: 'no-cors',
        // mode: { mode: 'no-cors'},
        // headers: typeof Headers !== 'undefined' ? new Headers({ 'content-type': 'application/x-www-form-urlencoded' }) : { 'content-type': 'application/x-www-form-urlencoded'}
      }

      const response = await fetch('http://127.0.0.1:5000/register', request);
      const body = await response.json()
      return body;
    }

  async handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    const name = data.get('username');
    const courses = data.get('courses');
    const major = data.get('major');
    const standing = data.get('standing');
    const techCourses = data.get('techCourses');
    const minimumCredits = data.get('minimumCredits');
    const maximumCredits = data.get('maximumCredits');
    const minorCourses = data.get('minor');
    const sem = data.get('sem');
    const year = data.get('year');

    const obj = {
      name: name,
      courses: courses,
      major: major,
      standing: standing,
      techCourses: techCourses,
      minimumCredits: minimumCredits,
      maximumCredits: maximumCredits,
      minorrelatedCourses: minorCourses,
      semester: sem,
      year: year
    };
    // var request = new XMLHttpRequest();
    // request.mode = 'no-cors'
    // request.open("POST", "http://127.0.0.1:5000/register");
    // request.setRequestHeader("Content-Type", "text/plain; charset=UTF-8");
    // request.send(JSON.stringify(obj))
    // console.log("Done")

    // console.log("huvjh")
    // fetch('http://0.0.0.0:5000/register', {
    //   method: 'GET'
    // }).then(response => response.json())
    // request.open("GET", "http://0.0.0.0:5000/register");
    // request.onload = async function() {
    //   console.log("in")
    //   var schedule = JSON.parse(request.responseText);
    //   if (request.readyState == 4 && request.status == "200") {
    //       console.log(schedule)
    //   } else {
    //       console.error(schedule)
    //   }
    // }
    // var arr = await this.getData();

   //  event.preventDefault();
    fetch('http://127.0.0.1:5000/register', {
     method: 'post',
     mode: 'no-cors',
     headers: {'Content-Type':'application/json'},
     body: JSON.stringify(obj)
   }).then((response) => {
     console.log("Post sent status: " + response.status)
   })
   this.setState({ show: true });

    // this.props.history.push('/about')
    //send all of information to backend
    //recieve schedule output
    // route to new page to display schedule output
  }
  render() {
    return (
      <div>
      <Grid>
        <Jumbotron>
          <h2> Welcome to EasyWeek </h2>
          <p> This is the ideal schedule optimizer app! </p>
          <form onSubmit={this.handleSubmit}>
            <div>
              <label htmlFor="name">Enter your name  </label>
              <input id="username" name="username" type="text" />
            </div>
            <div>
              <label htmlFor="birthdate">Enter your courses (Ex. CS 125, Math 241 etc.)  </label>
              <input id="courses" name="courses" type="text" />
              </div>
            <div>
              <label htmlFor="major">Enter your major (CS, CE etc.) </label>
              <input id="major" name="major" type="text" />
            </div>
            <div>
              <label htmlFor="standing">Enter your standing (Freshman, Sophmore etc.)  </label>
              <input id="standing" name="standing" type="text" />
            </div>
            <div>
              <label htmlFor="techCourses">Enter the maximum amount of technical courses you are willing to take</label>
              <input id="techCourses" name="techCourses" type="text" />
            </div>
            <div>
              <label htmlFor="standing">Maximum number of credits you are willing to take</label>
              <input id="maximumCredits" name="maximumCredits" type="text" />
            </div>
            <div>
              <label htmlFor="standing">Minimum number of credits you are willing to take</label>
              <input id="minimumCredits" name="minimumCredits" type="text" />
            </div>
            <div>
              <label htmlFor="standing">Number of possible minor-related courses to take</label>
              <input id="minor" name="minor" type="text" />
            </div>
            <div>
              <label htmlFor="semester">Which semester are you in</label>
              <input id="sem" name="sem" type="text" />
            </div>
            <div>
              <label htmlFor="year">Which year are you in</label>
              <input id="year" name="year" type="text" />
            </div>
            <button>Send data!</button>
          </form>
        </Jumbotron>
      </Grid>
      <div>
        <About show={this.state.show}>

        </About>
      </div>
      </div>

    )
  }
}
