FROM python:3.8.3
WORKDIR /app

ENV PYTHONPATH /app
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  vim \
  && rm -rf /var/lib/apt/lists/*

# pipのアップデート
RUN pip install --upgrade pip setuptools wheel
# Poetryをインストール
RUN pip install poetry

# RUN pip install uWSGI

# コンテナ内で仮想環境の作成を無効
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project true

# COPY pyproject.toml pyproject.toml
COPY . /app
RUN poetry install

# CMD ["bash"]
# uwsgi --socket :8001 --module config.wsgi
CMD [ "poetry", "run", "uwsgi", "--socket", "：8001", "--module", "config.wsgi"]

EXPOSE 8001
