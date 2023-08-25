# Use the official Python image as the base image
FROM python:3.8

# Set the working directory
WORKDIR /opt/PDD_Bez_Zabot

# Copy the requirements file into the container
COPY requirements.txt .

RUN python3 -m pip install virtualenv 
RUN python3 -m virtualenv /opt/bot/venv

RUN /opt/bot/venv/bin/pip install -r requirements.txt

COPY . .

# Start the bot
CMD ["/opt/PDD_Bez_Zabot/venv/bin/python", "bot.py"]
