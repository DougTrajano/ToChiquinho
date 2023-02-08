ARG PYTORCH_VERSION=1.12.0
ARG PYTORCH_PROCESSOR=gpu
ARG PYTHON_VERSION=py38

FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:${PYTORCH_VERSION}-${PYTORCH_PROCESSOR}-${PYTHON_VERSION}

RUN apt-get update && \
    apt install -y git-lfs libssl-dev && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PATH="/opt/ml/code:${PATH}"

ENV SAGEMAKER_SUBMIT_DIRECTORY /opt/ml/code

WORKDIR /opt/ml/code

CMD ["/bin/bash"]