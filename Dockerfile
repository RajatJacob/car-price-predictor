FROM python:3.10

WORKDIR /app

COPY ./.venv ./

RUN python3 -m venv .venv

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

# CMD ["python3", "app.py"]
CMD [ "python3", "-m" , "streamlit", "run", "app.py"]
