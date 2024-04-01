FROM python:3-slim
# ENV STRIPE_API_URL=https://api.stripe.com/v1
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./user.py ./user.py
COPY ./utils.py ./utils.py
CMD [ "python", "user.py" ]