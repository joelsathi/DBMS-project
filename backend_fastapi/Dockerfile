FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY ./requirements.txt /code/

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
