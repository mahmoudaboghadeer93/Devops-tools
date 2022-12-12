FROM summerwind/actions-runner-dind

ENV ANDROID_HOME="/opt/cmdline-tools/latest/bin/"
USER root
WORKDIR /root/
# to run dpkg (behind other tools like Apt) without interactive dialogue
ARG DEBIAN_FRONTEND=noninteractive
# tools and packages versions
ARG WM_VERSION=v2021.03.01.00
ARG NPM_VERSION=7.10.0
ARG GRADLE_VERSION=gradle-7.4.1
ARG ANDROID_SDK_VERSION=commandlinetools-linux-7583922_latest
#ARG ANDROID_SDK_VERSION=tools_r25.2.3-linux
ARG SDK_BUILD_TOOLS_VERSION_1=31.0.0
ARG SDK_BUILD_TOOLS_VERSION_2=30.0.3
ARG SKD_PLATFORMS_1=android-33
ARG SKD_PLATFORMS_2=android-31
ARG NODE_VERSION=16.0.0
ARG JAVA_VERSION=openjdk-11-jdk
ARG SONAR_SCANNER_VERSION=sonar-scanner-cli-3.2.0.1227-linux

RUN   apt update -y \
  &&  apt upgrade -y \ 
  &&  apt install curl npm wget  -y \
  &&  curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" \
  &&  chmod +x ./kubectl \
  &&  mv ./kubectl /usr/local/bin/kubectl \
  &&  mkdir /opt/gradle \
  && cd /opt/gradle \
  &&  wget https://services.gradle.org/distributions/$GRADLE_VERSION-all.zip \
  &&  unzip -d /opt/gradle $GRADLE_VERSION-all.zip \
  &&  rm /opt/gradle/$GRADLE_VERSION-all.zip \
  &&  ln -s /opt/gradle/${GRADLE_VERSION}/bin/gradle /usr/local/bin/gradle

# install android-sdk
WORKDIR /opt
ARG DEBIAN_FRONTEND=noninteractive
RUN  apt install -y ${JAVA_VERSION}\
  && wget https://dl.google.com/android/repository/$ANDROID_SDK_VERSION.zip \ 
  && export PATH=${PATH}:~/android-sdk-linux/toolsi \
  && export PATH=${PATH}:~/android-sdk-linux/platform-tools \
  && unzip ${ANDROID_SDK_VERSION}.zip && rm ${ANDROID_SDK_VERSION}.zip 
RUN cd cmdline-tools && mkdir latest &&  mv NOTICE.txt  bin  lib  source.properties latest && cd latest/bin/ \
  && yes | ./sdkmanager --licenses --sdk_root=/opt/cmdline-tools/latest/bin  \
  &&  ./sdkmanager --list  \
  && yes | ./sdkmanager "tools" "platform-tools" --sdk_root=/opt/cmdline-tools/latest/bin \
  && yes | ./sdkmanager "build-tools;${SDK_BUILD_TOOLS_VERSION_1}" "build-tools;${SDK_BUILD_TOOLS_VERSION_2}" --sdk_root=/opt/cmdline-tools/latest/bin \
  && yes | ./sdkmanager "platforms;${SKD_PLATFORMS_1}" "platforms;${SKD_PLATFORMS_2}" --sdk_root=/opt/cmdline-tools/latest/bin \ 
  &&  chmod 777 /opt/cmdline-tools/latest/bin
RUN  npm install -g n \
 &&  npm install -g npm@${NPM_VERSION} \
 &&  n install ${NODE_VERSION} 
#install gh cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&&  chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&&  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" |  tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&&  apt update \
&&  apt install gh -y \
&&  npm install eslint -g \
&&  chown -R runner:runner /home/runner/ \
&&  rm -rf /var/lib/apt/lists/*
RUN chmod 777 /home/runner/  
USER runner  
COPY ./git-credentials /home/runner/.git-credentials
RUN git config --global credential.helper store  \
 && git config --global --add safe.directory '*' 
