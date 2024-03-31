FROM python:3-slim
# set stripe api endpoints
# ENV STRIPE_API_URL=https://api.stripe.com/v1
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./back_project.py ./back_project.py
COPY ./amqp_connection.py ./amqp_connection.py
CMD [ "python", "back_project.py" ]