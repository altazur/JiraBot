FROM python:3

ARG SLACK_BOT_TOKEN="empty"
ARG JIRA_URL="empty"
ARG JIRA_LOGIN="empty"
ARG JIRA_PASSWORD="empty"

ENV SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN}"
ENV JIRA_URL="${JIRA_URL}"
ENV JIRA_LOGIN="${JIRA_LOGIN}"
ENV JIRA_PASSWORD="${JIRA_PASSWORD}"

ADD bot.py JiraAPI.py bot_command_parser.py /app/
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update \
	&& apt-get install openssl \
	&& apt-get install ca-certificates
CMD [ "python3", "./bot.py" ]
