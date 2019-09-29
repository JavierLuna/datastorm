FROM ubuntu:18.04
MAINTAINER javierluna

LABEL com.circleci.preserve-entrypoint=true

ARG CLOUD_SDK_VERSION=255.0.0
ARG DATASTORE_PROJECT_ID=datastorm-test-env

ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV DATASTORE_PROJECT_ID=$DATASTORE_PROJECT_ID
ENV DATASTORE_EMULATOR_HOST=localhost:8081
ENV PATH /google-cloud-sdk/bin:$PATH

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y -qq curl python3 python3-dev python3-pip python3-venv gcc openjdk-8-jdk && pip3 install pipenv --user

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image && \
    gcloud config set project ${DATASTORE_PROJECT_ID} && \
    gcloud components install cloud-datastore-emulator beta --quiet

EXPOSE 8081

VOLUME ["/root/.config", "/opt/data"]

ENTRYPOINT ["gcloud", "beta", "emulators", "datastore", "start", "--host-port=0.0.0.0:8081", "--consistency=1", "--project=datastorm-test-env"]
