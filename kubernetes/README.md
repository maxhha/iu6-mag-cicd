```bash
minikube addons enable ingress
minikube kubectl -- kustomize | minikube kubectl -- apply -f -
```

Open http://localhost/users. User:Password: bmstu:123qweasd

On WSL2:

```bash
minikube service ingress-nginx-controller -n ingress-nginx
```

Open `http://127.0.0.1:{{port from output}}/users`. User:Password: bmstu:123qweasd
