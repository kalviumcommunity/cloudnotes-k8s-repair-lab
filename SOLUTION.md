# Cloud Computing Module 4 — Verified solution

# Completed repair notes

Fork URL: https://github.com/srimanh/cloudnotes-k8s-repair-lab
Solution branch: fix/cloudnotes-k8s-release
Namespace: cloudnotes-mpa4-final
Cluster: Docker Desktop Kubernetes v1.34.3
Executed: 12 October 2026. No paid tools used. Application code unchanged.

## Task 1 — Startup

- Original diagnostic: CreateContainerConfigError; event: Error: configmap "cloudnotes-settings" not found. Fresh namespace already had cloudnotes-config and preloaded image; no image-pull fault occurred in this run.
- Root cause: Deployment envFrom references nonexistent ConfigMap.
- File and change: k8s/deployment.yaml, envFrom.configMapRef.name: cloudnotes-settings -> cloudnotes-config.
- Applied correction: kubectl -n cloudnotes-mpa4-final apply -f /tmp/cloudnotes-stage1.yaml (stage copy of corrected deployment with original readiness path).
- Verification: corrected pod cloudnotes-974d9479f-zzftw was 0/1 Running; kubectl exec on that exact pod returned APP_ENV=local. It was running but unready, not CreateContainerConfigError. Old ReplicaSet pod is not the corrected pod.

## Task 2 — Readiness

- Original diagnostic: corrected running pod emitted "Readiness probe failed: HTTP probe failed with statuscode: 404".
- Root cause: /readyz does not exist; documented health endpoint is /health.
- File and change: k8s/deployment.yaml, readinessProbe.httpGet.path: /readyz -> /health. Readiness retained, port 5000 unchanged.
- Verification: applied corrected Deployment; rollout status reported successful rollout; current pod reached 1/1 Running.
- Readiness explanation: Failed readiness excludes pod from ready Service backends without restart, while failed liveness can restart its container after the failure threshold.

## Task 3 — Service access

- Original diagnostic: Service selector app=cloudnotes-web, ready pod label app=cloudnotes, EndpointSlice endpoints=[].
- Root cause: Service selector does not match workload pod labels.
- File and change: k8s/service.yaml, selector.app: cloudnotes-web -> cloudnotes. Service name, port 80, targetPort 5000 and workload identity unchanged.
- Verification: applied corrected Service; EndpointSlice has ready=true backend; in-container urllib request to http://cloudnotes/health returned HTTP 200 and {"service": "cloudnotes-api", "status": "ok", "environment": "local"}.
- Traffic flow: Service DNS resolves cloudnotes to its ClusterIP; Service selector identifies matching pods and ready EndpointSlice backends; cluster routing forwards Service port 80 to application port 5000.


Actual Terminal screenshots and raw command output: solution-evidence/final-*.
Remote question repository remains unchanged.
