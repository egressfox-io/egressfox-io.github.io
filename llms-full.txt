# EgressFox

Source: https://egressfox.io/

Open source Pre-alpha

## A smarter way out.

EgressFox is an open-source adaptive egress control plane for reliable external connectivity.

For DevOps and platform engineers managing changing proxy gateways. Discover endpoints, observe destination-specific health, and publish validated configurations for Mihomo and sing-box.

[View on GitHub](https://github.com/egressfox-io/egressfox) [Read the documentation](https://egressfox.io/#docs)

Core implemented. First public release in preparation.

discover observe select publish

01 / Why EgressFox

## Gateways change. Your configuration should keep up.

External integrations can depend on gateways that rotate credentials, disappear, slow down, or fail only for particular destinations. A static endpoint list cannot distinguish stale evidence from a confirmed failure. Manually replacing gateways makes decisions difficult to reproduce.

EgressFox turns endpoint descriptions and historical observations into reproducible selection decisions. Stability controls reduce unnecessary switches, and invalid candidate configurations never replace the last known good output.

### Built for external connectivity

- Third-party API access through changing gateways
- Gateway selection across multiple providers
- Explicit proxy egress for Kubernetes applications

[Product scope](https://github.com/egressfox-io/egressfox/blob/main/docs/product.md)

02 / How it works

## From endpoint lists to a validated configuration.

### Discover

Read endpoint subscriptions from Secrets or managed HTTP sources. Normalize connections and retain source provenance.
### Observe

Probe through gateways for specific destinations. Keep revision-aware history and account for the freshness of evidence.
### Select

Choose an eligible set using static, lowest-latency, or adaptive Top-N strategies, with hysteresis, cooldown, and failure replacement.
### Publish

Render engine-native configuration, validate it, and safely publish the new generation. Preserve the last known good output on failure.

A clear boundary

EgressFox decides which validated configuration should exist. Mihomo and sing-box are the data plane: they implement protocols and move traffic. Adaptive selection uses a deterministic policy over observations.

03 / Kubernetes configuration

## One pool. One explicit gateway.

### Describe the endpoints and the destination.

A `ProxyPool` reads an endpoint subscription and a probe target from Secrets. Adaptive selection maintains up to two eligible endpoints.

### Choose the engine and runtime.

An `EgressGateway` references the pool and opts into managed mode. The namespace-scoped operator creates one authenticated SOCKS5 ClusterIP Service. Applications explicitly configure that proxy.

Create the referenced Secrets through your own secret management workflow. This example is an API illustration; it requires an installed operator and a qualified runtime build.

[Explore the samples](https://github.com/egressfox-io/egressfox/tree/main/config/samples)

gateway.yaml · egressfox.io/v1alpha1

```yaml
apiVersion: egressfox.io/v1alpha1
kind: ProxyPool
metadata:
  name: external-api
spec:
  sources:
    - id: primary
      secretRef: {name: endpoint-subscription, key: nodes}
      format: URIList
  probe:
    targetSecretRef: {name: external-api-probe, key: url}
    expectedStatus: 204
  selection: {strategy: Adaptive, topN: 2}
  refreshInterval: 5m
---
apiVersion: egressfox.io/v1alpha1
kind: EgressGateway
metadata:
  name: external-api
spec:
  poolRef: {name: external-api}
  engine: SingBox
  runtime:
    managed: {}
```

04 / Project status

## Built in the open. Still pre-alpha.

API v1alpha1

Core functionality is implemented. Public releases, API stability, and production readiness are not yet guaranteed. Breaking changes may occur.

Sources & evidence

### Observe changing inventory

Secret and managed HTTP sources, bounded refresh with protected cache, destination-specific probes, and SQLite observation history.

Selection

### Keep choices reproducible

Static, lowest-latency, and adaptive Top-N selection. Named target profiles share one inventory while keeping their own evidence and selected sets.

Configuration

### Validate before publishing

Exact Mihomo 1.19.31 and sing-box-compatible 1.14.1 profiles, native validation, and last-known-good preservation.

Kubernetes

### Manage an explicit gateway

Namespace-scoped operator and Helm chart, managed or bring-your-own runtimes, scoped RBAC, and distinct published and active generations.

### Implemented milestones

M1–M6 core and BYO operator, M7 managed gateway and activation, M8 resilient HTTP refresh, M8.5 bounded protocol compatibility, and M9 target-aware selection profiles are complete for their documented scope.

M10 bounded routing policy is next, followed by M11 operational metrics and M12 explainability and P1 acceptance.

[Follow the roadmap](https://github.com/egressfox-io/egressfox/blob/main/docs/roadmap/p1.md)

### Current boundaries

- One managed replica; no operator HA or live reload.
- No transparent interception, sidecar injection, or automatic workload routing.
- No user-facing standalone product CLI/daemon or Web UI yet.
- Runtime readiness does not prove arbitrary destination traffic is healthy.

[Check engine compatibility](https://github.com/egressfox-io/egressfox/blob/main/docs/designs/engine-protocol-compatibility.md)

05 / Documentation

## Inspect the design. Evaluate the code.

- [Operator guide](https://github.com/egressfox-io/egressfox/blob/main/docs/operations/kubernetes.md): Kubernetes setup, managed gateways, and BYO operation.

- [Roadmap](https://github.com/egressfox-io/egressfox/blob/main/docs/roadmap/README.md): Completed milestones, current priorities, and later horizons.

- [Architecture decisions](https://github.com/egressfox-io/egressfox/blob/main/docs/decisions/README.md): The contracts and tradeoffs behind the control plane.

- [Threat model](https://github.com/egressfox-io/egressfox/blob/main/docs/security/threat-model.md): Trust boundaries, implemented controls, and residual risks.

- [Security policy](https://github.com/egressfox-io/egressfox/blob/main/SECURITY.md): Supported versions and confidential vulnerability reporting.

- [Release guide](https://github.com/egressfox-io/egressfox/blob/main/docs/operations/releasing.md): Artifact verification, checksums, SBOMs, and provenance.

[Browse all documentation](https://github.com/egressfox-io/egressfox/blob/main/docs/README.md)

06 / About & contact

## An independent open-source project.

### Maintained by Ruslan [@flerris](https://github.com/flerris)

EgressFox combines a Kubernetes-independent Go core with a namespace-scoped operator.

I maintain EgressFox and its technical direction, from architecture and compatibility decisions to contribution reviews, release preparation, and documentation. The code and design decisions are developed in the open under the EgressFox GitHub organization.

[Maintainer responsibilities](https://github.com/egressfox-io/egressfox/blob/main/MAINTAINERS.md)

### Get in touch

[hello@egressfox.io](mailto:hello@egressfox.io)

For reproducible bugs and feature proposals, use [GitHub Issues](https://github.com/egressfox-io/egressfox/issues). For sensitive reports, follow the [security policy](https://github.com/egressfox-io/egressfox/blob/main/SECURITY.md).

Adaptive egress routing, built in the open.

[GitHub](https://github.com/egressfox-io) [Apache-2.0](https://github.com/egressfox-io/egressfox/blob/main/LICENSE) [Third-party notices](https://github.com/egressfox-io/egressfox/blob/main/THIRD_PARTY_NOTICES.md) [hello@egressfox.io](mailto:hello@egressfox.io) [llms.txt](https://egressfox.io/llms.txt) [llms-full.txt](https://egressfox.io/llms-full.txt)
