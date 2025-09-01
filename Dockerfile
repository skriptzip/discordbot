FROM python:3.11-slim AS base
WORKDIR /app

LABEL org.opencontainers.image.title="discordbot" \
	org.opencontainers.image.description="A Discord bot application using Python." \
	org.opencontainers.image.url="https://github.com/skriptzip/discordbot" \
	org.opencontainers.image.source="https://github.com/skriptzip/discordbot" \
	org.opencontainers.image.authors="skript.zip <info@skript.zip>" \
	org.opencontainers.image.licenses="MIT" \
	org.opencontainers.image.vendor="skript.zip" \
	org.opencontainers.image.documentation="https://github.com/skript.zip/discordbot#readme" \
	org.opencontainers.image.ref.name="latest" \
	org.opencontainers.image.revision="commit-sha"

# Install system dependencies for performance and security
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY bot/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# Copy bot source code to a default location (not the final location)
COPY bot/ ./bot-default/

# Copy the entrypoint script
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Use a non-root user for security
RUN useradd -m botuser && chown -R botuser:botuser /app
USER botuser

# Use the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
