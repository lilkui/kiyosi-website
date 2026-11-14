# kiyosi 文档

[kiyosi](https://github.com/lilkui/kiyosi) 的中文文档站，包含指南、Python API 和 Rust API。

需要 Node.js 22+、Git、Python 3.12+（含 venv 和 pip）及 Rust 1.85+（含 Cargo 和本机编译工具）。首次运行需要联网。

```sh
npm ci
npm run docs:dev
```

构建和预览：

```sh
npm run docs:build
npm run docs:preview
```

构建输出位于 `docs/.vitepress/dist/`。开发和构建时会生成 API 文档；`docs/api/` 无需手工编辑。
