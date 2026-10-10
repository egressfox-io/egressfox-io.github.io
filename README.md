# EgressFox website

The source for [egressfox.io](https://egressfox.io), the official website of [EgressFox](https://github.com/egressfox-io/egressfox).

EgressFox is an open-source adaptive egress control plane. The website explains the problem, the discover → observe → select → publish workflow, Kubernetes manifests, current capabilities and boundaries, documentation, and maintainer contact. Product code, technical discussions, and release information live in the [main repository](https://github.com/egressfox-io/egressfox).

## Stack

The site uses plain HTML, CSS, and SVG. It has no build step, JavaScript runtime, package manager, or third-party frontend dependencies. GitHub Pages serves the files in this repository directly.

## Run locally

From the repository root, start a static file server:

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

Open **http://127.0.0.1:8080/** in your browser. Stop the server with `Ctrl+C`.

Edits to `index.html`, `styles.css`, or the files in `assets/` are reflected after refreshing the page; there is no compilation step.

## Repository layout

| Path | Purpose |
| --- | --- |
| `index.html` | Page content, inline SVG artwork, and social metadata |
| `styles.css` | Layout, visual styles, and responsive breakpoints |
| `assets/fox-mark.svg` | Site favicon |
| `assets/egressfox.png` | Social preview image referenced by the Open Graph metadata |
| `CNAME` | Custom domain for GitHub Pages (`egressfox.io`) |
| `robots.txt` | Crawler access and sitemap location |
| `sitemap.xml` | Canonical public page for discovery |
| `llms.txt` | Short machine-readable project summary and document index |
| `llms-full.txt` | Complete public homepage text, including YAML, in Markdown |
| `index.html.md` | Markdown alternative to the homepage |
| `scripts/generate-machine-content.py` | Standard-library Python exporter and freshness check |
| `LICENSE` | Apache License 2.0 |

## Publishing

After editing the homepage, refresh its machine-readable exports and check that they match:

```bash
python3 scripts/generate-machine-content.py
python3 scripts/generate-machine-content.py --check
```

The generated files are committed static assets; visitors need no JavaScript or generation service. The HTML advertises the Markdown alternative and `llms.txt` with link relations, and the footer links to both LLM files. JSON-LD describes the website, source repository, license, and maintainer using only public project facts. These formats aid discovery and interpretation; they do not establish eligibility for any startup program.

The repository is intended to be published with **GitHub Pages** using the `main` branch and its root directory (`/`). The custom domain is declared in `CNAME`; its DNS configuration and HTTPS settings are managed separately in GitHub Pages and the domain's DNS provider.

Once Pages is configured, updates to the published branch are deployed by GitHub Pages. A local preview does not change the live website: commit and push the intended changes to publish them.

## Contributing

Keep capability and milestone statements aligned with the main repository's README, P1 roadmap, and authoritative compatibility matrix. The displayed YAML is the README's Kubernetes example; it assumes the operator, runtime build, and referenced Secrets are configured separately. Planned features must not be presented as available, and pre-alpha status must remain visible until the project changes it.

The site lists `hello@egressfox.io` as the intended contact address. Mailbox provisioning is managed separately and must be completed before relying on that address for correspondence.

Issues and pull requests for small website fixes are welcome. Please keep the landing page lightweight, responsive, accessible, and framework-free. For EgressFox features or bugs, use the [main project repository](https://github.com/egressfox-io/egressfox) instead.

## License

This repository is licensed under the [Apache License 2.0](LICENSE).
