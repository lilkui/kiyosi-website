# kiyosi 文档

[kiyosi](https://github.com/lilkui/kiyosi) 的中文文档站，包含指南、Python API 和 Rust API。

阅读文档：[使用指南](docs/guide/introduction.md)、[Python API 概览](docs/reference/python.md)、[Rust 核心](docs/rust/building.md)。`upstream.json` 固定文档对应的版本和源码提交。

## 本地开发

本地开发需要 Node.js 22+、Git、Python 3.12+（含 venv 和 pip）及 Rust 1.85+（含 Cargo 和本机编译工具）。首次运行会联网下载依赖与源码。

```sh
npm ci
npm run docs:dev
```

## 构建和预览

```sh
npm run docs:build
npm run docs:preview
```

构建输出位于 `docs/.vitepress/dist/`。开发和构建命令会根据固定提交的源码生成 Python API 页面与 Rust API 静态资源，分别写入 `docs/api/` 和 `docs/public/api/rust/`。

API 页面内容来自源码中的文档字符串和注释。手写中文指南与报告位于 `docs/guide/`、`docs/reference/`、`docs/rust/` 和 `docs/reports/`。
