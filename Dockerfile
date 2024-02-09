FROM python:3.10-slim
WORKDIR /home/user/app
ENV APP_VERSION=${version:-"1.0.0"}
ENV APP_HOST="0.0.0.0"
ENV APP_PORT=8000
EXPOSE 8000 
COPY requirements.txt /home/user/app 
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]