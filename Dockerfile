FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

ENV TORCH_CUDA_ARCH_LIST="7.0;7.5;8.0;8.6;8.9;9.0"

COPY --from=continuumio/miniconda3:4.12.0 /opt/conda /opt/conda

ENV PATH=/opt/conda/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    ninja-build \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libegl1-mesa-dev \
    libgles2-mesa-dev \
    libosmesa6-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip cache purge

WORKDIR /workspace

COPY . .

RUN conda create -n mvadapter python=3.10
ENV PATH=/opt/conda/envs/mvadapter/bin:$PATH

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

RUN pip install --no-build-isolation -r requirements.txt

CMD ["bash"]
