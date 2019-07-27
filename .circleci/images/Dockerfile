FROM python:3.6.9-alpine3.10

ARG CLOUD_SDK_VERSION=255.0.0
ARG DATASTORE_PROJECT_ID=test

ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV DATASTORE_PROJECT_ID=$DATASTORE_PROJECT_ID

LABEL com.circleci.preserve-entrypoint=true

ENV PATH /google-cloud-sdk/bin:$PATH
RUN apk --update --no-cache add \
        curl \
        tar \
        gzip \
        ca-certificates \
        py-crcmod \
        bash \
        libc6-compat \
        openssh-client \
        git \
        gnupg \
        openjdk8-jre \
    && curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image && \
    gcloud components install cloud-datastore-emulator beta --quiet && \
    gcloud config set project ${DATASTORE_PROJECT_ID} && \
    gcloud --version

VOLUME ["/root/.config", "/opt/data"]

EXPOSE 8081

ENTRYPOINT ["gcloud", "beta", "emulators", "datastore", "start", "--data-dir=/opt/data", "--host-port=0.0.0.0:8081", "--consistency=1"]
