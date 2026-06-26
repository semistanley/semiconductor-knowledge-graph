FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY settings.py run_platform.py ./
COPY semiconductor_doc_ingest.py semiconductor_kg_qa.py tech_Data.py tech_entity.py tech_relationship.py ./
COPY web_app ./web_app
COPY automation ./automation
COPY scripts ./scripts
COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh

RUN sed -i 's/\r$//' /docker-entrypoint.sh \
    && chmod +x /docker-entrypoint.sh \
    && mkdir -p web_app/data automation/inbox automation/outbox automation/processed automation/logs

ENV PYTHONPATH=/app:/app/web_app

EXPOSE 5000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "--chdir", "/app/web_app", "app:app"]
