# cloudnotes-k8s-repair-lab

Module 4 MPA starter. Local Kubernetes repair lab.

Repository: https://github.com/kalviumcommunity/cloudnotes-k8s-repair-lab

## Cost: ₹0 / $0

This continuous assessment uses **no paid tools** and **no paid cloud**.

Allowed: the free local cluster the instructor already prepared (kind, minikube, k3s, or Docker Desktop Kubernetes), `kubectl`, a text editor, and Python already inside the supplied image.

Not used and not required: AWS, Azure, GCP, any other cloud account, paid Kubernetes service, registry login, API keys, real credentials, Ingress controller, CI/CD, or a credit card. Do not open a cloud console to “fix” this lab. If a local tool fails, tell the instructor. That is not one of the planted faults.

## Before the timer

1. Fork this repository, then clone your fork.
2. Create branch `fix/cloudnotes-k8s-release` before the timer starts.
3. The instructor prepares the cluster, namespace, and image. Do not create a cluster, build an image, or install tools during the timer.

Work only in the namespace the instructor assigns. Commands below use `cloudnotes-mpa4`. Replace that name if you are given another one.

## What the release is supposed to do

| Item | Intended value |
|---|---|
| Image already loaded in the cluster | `cloudnotes-api:mpa4` |
| Container listen address | `0.0.0.0:5000` |
| Health check | `GET /health` |
| ConfigMap | `cloudnotes-config` |
| ConfigMap key | `APP_ENV` (intended value `local`) |
| Deployment | `cloudnotes`, one replica, container name `api` |
| Service | `cloudnotes`, ClusterIP, port `80` → container port `5000` |

`GET /health` returns HTTP 200 and JSON. `service` is `cloudnotes-api`. `status` is `ok`. `environment` comes from `APP_ENV`. Any other path returns HTTP 404, not HTTP 200.

The process runs as a non-root user. This repository has no real secrets. ConfigMap data is only a non-secret environment label.

Keep application code unchanged. Do not delete the readiness check. Do not skip configuration injection. Do not replace Service access with direct pod IP access or `kubectl port-forward` and call that a fix. Do not change `imagePullPolicy`. `ImagePullBackOff` is a setup problem — report it.

## Tasks

The manifests contain exactly three faults. Do them in order. An earlier fault can hide the next one. Smallest valid correction only.

### Task 1 — Startup (6 marks)

The container does not start.

1. Capture pod status, `describe`, or events that name the startup problem.
2. Repair the responsible manifest. Do not change application code or the ConfigMap object.
3. Apply the change. Show the container is running and that `APP_ENV` is `local`. The pod may still be `0/1` Ready. That is the next task, not a failed fix.

PDF: original diagnostic, corrected YAML or diff, runtime proof of `APP_ENV=local`.

### Task 2 — Readiness (6 marks)

The container runs but is not ready for traffic.

1. Capture the readiness failure from cluster diagnostics. Compare it with the health behaviour above.
2. Smallest manifest correction. Keep the readiness check. Apply it.
3. Show `rollout status` success and the current pod `1/1` Running.
4. One sentence: how a failed readiness check affects Service traffic, and how that differs from a failed liveness check.

PDF: diagnostic, corrected YAML or diff, rollout plus `1/1`, and that sentence.

### Task 3 — Service access (6 marks)

The pod is ready. Requests through the Service still fail.

1. Capture Service, pod label, and endpoint (or EndpointSlice) evidence.
2. Repair the responsible manifest. Keep the Service name, ports, and workload identity. Apply it.
3. Show a ready backend on the Service.
4. From inside the cluster, request `http://cloudnotes/health`. Show HTTP 200 and a body with `status` `ok`.

PDF: communication evidence, corrected YAML or diff, ready endpoint, Service-DNS response. Pod IP or port-forward alone does not count.

## Commands you may use

```bash
kubectl config current-context
kubectl -n cloudnotes-mpa4 get pods,svc,configmap,endpoints,endpointslices
kubectl -n cloudnotes-mpa4 describe pods -l app=cloudnotes
kubectl -n cloudnotes-mpa4 describe svc cloudnotes
kubectl -n cloudnotes-mpa4 get endpoints cloudnotes -o yaml
kubectl -n cloudnotes-mpa4 get events --sort-by=.lastTimestamp
kubectl -n cloudnotes-mpa4 apply -f k8s/
kubectl -n cloudnotes-mpa4 rollout status deployment/cloudnotes
kubectl -n cloudnotes-mpa4 get endpointslices -l kubernetes.io/service-name=cloudnotes -o yaml
```

`curl` is not in the container. Python and `urllib` are.

Task 1 — configuration, after the container is running:

```bash
kubectl -n cloudnotes-mpa4 exec deploy/cloudnotes -c api -- python -c "import os; print(os.environ.get('APP_ENV'))"
```

Task 3 — Service DNS, only after a ready backend exists. Prints status code and body:

```bash
kubectl -n cloudnotes-mpa4 exec deploy/cloudnotes -c api -- python -c "import urllib.request; r=urllib.request.urlopen('http://cloudnotes/health'); print(r.status); print(r.read().decode())"
```

## Submission

One PDF. Three labelled sections: cause, fix, verification. Readable screenshots. Corrected YAML or diffs. Completed `repair-notes.md` (text or a readable capture). Fork URL. No pull request required. No paid-tool screenshots.
