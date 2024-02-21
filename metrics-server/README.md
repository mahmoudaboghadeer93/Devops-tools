# Kubernetes Metrics Server

Kubernetes Metrics Server is a scalable, efficient source of container resource metrics for Kubernetes built-in autoscaling pipelines.

## Installing the Chart

Before you can install the chart, you will need to add the metrics-server repo to Helm:

```bash
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
```
# After you've installed the repo you can install the chart.
```bash
helm upgrade --install metrics-server metrics-server/metrics-server
```

[RFC](https://artifacthub.io/packages/helm/metrics-server/metrics-server)
