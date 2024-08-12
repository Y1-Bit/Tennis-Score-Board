FROM python:3.11

WORKDIR /tennis_score_board

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY tennis_score_board ./tennis_score_board

