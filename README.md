# RabbitMQ Test in minikube

This repo uses `minikube` to replicate a k8s environment with rabbitMQ as a
broker and a cron-job publisher at regular intervals and a long-running consumer.

Should serve as a testing ground for systems with AMQP communications.


<!--ts-->
* [RabbitMQ Test in minikube](#rabbitmq-test-in-minikube)
   * [How To](#how-to)
      * [Install](#install)
      * [Set up](#set-up)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: ubuntu, at: Wed Jun  1 09:37:46 UTC 2022 -->

<!--te-->

## How To

### Install

> :warn: This assumes `Docker` and `Docker-compose` are already installed in the system

> :warn: This assumes you are running on `Linux x86_64`


1. Install [minikube](https://minikube.sigs.k8s.io/docs/)

  ```bash
  # Download and exec permissions
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  # Add to the path
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
  ```

2. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

  ```bash
  # Download
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  # Install (alternatively install @ ~/.local/bin)
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  ```

3. Install [k9s](https://github.com/derailed/k9s)

  ```bash
  # Download
  wget https://github.com/derailed/k9s/releases/download/v0.25.18/k9s_Linux_arm64.tar.gz
  tar -xvzf k9s_Linux_arm64.tar.gz
  # Install
  sudo install -m 0755 k9s /usr/local/bin/k9s
  ```

### Set up


1. Start minikube

  ```bash
  minikube start
  ```

  > ☝ Optional: Bring up the k8s dashboard: `minikube dashboard --url &`


2. Creating the maipy image

```bash
export PYPI_USR="<YOUR-USER-IN-HERE>"
export PYPI_PWD="<YOUR-PASSWORD-IN-HERE>"
./scripts/build-docker.sh 0.3.6
```

3. Add the image to minikube registry

  ```bash
  minikube image load registry.melior.ai/maipy:0.3.6
  ```

4. Create the services

  ```bash
  kubectl apply -f deployments/rabbit.yml
  kubectl apply -f deployments/consumer.yml
  kubectl apply -f deployments/publisher-cron.yml
  ```

> :bulb: For convinience steps 2 to 4 can be run with: `make update-maipy-image`


