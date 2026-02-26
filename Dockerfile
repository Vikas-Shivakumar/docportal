FROM python:3.10

# Prevent python buffering
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system deps (needed for PyMuPDF)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt



EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py", "--server.address=0.0.0.0", "--server.port=8501"]
