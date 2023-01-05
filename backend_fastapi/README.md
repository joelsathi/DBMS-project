
### Setup

- (Recommended) Create a python virtual environment and activate it
- `pip install -r requirements.txt`
- copy the `.sample.env` file as `.env` to configure env variables

### Run server

- `uvicorn src.main:app --reload`

### Development notes

- run `flake8` before committing. use black to format .py files