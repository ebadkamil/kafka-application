#!/bin/bash

set -x
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE:-$0}")"; pwd)"/..


KAFKA_VERSION=2.7.0
KAFKA_BUILD_DIR=${ROOT_DIR}/pkg/kafka/
KAFKA_SRC=kafka_2.13-${KAFKA_VERSION}

if [[ ! -f ${KAFKA_BUILD_DIR}/kafka/bin/kafka-server-start.sh ]]; then

    KAFKA_DOWNLOAD=${KAFKA_SRC}.tgz

    mkdir -p ${KAFKA_BUILD_DIR}
    wget https://mirrors.dotsrc.org/apache/kafka/${KAFKA_VERSION}/${KAFKA_SRC}.tgz -P ${KAFKA_BUILD_DIR}
    tar -xzf ${KAFKA_BUILD_DIR}/${KAFKA_DOWNLOAD} -C ${KAFKA_BUILD_DIR}
    rm ${KAFKA_BUILD_DIR}/${KAFKA_DOWNLOAD}
    mv ${KAFKA_BUILD_DIR}/${KAFKA_SRC} ${KAFKA_BUILD_DIR}/kafka
fi
