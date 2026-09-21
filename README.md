# EgressFox website

The source for [egressfox.io](https://egressfox.io), the official website of [EgressFox](https://github.com/egressfox-io/egressfox).

EgressFox is an open-source adaptive egress routing project. This website is a small landing page while the first public release is in development; product code, technical discussions, and release information live in the [main repository](https://github.com/egressfox-io/egressfox).

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
| `LICENSE` | Apache License 2.0 |

## Publishing

The repository is intended to be published with **GitHub Pages** using the `main` branch and its root directory (`/`). The custom domain is declared in `CNAME`; its DNS configuration and HTTPS settings are managed separately in GitHub Pages and the domain's DNS provider.

Once Pages is configured, updates to the published branch are deployed by GitHub Pages. A local preview does not change the live website: commit and push the intended changes to publish them.

## Contributing

Issues and pull requests for small website fixes are welcome. Please keep the landing page lightweight, responsive, accessible, and framework-free. For EgressFox features or bugs, use the [main project repository](https://github.com/egressfox-io/egressfox) instead.

## License

This repository is licensed under the [Apache License 2.0](LICENSE).
