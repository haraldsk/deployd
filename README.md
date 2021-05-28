# Deployd

Deployd is a demo k8s deployment application that runs on minikube.

It installs kubernetes manifests bundled with applications into a
configured namespace in minikube.

It deploys all k8s manifests in the `deploy/manifests` directory of a
configured application repostitory.

Redeploy is triggered on changes to the repository.

The status of the deployed k8s objects can be observed through an API.

By default the application will deploy the two following sample
applications.

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
$ kubectl -n kube-system rollout restart deployment deployd
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

## Bugs and caveats
* This code should be considered as a demo / alpha state
* Deployment will run on any push to an application repo, not just to
  the manifests
* The code is not fully async as kubectl and git calls run from the
  event loop thread and will block the Quart server
* Error handling is quite naive
* The deployment endpoint passes back the k8s object json, and leaves it
  up to the client to parse it
* It would be more natural to use a callback webhook from git or an http
  request from a build server to let deployd know when to run a deploy,
  this is seen as not needed at this point in the project
* tests, there is None

## Further development
* environment awareness - allow different configurations per environment
* templating support with helm, kubernetes kustomize or Jinja2 powered
  manifests
* integration into build pipelines by triggering deploys and
  getting proper status by api calls
* dynamic configuration of repositories to deploy
