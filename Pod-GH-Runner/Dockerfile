FROM debian:buster-slim

ENV GITHUB_PAT ""
ENV GITHUB_TOKEN ""
ENV GITHUB_OWNER ""
ENV GITHUB_REPOSITORY ""
ENV RUNNER_WORKDIR "_work"
ENV RUNNER_LABELS ""
ENV ADDITIONAL_PACKAGES ""

RUN apt-get update -y \
    && apt-get install curl git sudo wget jq iputils-ping openjdk-11-jdk -y \
 ###_Install nodejs_22_#####
 && sudo apt-get install ca-certificates curl gnupg -y \
 && sudo mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list \
 && sudo apt-get update -y \
 && sudo apt-get install nodejs -y \
  ###_install mvaven_3.9.6_#####
 && export VER="3.9.6" \
 && sudo wget https://downloads.apache.org/maven/maven-3/$VER/binaries/apache-maven-$VER-bin.tar.gz \
 && sudo tar xvf apache-maven-$VER-bin.tar.gz \
 && sudo mv apache-maven-$VER /opt/maven \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m github \
    && usermod -aG sudo github \
    && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER github
WORKDIR /home/github

RUN GITHUB_RUNNER_VERSION=$(curl --silent "https://api.github.com/repos/actions/runner/releases/latest" | jq -r '.tag_name[1:]') \
    && curl -Ls https://github.com/actions/runner/releases/download/v${GITHUB_RUNNER_VERSION}/actions-runner-linux-x64-${GITHUB_RUNNER_VERSION}.tar.gz | tar xz \
    && sudo ./bin/installdependencies.sh

COPY --chown=github:github entrypoint.sh runsvc.sh ./
RUN sudo chmod u+x ./entrypoint.sh ./runsvc.sh

ENTRYPOINT ["/home/github/entrypoint.sh"]
