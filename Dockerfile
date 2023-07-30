FROM python:3.9-slim
MAINTAINER Arun rpakishore@gmail.com

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

RUN pip3 install --no-cache -r requirements.txt

COPY . /app

<<<<<<< HEAD
ENTRYPOINT ["streamlit", "run"]
CMD ["About.py"]
=======
ENTRYPOINT ["streamlit", "run", "About.py", "--server.port=8501", "--server.address=0.0.0.0"]
>>>>>>> d8c8a0c1a4483d4f608430d28764b352a9200fa7
