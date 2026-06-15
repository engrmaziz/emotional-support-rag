# Use official Python image
FROM python:3.12

# Set the working directory
WORKDIR /code

# Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Download the spaCy NLP model for your PII guardrail
RUN python -m spacy download en_core_web_sm

# Copy the rest of your app's code
COPY . .

# Build the vector database dynamically during deployment
RUN python ingest.py

# Expose port 7860 and run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]