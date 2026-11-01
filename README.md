# kiyosi 文档

这是 [kiyosi](https://github.com/lilkui/kiyosi) 的 VitePress 文档站，提供中文指南、Python API 参考和原生 Rust API 文档。

文档对应的上游版本和源码提交见 [`upstream.json`](./upstream.json)。

## 构建要求

- Node.js 22+、npm、Git。
- uv；项目通过 `uv run` 使用 Python 3.11+，缺少解释器时会自动下载。
- Rust 1.85+、Cargo 和本机编译／链接工具；Windows 使用 MSVC 工具链及 Visual Studio Build Tools。

首次构建需要联网下载 Python、源码和依赖。

## 本地开发

```sh
npm ci
npm run docs:dev
```

启动时会先生成 Python 和 Rust API。API 已生成后，可用 `npx vitepress dev docs` 跳过生成步骤。

指南位于 [`docs/guide/`](./docs/guide/)，站点配置和主题位于 [`docs/.vitepress/`](./docs/.vitepress/)。

## 构建与部署

```sh
npm run docs:test
npm run docs:build
npm run docs:preview
```

构建会重新生成 API。将 **`docs/.vitepress/dist/` 整个目录**发布到静态托管服务，包含 Rust API 的资源和源码链接。托管服务需支持 `.html` 文件，无需 URL 重写；预览与托管无需 Python 或 Rust。

默认部署在 `/`。部署到子目录时，设置首尾带斜杠的 `DOCS_BASE`：

```sh
DOCS_BASE=/kiyosi-website/ npm run docs:build
```

PowerShell：

```powershell
$env:DOCS_BASE = '/kiyosi-website/'
npm run docs:build
```

## 更新文档版本

1. 修改 `upstream.json` 的版本和完整提交，确保二者一致。
2. 同步更新首页、指南和 Rust 示例中的版本、接口及源码链接。
3. 执行 `npm run docs:build` 和 `npm run docs:test`，检查生成的 Python API，并运行指南示例。

单独生成 API：`npm run docs:generate`。

`docs/api/` 由工具生成，请勿手工编辑；生成的 Python API Markdown、rustdoc HTML 和构建缓存均不提交到仓库。
