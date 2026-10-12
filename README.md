# cloudnotes-k8s-repair-lab

Module 4 MPA starter. Local Kubernetes repair lab. Free tools only. No paid cloud.

Repository: https://github.com/kalviumcommunity/cloudnotes-k8s-repair-lab

## Before the timer

1. Fork this repository, then clone your fork.
2. Create branch `fix/cloudnotes-k8s-release` before the timer starts.
3. Instructor prepares the local cluster, namespace, and image. Do not create a cluster, build the image, or download tools during the timer.

Work only in the namespace the instructor assigns. Commands below use `cloudnotes-mpa4`. Replace that name if the instructor gives another one. A shared cluster uses a unique namespace per student.

If a tool or the cluster itself fails, tell the instructor. That is not one of the planted faults.

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

Keep application code unchanged. Do not remove the readiness check, skip configuration injection, or replace the Service with direct pod access and call that a fix.

## Tasks

The manifests contain exactly three faults. Complete the tasks in order. An earlier fault can hide the next one. Make the smallest valid correction for each fault. Do not change anything else.

1. **Startup.** The container does not start. Use pod status, resource details, or events. Repair the manifest that causes startup to fail. Do not change application code. After the fix, confirm the container starts and receives `APP_ENV=local`. The pod may still be unready.
2. **Readiness.** The container runs but is not ready for traffic. Use cluster diagnostics and the application behaviour above. Keep the readiness check. After the fix, the Deployment rollout must finish and the current pod must be `1/1` Running. In `repair-notes.md`, explain in one sentence how a readiness failure affects Service traffic, and how that differs from a liveness failure.
3. **Service access.** The pod is ready, but requests through the Service still fail. Use Service, pod, and endpoint evidence. Keep the Service name, ports, and workload identity. After the fix, the Service must have a ready backend. From inside the cluster, request `http://cloudnotes/health` and show HTTP 200 with `status: ok`. Direct pod access or `kubectl port-forward` alone does not prove Service routing.

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

The image includes Python and `urllib`. `curl` is not installed in the container.

Check injected configuration from inside the running container:

```bash
kubectl -n cloudnotes-mpa4 exec deploy/cloudnotes -c api -- python -c "import os; print(os.environ.get('APP_ENV'))"
```

Check Service DNS only after the Service has a ready backend. Run this from inside the pod:

```bash
kubectl -n cloudnotes-mpa4 exec deploy/cloudnotes -c api -- python -c "import urllib.request; print(urllib.request.urlopen('http://cloudnotes/health').read().decode())"
```

## What to record

Fill `repair-notes.md` during the assessment. For each task, record the original diagnostic, the cause, the file and change, and the verification command plus result. Task 2 also needs the readiness explanation. Task 3 also needs the traffic-flow explanation.

Submission is one PDF: three labelled sections (cause, fix, verification), readable screenshots, corrected YAML or diffs, and the completed repair notes. Include your fork URL. A pull request is not required.
