# Deployd

Deployd is a demo application that runs on minikube and installs
kubernetes manifests of applications into a configure namespace in
minikube.

It will deploy all manifests in the `deploy/manifests` directory of a
configured application repository.

It will redeploy on changes to the repository and fetching of the k8s
objects through an API.

* [an-application](https://github.com/haraldsk/an-application)
* [an-other-application](https://github.com/haraldsk/an-other-application)

## Install

### Dependendcies
* [minikube](https://minikube.sigs.k8s.io/docs/start/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Setup

To build images for minikube docker environment needs to point to
minikube

```
$  eval $(minikube -p minikube docker-env)
```

### Building the deployd image

```
$ docker build -t deployd:0.0.1 .
```

### Deploying deployd deployment and service

```
$ kubectl apply -f k8s/
```

### Redeploying image in a running minikube

First run docker build as stated above

```
kubectl -n kube-system rollout restart deployment deployd
```

### Accessing the service

Open a minikube tunnel to the service

```
$ minikube service deployd -n kube-system
```

Get the port number from the output.

You can now get the status of the deployed kubernetes objects.

```
$ curl http://127.0.0.1:<port>/deployment/haraldsk/an-application
$ curl http://127.0.0.1:<port>/deployment/haraldsk/an-other-application
```
