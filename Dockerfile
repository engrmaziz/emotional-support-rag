# Use official Python image
FROM python:3.12

# Create a standard user (Required by Hugging Face Spaces security)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory
WORKDIR $HOME/app

# Copy requirements and install
COPY --chown=user ./requirements.txt $HOME/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Download the spaCy NLP model for the PII guardrail
RUN python -m spacy download en_core_web_sm

# Copy the rest of your app's code with the correct permissions
COPY --chown=user . $HOME/app

# Build the vector database dynamically
RUN python ingest.py

# Expose port 7860 and run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]