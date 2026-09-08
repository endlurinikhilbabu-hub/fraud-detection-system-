FROM python:3.12-slim

WORKDIR /app

# Install production dependencies only
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Create a non-root application user
RUN useradd --create-home --shell /bin/bash appuser

# Copy application code and model artifacts
COPY api ./api
COPY src ./src
COPY models ./models

# Give the application user access to the application files
RUN chown -R appuser:appuser /app

# Switch away from root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
