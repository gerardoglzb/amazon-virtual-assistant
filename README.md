<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Amazon Virtual Assistant</h3>

  <p align="center">
    A web app that tracks Amazon product prices for you.
    <br />
    <a href="https://github.com/gerardoglzb/amazon-virtual-assistant"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://type-racing.herokuapp.com/">View Demo</a> -->
    <!-- · -->
    <a href="https://github.com/gerardoglzb/amazon-virtual-assistant/issues">Report Bug</a>
    ·
    <a href="https://github.com/gerardoglzb/amazon-virtual-assistant/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](http://amazon-va.herokuapp.com/)

A simple web app where a user can add Amazon products through their urls and have them all displayed on their personal board. Alongside each product, they're able to specify a price they're looking for, and whenever a product drops below said price, the app will also notify the user through their email.

### Built With
* HTML5
* CSS3
* [Javascript](https://www.javascript.com/)
* [Python3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [gunicorn](https://gunicorn.org/)
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
* [APScheduler](https://apscheduler.readthedocs.io/en/stable/)
* [Redis](https://redis.io/)



<!-- GETTING STARTED -->
## Getting Started

Follow these steps to get your own local copy up and running.

### Prerequisites

* pip

### Installation

1. Clone the repo

```sh
git clone https://github.com/gerardoglzb/amazon-virtual-assistant.git
```

2. Install python packages

* Packages in requirements.txt file
```sh
pip3 install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

You can run the project like this:

```sh
python3 run.py
```

Make sure to also start your redis server like this:

```sh
redis-server
```

And run the worker:
```sh
python3 worker.py
```

And finally, the clock:
```sh
python3 clock.py
```

These four must be running simultaneously.

And that's it! You have your own local copy of the Amazon Virtual Assistant. You can try this out by accessing your localhost:5000 on your browser.

You can host this on a site like [Heroku](https://www.heroku.com/). However, the way it's set right now, using Heroku would require three dynos (at least $21).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

<!-- Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com -->

Project Link: [https://github.com/gerardoglzb/amazon-virtual-assistant](https://github.com/gerardoglzb/amazon-virtual-assistant)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: https://i.ibb.co/VvpRP55/ava-ss.png