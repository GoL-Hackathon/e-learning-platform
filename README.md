# E-Learning Application
- This is an e-learning platform which provides *content management system (CMS)*.
- Its a versatile system to manage different types of content for the course modules.
    - Meaning you can get files, videos or images as contents.
 
## Technologies used
- The application is built with Python(Django), HTML, CSS and JavaScript(JQuery).

### Technologies breakdown
- It uses class-based views Mixins. They help in working with groups and permissions to restrict access to your views.
- The project uses formsets to manage course modules.
- Also, Memcached backend caching system.

## Features
- A Tutor/Owner/Author can login and post a course.
    - The course is divided into modules.
    - They have the right to update, delete update a certain course/module.
- A student/learner can login, see the courses catalog, and get enrolled in a course of choice.
    - Also they can enroll in multiple courses.

## Installation
- Fork the project to your account then clone it.
- Create a virtual environment with `python -m venv venv`
- Activate the virtual environment with `source venv/bin/activate` then install the project packages with `pip install -r requirements.txt`
- Refer to the `.env example` file for more information on PostgreSQL configurations for the project.

<!-- ![alt text for screen readers](./static/images/search.png "Search Module"). -->

## Authors
- Waithaka Waweru (Backend Development)
    - [Github](https://github.com/weshy007)
- Castro Mbithi (Frontend Development)
    - [Github](https://github.com/castrombithisamm)
- Mergery Wanjiru (Technical Writter)
    - [Github](https://github.com/Mergery)
- Museveni Brian (Technical Writter && Frontend Developer)
    - [Github](https://github.com/Museveni254)


## Contributing
Pull requests are welcome.

Please make sure to update tests as appropriate.

## License
&copy; [MIT](https://choosealicense.com/licenses/mit/)
