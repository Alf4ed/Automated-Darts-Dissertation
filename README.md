# 🎯 CS310

This project is an automated scoring and shot recommendation/analysis system for darts games. It provides real-time insights and analysis to help players improve their game.

## Built With

This project was developed using the following tools and libraries:

- Python
- JavaScript
- Flask
- OpenCV
- SciPy
- jQuery

## Getting Started

Follow these steps to get a local copy up and running:

### Installation



1. Obtain the code:

   If you have access to the repository, clone it using the following command:

    `git clone https://github.com/Alf4ed/cs310.git`

   Alternatively, if you already have a copy of the code, navigate to the directory where the code is located.

3. Create a virtual environment:

    `python -m venv env`
    
4. Activate the virtual environment:
   
    On Windows:
   
        .\env\Scripts\activate
   
    On Unix or MacOS:
   
        source env/bin/activate
   
5. Install the required packages from the requirements.txt file:
   
    `pip install -r requirements.txt`

### Usage

1. Move into the src directory:
   
    `cd src`
   
2. Run _start.py_ or _startTests.py_ using Python:
   
    `python start.py`

3. Access the webserver by visiting the following URL:

   http://localhost:5000

## License

This project is distributed under the MIT License. See LICENSE.txt for more information.

## Note

Please note that the code requires live camera feeds. Without the camera feeds, the system uses prerecorded videos, so the different pages can be viewed, but the functionality is not entirely as expected.
