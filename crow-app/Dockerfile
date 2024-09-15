# The first stage will install build dependencies and compile the executable

FROM ubuntu:latest AS builder

RUN set -ex;                                                                      \
    apt-get update;                                                               \
    apt-get install -y clang wget cmake libzmq3-dev unzip libasio-dev;                                \
    mkdir -p /usr/src;                                                            \
    cd /usr/src;                                                                  \
    wget https://github.com/CrowCpp/Crow/releases/download/v1.2.0/Crow-1.2.0.zip;  \
    unzip Crow-1.2.0.zip; \
    cp -R Crow-1.2.0-Darwin/lib/* /usr/local/lib; \
    cp -R Crow-1.2.0-Darwin/include/* /usr/local/include ;

COPY . /usr/src/crow-app

RUN set -ex;              \
    cd /usr/src/crow-app;  \
    cmake -S . -B ./build; \
    cmake --build ./build; 

# The second stage will install the runtime dependencies only and copy
# the compiled executables

FROM ubuntu:latest AS runtime

RUN set -ex;         \
    apt-get update;  \
    apt-get install -y libzmq5

COPY --from=builder /usr/src/crow-app/build/main /usr/local/bin/crow-app

ENTRYPOINT ["crow-app"]
