# Stage 1: Build dependencies in a virtual environment
FROM python:3.11-buster AS builder

WORKDIR /app

# Copy requirements to the build stage
COPY requirements.txt .

# Set up and activate virtual environment, then install dependencies
RUN python -m venv /app/.venv && \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim-buster AS runtime

# Environment variables for virtual environment
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Set working directory
WORKDIR /app

# Copy the source code
COPY src .

# Install any additional runtime dependencies
RUN pip install uvicorn streamlit

# Expose the necessary port
EXPOSE 5500

# Set the entry point for running the application, update as necessary
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5500"]
