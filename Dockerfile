FROM node:14.3.0 AS frontend
COPY frontend/ /frontend
WORKDIR /frontend
RUN npm i --no-optional
RUN npm run build

FROM python:3.8
ENV PRODUCTION=1

COPY backend/ /backend
COPY  --from=frontend /frontend/dist /backend/static

WORKDIR /backend
RUN pip install -r requirements.txt
CMD ["uvicorn","backend:app"]
