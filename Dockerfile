FROM node as NODE_BUILDER
WORKDIR /app

COPY . /app

RUN npm i

FROM python:3.9
ENV PYTHONUNBUFFERED=1

#Build code
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#static builds
COPY --from=NODE_BUILDER /app/node_modules /app/static/node_modules

#Entrypoint
ENTRYPOINT ["sh","/app/entrypoint.sh"]