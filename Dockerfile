FROM python:3.11-slim AS base
WORKDIR /app

# Install system dependencies for performance and security
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Use a non-root user for security
RUN useradd -m botuser
USER botuser

# Start the bot
CMD ["python", "bot.py"]
