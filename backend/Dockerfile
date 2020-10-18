FROM python:3.8.3
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV TZ Asia/Tokyo

RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  vim \
  && rm -rf /var/lib/apt/lists/*

# pipのアップデート
RUN pip3 install --upgrade pip setuptools wheel
# Poetryをインストール
RUN pip3 install poetry

# コンテナ内で仮想環境の作成を無効
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project true

COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt
COPY ./ /app/

CMD ["bash"]

EXPOSE 8000
