FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# --------------------------
# Install System Dependencies
# --------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    g++-10 \
    cmake \
    git \
    python3.9 \
    python3-pip \
    perl \
    wget \
    xz-utils \
    libssl-dev \
    clang \
    lld \
    coreutils \
    && rm -rf /var/lib/apt/lists/*

# Set default compiler
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100

# Project root
WORKDIR /workspace

# Copy repo directly into project root
COPY . /workspace

# Start container in project root
WORKDIR /workspace
