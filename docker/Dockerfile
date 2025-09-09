# Set base imagem
FROM python:3.11.9-slim

# Set working directory to workspace
WORKDIR /workspace

# Create and virtual environemtn with venv
RUN python -m venv /venv

# Activate virtual environemnt
RUN . /venv/bin/activate

# Copy requirements.txt to workspace
COPY ./requirements.txt .

# Install requirements on vvenv
RUN pip install -r requirements.txt

# Copy all files, except config folder, to workspace
COPY [^config]* .

# Turn entrypoint.sh and run.sh  executables
RUN chmod +x entrypoint.sh run.sh

# Copy config folder as a config tamplate
COPY ./config ./config_template

# Run label studio
CMD . /venv/bin/activate && ./entrypoint.sh
