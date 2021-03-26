#!/bin/bash

set -x
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE:-$0}")"; pwd)"/..


KAFKA_VERSION=2.7.0
KAFKA_BUILD_DIR=${ROOT_DIR}/pkg/kafka/
KAFKA_SRC=kafka-${KAFKA_VERSION}-src

if [[ ! -f ${KAFKA_BUILD_DIR}/${KAFKA_SRC}/bin/kafka-server-start.sh ]]; then

    KAFKA_DOWNLOAD=kafka-${KAFKA_VERSION}-src.tgz

    mkdir -p ${KAFKA_BUILD_DIR}
    wget https://mirrors.dotsrc.org/apache/kafka/${KAFKA_VERSION}/kafka-${KAFKA_VERSION}-src.tgz -P ${KAFKA_BUILD_DIR}
    tar -xzf ${KAFKA_BUILD_DIR}/${KAFKA_DOWNLOAD} -C ${KAFKA_BUILD_DIR}
    rm ${KAFKA_BUILD_DIR}/${KAFKA_DOWNLOAD}
fi
