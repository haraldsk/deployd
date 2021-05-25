# starting minikube


# using locally built image in minikube

https://stackoverflow.com/questions/42564058/how-to-use-local-docker-images-with-minikube

```
eval $(minikube docker-env)
docker build -t deployd:0.0.1 .
```

# access minikube from inside container

https://stackoverflow.com/questions/61686660/how-to-access-the-minikube-from-a-docker-container


# echoserver
https://github.com/cilium/echoserver/blob/master/Dockerfile
