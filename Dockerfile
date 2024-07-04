# # syntax=docker/dockerfile:1

# # Comments are provided throughout this file to help you get started.
# # If you need more help, visit the Dockerfile reference guide at
# # https://docs.docker.com/go/dockerfile-reference/

# # Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

# ARG PYTHON_VERSION=3.12.3
# FROM python:${PYTHON_VERSION}-slim as base

# # Prevents Python from writing pyc files.
# ENV PYTHONDONTWRITEBYTECODE=1

# # Keeps Python from buffering stdout and stderr to avoid situations where
# # the application crashes without emitting any logs due to buffering.
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # Create a non-privileged user that the app will run under.
# # See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

# # Download dependencies as a separate step to take advantage of Docker's caching.
# # Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# # Leverage a bind mount to requirements.txt to avoid having to copy them into
# # into this layer.
# USER root
# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#         gcc \
#     libxss1 \
#     wget \
#     gnupg \
#     unzip \
#     xvfb \
#     libxi6 \
#     libgconf-2-4 \
#     curl \
#     libgconf-2-4

# RUN --mount=type=cache,target=/root/.cache/pip \
#     --mount=type=bind,source=requirements.txt,target=requirements.txt \
#     python -m pip install -r requirements.txt

# # Скачиваем и устанавливаем Google Chrome
# #RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
# #    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
# #    apt-get update && \
# #    apt-get install -y google-chrome-stable

# # Скачивание и установка конкретной версии Google Chrome (версия 114)
# RUN wget -q -O /tmp/google-chrome-stable.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.1234.5678_amd64.deb && \
#     dpkg -i /tmp/google-chrome-stable.deb || apt-get install -f -y

# # Установка ChromeDriver, совместимого с версией 114
# RUN CHROME_DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_114") && \
#     wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" && \
#     unzip /tmp/chromedriver.zip -d /usr/local/bin/

# # Установка переменной окружения PATH
# #ENV PATH="/usr/bin/google-chrome-stable:${PATH}"
# RUN chmod +x /usr/local/bin/chromedriver
# # Switch to the non-privileged user to run the application.
# USER appuser

# # Copy the source code into the container.
# COPY . .

# # Expose the port that the application listens on.
# EXPOSE 8090

# # RUN #echo $PATH
# RUN ls -l /usr/local/bin/chromedriver

# # Run the application.
# CMD python3 -m flask run --host=0.0.0.0 --port=8090

FROM python:3.12

# Удаляем старую версию ChromeDriver, если она существует
RUN rm -f /usr/local/bin/chromedriver

RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
   mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
   curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
   unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
   rm /tmp/chromedriver_linux64.zip && \
   chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
   ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
   echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
   apt-get -yqq update && \
   apt-get -yqq install google-chrome-stable && \
   rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
  unzip \
  curl \
  gnupg \
  && rm -rf /var/lib/apt/lists/*


RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add

RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY parser.py .

CMD [ "python", "parser.py" ]