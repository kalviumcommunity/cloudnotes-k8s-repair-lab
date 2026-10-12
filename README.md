# cloudnotes-k8s-repair-lab

Module 4 MPA starter. Small local Kubernetes repair lab. Free tools only. No paid cloud.

Proposed publication URL: https://github.com/kalviumcommunity/cloudnotes-k8s-repair-lab

## Before the timer

1. Fork this repository, then clone your fork.
2. Create branch `fix/cloudnotes-k8s-release` before the timer starts.
3. Instructor prepares the local cluster, namespace, and image. Do not create a cluster during the timer.

Work in the namespace the instructor assigns. Shared clusters use a unique namespace per student. Commands below use `cloudnotes-mpa4`. Replace that name if the instructor gives another one.

## What is already correct

| Item | Value |
|---|---|
| Image | `cloudnotes-api:mpa4` (`imagePullPolicy: Never`) |
| Container listen port | `5000` |
| Health path | `GET /health` |
| ConfigMap | `cloudnotes-config` |
| ConfigMap key | `APP_ENV` |
| Service | `cloudnotes`, ClusterIP, port `80` → container `5000` |
| Deployment | `cloudnotes`, container name `api` |

`GET /health` returns HTTP 200 and JSON: `service` is `cloudnotes-api`, `status` is `ok`, `environment` comes from `APP_ENV`. Unknown paths return HTTP 404.

The process runs as a non-root user. No real secrets are in this repository. ConfigMap data is a non-secret environment label only.

## Tasks

Exactly three manifest faults. Fix them in order. Task 1 hides Task 2 until the container can start. Do not add other changes. Do not treat setup or tool failures as extra planted bugs — report those to the instructor.

1. Deployment cannot start. Diagnostics name a missing ConfigMap. Fix only the ConfigMap reference. Do not change the app or the ConfigMap object.
2. After Task 1, the container runs but the pod stays `0/1` Ready. A readiness check gets HTTP 404. Correct only the probe path. Do not delete the probe.
3. After Task 2, the pod is `1/1` Ready but the Service has no ready backend. Correct only the Service selector.

## Commands you may use

```bash
kubectl config current-context
kubectl -n cloudnotes-mpa4 get pods,svc,configmap,endpointslices
kubectl -n cloudnotes-mpa4 describe pods -l app=cloudnotes
kubectl -n cloudnotes-mpa4 describe svc cloudnotes
kubectl -n cloudnotes-mpa4 get events --sort-by=.lastTimestamp
kubectl -n cloudnotes-mpa4 apply -f k8s/
kubectl -n cloudnotes-mpa4 rollout status deployment/cloudnotes
kubectl -n cloudnotes-mpa4 get endpointslices -l kubernetes.io/service-name=cloudnotes -o yaml
kubectl -n cloudnotes-mpa4 exec deploy/cloudnotes -c api -- python -c "import os,urllib.request; print(os.environ.get('APP_ENV')); print(urllib.request.urlopen('http://cloudnotes/health').read().decode())"
```

The image includes Python and `urllib`. Do not expect `curl` inside the container.

## Submission notes

Record cause, fix, and result in `repair-notes.md`. Stay inside the three faults. No fixed screenshot count. Scope is these manifests only.
