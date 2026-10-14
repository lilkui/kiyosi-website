import { access, mkdir, writeFile } from 'node:fs/promises'
import { dirname, join, posix } from 'node:path'
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'kiyosi',
  description: '基于 C++23 的衍生品定价库，提供 Python 接口，支持普通期权、奇异期权和结构化产品。',
  lang: 'zh-CN',
  base: process.env.DOCS_BASE || '/',
  async buildEnd({ outDir }) {
    const legacyPages = [
      'index',
      'guide/introduction',
      'guide/installation',
      'guide/first-price',
      'guide/engines',
      'reference/python',
      'cpp/building',
    ]
    for (const page of legacyPages) {
      const file = `${page}.html`
      await access(join(outDir, file))
      const target = posix.relative(posix.dirname(`zh/${file}`), file)
      const output = join(outDir, 'zh', file)
      await mkdir(dirname(output), { recursive: true })
      await writeFile(output, `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>页面已迁移</title>
<link rel="canonical" href="${target}">
<script>location.replace(${JSON.stringify(target)} + location.search + location.hash)</script>
<noscript><meta http-equiv="refresh" content="0;url=${target}"></noscript>
</head><body><p>页面已迁移，请<a href="${target}">前往新页面</a>。</p></body></html>`, 'utf8')
    }
  },
  appearance: true,
  head: [['link', { rel: 'icon', href: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"%3E%3Crect width="32" height="32" rx="6" fill="%2308776b"/%3E%3Ctext x="8" y="25" fill="%23fcfdfc" font-family="sans-serif" font-weight="700" font-size="28"%3Ek%3C/text%3E%3C/svg%3E' }]],
  markdown: {
    theme: { light: 'github-light-high-contrast', dark: 'github-dark-high-contrast' },
    codeCopyButtonTitle: '复制代码',
    container: {
      infoLabel: '说明',
      noteLabel: '注意',
      tipLabel: '提示',
      warningLabel: '警告',
      dangerLabel: '危险',
      detailsLabel: '详情',
      importantLabel: '重要',
      cautionLabel: '小心',
    },
  },
  themeConfig: {
    siteTitle: 'kiyosi',
    nav: [
      { text: '使用指南', link: '/guide/introduction', activeMatch: '/guide/' },
      { text: 'API 参考', link: '/api/', activeMatch: '/api/' },
    ],
    sidebar: [
      {
        text: '快速上手',
        items: [
          { text: '简介', link: '/guide/introduction' },
          { text: '安装', link: '/guide/installation' },
          { text: '首次定价', link: '/guide/first-price' },
        ],
      },
      {
        text: '深入了解',
        items: [
          { text: '定价引擎', link: '/guide/engines' },
          { text: 'Python API 概览', link: '/reference/python' },
          { text: '构建 C++ 库', link: '/cpp/building' },
        ],
      },
      {
        text: 'API 参考',
        items: [
          { text: '概览', link: '/api/' },
          { text: 'C++ API', link: '/api/cpp/' },
          { text: 'Python API', link: '/api/python/' },
        ],
      },
    ],
    search: {
      provider: 'local',
      options: { translations: {
        button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
        modal: {
          noResultsText: '未找到相关结果',
          resetButtonTitle: '清空搜索',
          backButtonTitle: '关闭搜索',
          displayDetails: '显示详细列表',
          footer: {
            selectText: '选择',
            selectKeyAriaLabel: '回车键',
            navigateText: '切换',
            navigateUpKeyAriaLabel: '向上方向键',
            navigateDownKeyAriaLabel: '向下方向键',
            closeText: '关闭',
            closeKeyAriaLabel: '退出键',
          },
        },
      } },
    },
    socialLinks: [{ icon: 'github', link: 'https://github.com/lilkui/kiyosi' }],
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一页', next: '下一页' },
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '返回顶部',
    skipToContentLabel: '跳转到正文',
    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    notFound: {
      title: '页面未找到',
      quote: '页面可能已移动或不存在，请返回首页或搜索文档。',
      linkLabel: '返回首页',
      linkText: '返回首页',
    },
    footer: {
      message: 'kiyosi · 开源衍生品定价库',
      copyright: '<a href="https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt">本项目采用 MIT 许可证</a>',
    },
  },
})
