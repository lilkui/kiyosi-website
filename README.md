# kiyosi documentation

A VitePress documentation site for [kiyosi](https://github.com/lilkui/kiyosi), with a custom homepage, light/dark themes, local search, introductory guides, and generated C++ and Python API references.

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

The guides are based on the upstream README and link to the original source. They cover installation, a complete Python pricing example, engine coverage, the Python module structure, and native C++ builds.

The committed API pages are generated, so the website itself still requires no Python or C++ toolchain to build.

## Regenerate the API reference

The converter uses only the Python standard library. It requires:

- Doxygen XML produced from the matching kiyosi checkout.
- A Python interpreter that can import the matching built `kiyosi` package, including its native extension.

Generate the upstream XML first. On Windows, from the kiyosi repository:

```powershell
.\generate-docs.bat
```

On Linux:

```sh
cmake --preset linux-release -DKIYOSI_BUILD_DOCS=ON
cmake --build --preset linux-release --target kiyosi-docs
```

Then run the converter with the interpreter containing the built package. For the sibling checkout used by this repository on Windows:

```powershell
..\kiyosi\.venv\Scripts\python.exe tools\generate_api_docs.py `
  --doxygen-xml ..\kiyosi\out\build\windows-release\docs\xml `
  --output docs\api
```

Use `out/build/linux-release/docs/xml` on Linux. The converter replaces `docs/api/` and fails if a Python name listed in `__all__` is missing.

Validate the converter and site:

```powershell
..\kiyosi\.venv\Scripts\python.exe tools\test_generate_api_docs.py
npm run docs:build
```
