FROM python:3.12-slim

WORKDIR /app

# Install the SDK from local source
COPY pyproject.toml ./
COPY superinstance/ ./superinstance/
RUN pip install -e .

# Demo script
COPY demo.py ./

CMD ["python", "demo.py"]
