FROM python
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo "export PATH="/root/.local/bin:$PATH""
RUN echo "export PATH="/root/.local/bin:$PATH"" >> /etc/bash.bashrc
ENV PATH="$PATH:/root/.local/bin:$PATH"
WORKDIR /usr/app
COPY . .
RUN chmod 777 ./forestreeApp/manage.py
RUN poetry install
EXPOSE 8500
CMD ["poetry","run", "./forestreeApp/manage.py", "runserver"]