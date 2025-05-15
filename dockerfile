FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tzdata \
    git \
    build-essential \
    libopencv-dev \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "train.py"]
