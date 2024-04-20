# detroit_placekey_data

The idea of this project is simply to display data about Detroit blight violations and home sales aggregated at a placekey level.

# Dependancy installations

This project uses [poetry](https://python-poetry.org/) for dependancy management. Follow the installation instructions on their website to install it. Furthermore, this project makes use of [pyenv](https://github.com/pyenv/pyenv) to ensure the project uses `python = "^3.9"`. This is additionally specified in the `pyproject.toml` file.

 To install the dependancies, cd into the directory with the `pyproject.toml` file and run `poetry shell`, followed by `poetry install`. If you have issues with dependancies, make sure to check which python version you're using by running `pyenv version`. If it's not at least 3.9, you're gonna have a bad time. 


# Running the server

To run the server, enter into the poetry shell and run `uvicorn api:app --reload`


To view the map, open the `index.html` file in a browser.