# CyVerseSEChallenge

Deploy a pub-sub service using NATS messaging that collects random quotes from the TV show Friends. Quotes are collected, stored locally in a database, then displayed on screen. Application is containerized with Docker and deployed with Kubernetes using Minikube.

### Run from personal CyVerse Atmosphere VM:

1. Enter app directory

    `cd app/`
    
2. Get IP address of running Kubernetes pod

    `kubectl get pods -o=custom-columns=Name:.metadata.name,IP:.status.podIP`

3. SSH into minikube worker node

    `minikube ssh`
    
4. Demo service on running pod

    `curl 172.17.0.20:5000/`

### Resources

https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/

https://medium.com/@yzhong.cs/getting-started-with-kubernetes-and-docker-with-minikube-b413d4deeb92

https://github.com/nats-io/nats.py
