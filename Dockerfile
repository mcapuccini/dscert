# Base image
FROM mcr.microsoft.com/azureml/base

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Non-root user with sudo access
ARG USERNAME=default
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Apt deps
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install \
        sudo \
        curl \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    # az CLI
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    # pip deps
    && pip install azureml-sdk[notebooks,automl,explain] \
    # create non-root user
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    # fix conda permissions
    && mkdir /opt/miniconda/pkgs \
    && chown -R $USER_UID:$USER_GID /opt/miniconda/pkgs