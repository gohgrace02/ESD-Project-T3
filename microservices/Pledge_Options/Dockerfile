FROM python:3-slim
# ENV STRIPE_API_URL=https://api.stripe.com/v1
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./pledge_options.py ./pledge_options.py
COPY ./amqp_connection.py ./amqp_connection.py
COPY ./amqp_setup.py ./amqp_setup.py
CMD [ "python", "pledge_options.py" ]