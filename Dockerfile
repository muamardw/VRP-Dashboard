FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY vrp_rl_project/ ./vrp_rl_project/

EXPOSE 8080

CMD ["uvicorn", "vrp_rl_project.backend_api:app", "--host", "0.0.0.0", "--port", "8080"] 