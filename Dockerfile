FROM debian:bullseye
ARG token
ARG forwardDest
ARG ownerID
RUN if [ -z ${token} ]; then echo "Token not found."; exit -1; fi && \
    if [ -z ${forwardDest} ]; then echo "Forward destination not found."; exit -1; fi && \
    if [ -z ${ownerID} ]; then echo "Owner ID not found."; exit -1; fi && \
    apt-get update && \
    apt-get install -y \
        git \
        python3-certifi \
        python3-cryptography \
        python3-future \
        python3-tornado \
        python3-pip && \
    git clone -b master https://github.com/KungFur/munsin.git /var/lib/munsin && \
    pip3 install -r /var/lib/munsin/requirements.txt && \
    sed "s/^token\ =\ .*$/token\ =\ '${token}'/;s/^forwardDest\ =\ .*$/forwardDest\ =\ ${forwardDest}/;s/^ownerID\ =\ .*$/ownerID\ =\ ${ownerID}/" /var/lib/munsin/config.sample.py > /var/lib/munsin/config.py && \
    apt-get purge -y \
        git \
        python3-pip && \
    apt-get clean -y && \
    apt-get autoclean -y && \
    apt-get autoremove -y && \
    rm -rf /var/lib/munsin/.git /var/lib/munsin/.gitignore
WORKDIR /var/lib/munsin
ENTRYPOINT /var/lib/munsin/main.py
