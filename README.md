# kiyosi 文档

这是 [kiyosi](https://github.com/lilkui/kiyosi) 的 VitePress 文档站，提供中文指南、Python API 参考，以及同站托管的原生 Rust API 文档。保留现有首页、明暗主题和本地搜索。API 参考可保留英文，其余页面与界面使用中文。

当前文档对应 **kiyosi 0.14.0**，上游提交为 `748942203c99ffb5f011dbdcd06312d6b5f4a06c`。版本、完整提交和仓库地址统一记录在 [`upstream.json`](./upstream.json)。

## 构建要求

- Node.js 22+、npm、Git。
- Python 3.11+，含 `venv` 和 pip；Linux 命令为 `python3`，Windows 需要 `py -3` 启动器。
- Rust 1.85+、Cargo 和本机编译／链接工具；Windows 使用 MSVC 工具链及 Visual Studio Build Tools。
- 首次构建需要联网获取上游源码、Python 构建工具及 Cargo 依赖。

Debian / Ubuntu 若提示 `ensurepip is not available`，需安装与解释器匹配的 `python3-venv` 软件包。也可以用已经包含 venv/pip 的 Python 执行 `python tools/prepare_api_docs.py`。

VitePress 1 通过 Vite 版本覆盖使用已修补的构建依赖，升级 VitePress 时需重新评估该配置。

## 本地开发

```sh
npm ci
npm run docs:dev
```

首次启动会先生成两种语言的 API，再启动 VitePress。之后的 Markdown 编辑会热更新。若只修改指南和样式，可在已经成功生成 API 后使用 `npx vitepress dev docs` 直接启动。

指南位于 `docs/guide/`，配置位于 `docs/.vitepress/config.ts`，主题位于 `docs/.vitepress/theme/`。Rust 构建指南位于 `docs/rust/building.md`。

## 生产构建

```sh
npm run docs:test
npm run docs:build
npm run docs:preview
```

`docs:build` 完成以下步骤：

1. 在 `.cache/kiyosi/` 获取并检出 `upstream.json` 指定的完整提交；拒绝覆盖缓存源码中的本地修改。
2. 核对 Cargo workspace 版本，在 `.cache/venv/` 中从该源码构建并安装 Python 扩展，使用上游 Cargo 锁文件。
3. 执行 `cargo doc -p kiyosi-core --no-deps --locked`，将 rustdoc 警告视为错误。
4. 核对 Python 运行时版本，再按公开导出、签名、属性和文档字符串生成 `docs/api/`。
5. 将完整 rustdoc 目录复制到 `docs/public/api/rust/`，再运行 VitePress，检查 Markdown 内部链接。

发布目录为 **`docs/.vitepress/dist/`**，其中 Rust API 入口为 `api/rust/kiyosi_core/index.html`。发布时必须包含整个目录，以保留 rustdoc 的搜索、静态资源与源码链接。托管服务需支持 `.html` 文件，无需 URL 重写。构建完成后的预览与静态托管无需 Python 或 Rust。

Python API Markdown 提交到仓库，便于审查 API 变化；rustdoc HTML 和构建缓存不提交。缓存加快重复构建，每次仍从固定源码安装扩展，不复用外部环境中可能过期的 kiyosi。此流程固定源码版本，不承诺不同工具链下产物逐字节相同。

Rust API 使用原生 rustdoc 界面及独立搜索；VitePress 本地搜索包含中文指南和 Python API。站点没有配置托管账户或自动部署。

## 部署到子目录

默认基础路径为 `/`。部署到子目录时，设置首尾带斜杠的 `DOCS_BASE`：

```sh
DOCS_BASE=/kiyosi-website/ npm run docs:build
```

PowerShell：

```powershell
$env:DOCS_BASE = '/kiyosi-website/'
npm run docs:build
```

rustdoc 内部使用相对路径，随整个目录发布即可。原有 `/zh/` 的首页、指南和 Python 概览仍生成跳转；`/cpp/building.html` 与 `/zh/cpp/building.html` 跳转至 Rust 构建指南。跳转保留查询参数和锚点。

## 更新文档版本

1. 修改 `upstream.json` 的版本和完整提交，确保二者一致。
2. 同步修订首页、安装、指南、Rust 示例和本文档中的版本、接口及固定源码链接。
3. 执行 `npm run docs:generate`、`npm run docs:test` 与 `npm run docs:build`，审查生成的 Python API 差异，并运行指南示例。

单独生成 API：

```sh
npm run docs:generate
```

生成器按 `__all__` 收集导出；没有 `__all__` 时收集公开名称，保留 `typing.Literal` 类型别名。PyO3 构造签名、原生属性及交互示例均纳入参考。生成失败或版本不匹配时，保留原有 Python 参考；非空目录必须带 `.kiyosi-api-generated` 标记才允许替换，勿在生成目录中编写手工页面。

清理构建缓存时可以删除 `.cache/` 与 `docs/public/api/rust/`；下次生成会重新下载和构建。
