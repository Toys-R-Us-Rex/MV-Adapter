FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

LABEL org.opencontainers.image.source=https://github.com/Toys-R-Us-Rex/MV-Adapter

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    wget \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set python3.10 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Upgrade pip
RUN pip install --upgrade pip

# Install PyTorch with CUDA 11.8 support
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install Nvdiffrast
RUN pip install --no-build-isolation git+https://github.com/NVlabs/nvdiffrast.git

WORKDIR /workspace
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install the package in editable mode (if setup.py exists)
RUN pip install -e .

# Create output directory
RUN mkdir -p /workspace/outputs /workspace/checkpoints

# Expose port for Gradio demo (default: 7860)
EXPOSE 7860

CMD ["bash"]