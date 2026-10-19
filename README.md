# kiyosi 文档

这是 [kiyosi](https://github.com/lilkui/kiyosi) 的 VitePress 文档站，包含自定义首页、明暗主题、本地搜索、入门指南，以及自动生成的 C++ / Python API 参考文档。

除自动生成的 API 参考文档可保留英文外，其余文档和站点界面均使用中文。中文页面从站点根路径访问。代码、命令、标识符和专有名词保留原文。

## 本地开发

需要 Node.js 22+ 和 npm。

通过覆盖 Vite 版本，VitePress 1 使用的是已修补的构建工具和开发服务器依赖。升级 VitePress 时，需重新评估这项配置。

```sh
npm ci
npm run docs:dev
```

启动后，打开终端显示的本地地址。Markdown 文档位于 `docs/`，导航配置位于 `docs/.vitepress/config.ts`，样式位于 `docs/.vitepress/theme/style.css`。

## 生产构建

```sh
npm run docs:build
npm run docs:preview
```

构建时会检查 Markdown 内部链接。构建完成后，将 `docs/.vitepress/dist/` 发布到静态托管服务。目前尚未配置托管账户或部署流程。

构建时会为原有的 7 个 `/zh/` 页面生成跳转，并保留查询参数和锚点。旧书签仍可访问对应的中文页面。

默认基础路径为 `/`。部署到子目录时，请在构建前设置 `DOCS_BASE`，路径首尾都需加斜杠。以 GitHub Pages 的 `/kiyosi-website/` 为例：

```sh
DOCS_BASE=/kiyosi-website/ npm run docs:build
```

PowerShell：

```powershell
$env:DOCS_BASE = '/kiyosi-website/'
npm run docs:build
```

托管服务需支持 `.html` 文件，无需 URL 重写。

## 内容维护

指南基于 kiyosi README 编写，并附有源码仓库链接，内容包括安装、完整的 Python 定价示例、引擎支持范围、Python 模块结构和原生 C++ 构建。

自动生成的 API 页面已提交到仓库，因此构建网站无需 Python 或 C++ 工具链。

当前文档对应 kiyosi **0.11.0**（源码提交 `541546c`），包含 51 个公开 C++ 头文件页面和 4 个 Python 模块页面。指南中的选择参数使用字符串；`price()` 直接返回数值，`price_with_greeks()` 则需显式指定要计算的 Greeks。数值引擎在构造时验证配置，市场和产品历史更新使用返回副本的 `replace()`。

## 重新生成 API 参考文档

转换工具本身仅使用 Python 标准库。运行前需准备：

- 对应版本 kiyosi 源码生成的 Doxygen XML。
- Python 解释器，须能导入对应版本已构建的 `kiyosi` 包及其原生扩展。

先安装 Doxygen，再在 kiyosi 仓库中配置文档构建。以下命令适用于 Windows 和 Linux；Windows 下请先打开 Visual Studio Developer PowerShell：

```sh
cmake -S . -B build/docs -DBUILD_TESTING=OFF -DKIYOSI_BUILD_DOCS=ON
cmake --build build/docs --target kiyosi-doxygen
```

构建文档目标无需编译核心库，也不需要 Graphviz 或 Python。CMake 配置需要 oneTBB 2023.1+，未安装时会自动下载。XML 入口为 `build/docs/docs/xml/index.xml`，也可使用其他启用了 `KIYOSI_BUILD_DOCS` 的构建目录。

确认 Python 环境已安装同一版本的 kiyosi，并用 `import kiyosi; print(kiyosi.__version__)` 检查版本是否与 XML 一致，然后运行转换工具。以下 Windows 示例假定 kiyosi 位于本仓库的同级目录：

```powershell
..\kiyosi\.venv\Scripts\python.exe tools\generate_api_docs.py `
  --doxygen-xml ..\kiyosi\build\docs\docs\xml `
  --output docs\api
```

Linux 可使用对应虚拟环境的 `bin/python`，XML 路径相同。

转换会替换带生成标记的 `docs/api/`。若 Python 模块声明了 `__all__`，工具按该列表收集导出对象；否则收集名称不以下划线开头的公开对象。`typing.Literal` 保留为类型别名。若显式导出的名称缺失，或 XML 中未找到公开头文件，转换会失败。C++ 参考不包含 `detail/` 实现头文件。

验证转换工具和网站：

```powershell
..\kiyosi\.venv\Scripts\python.exe tools\test_generate_api_docs.py
npm run docs:build
```
