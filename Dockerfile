# Sử dụng một docker có sắn
FROM python:3.9-bullseye

# Tạo một folder root cho project
WORKDIR /api-dashboard
# Copy file requirements.txt vào folder api-dashboard
COPY requirements.txt .
# Install lib
RUN pip install -r requirements.txt
COPY ./app ./app
# Set env
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_PORT=50000
ENV FLASK_RUN_HOST=0.0.0.0
ENV SECRET_KEY=your_secret_key
ENV MAIL_USERNAME=zzro333@gmail.com
ENV MAIL_PASSWORD=wiibdoxuisaydfnb

CMD [ "flask", "run" ]
