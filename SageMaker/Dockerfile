FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:1.12.0-gpu-py38

RUN apt-get update && \
    apt install -y git-lfs

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# ENV PATH="/opt/ml/code:${PATH}"