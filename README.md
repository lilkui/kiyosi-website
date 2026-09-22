# kiyosi documentation

A VitePress documentation site for [kiyosi](https://github.com/lilkui/kiyosi), with a custom homepage, light/dark themes, local search, and introductory Python and C++ guides.

## Local development

Use Node.js 22+ and npm.

The Vite override keeps VitePress 1 on a patched build/dev-server dependency. Revisit it when upgrading VitePress.

```sh
npm ci
npm run docs:dev
```

Open the local URL printed by VitePress. Edit Markdown in `docs/`; navigation lives in `docs/.vitepress/config.ts` and styling in `docs/.vitepress/theme/style.css`.

## Production build

```sh
npm run docs:build
npm run docs:preview
```

Publish `docs/.vitepress/dist/` to a static host. The build checks internal Markdown links. No hosting account or deployment is configured.

The default base path is `/`. For a subdirectory deployment, set `DOCS_BASE` before building, including leading and trailing slashes. For example, for GitHub Pages at `/kiyosi-website/`:

```sh
DOCS_BASE=/kiyosi-website/ npm run docs:build
```

In PowerShell:

```powershell
$env:DOCS_BASE = '/kiyosi-website/'
npm run docs:build
```

The host must serve `.html` files; URL rewriting is not required.

## Content maintenance

The guides are based on the upstream README and link to the original source. They cover installation, a complete Python pricing example, engine coverage, the Python module structure, and native C++ builds. The API overview is intentionally not an exhaustive generated reference.

When kiyosi changes, review examples and installation requirements against upstream, then run the site build. The website requires no Python or C++ toolchain to build.
