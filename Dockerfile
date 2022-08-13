FROM intelligentdesigns/streamlit-plus:minimal-latest
MAINTAINER Arun rpakishore@gmail.com

#Set Working directory
WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

#Expose Port 8501 for app to be run on
EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", "run"]
CMD ["About.py"]