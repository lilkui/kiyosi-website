import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'kiyosi',
  description: 'C++23 derivatives pricing with Python bindings. Learn to price vanilla options, exotic instruments, and structured products.',
  lang: 'en-US',
  locales: {
    root: { label: 'English', lang: 'en-US' },
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      description: '基于 C++23 的衍生品定价库，提供 Python 接口，支持普通期权、奇异期权和结构化产品。',
      themeConfig: {
        nav: [
          { text: '使用指南', link: '/zh/guide/introduction', activeMatch: '/zh/guide/' },
          { text: 'API 参考（英文）', link: '/api/', activeMatch: '/api/' },
        ],
        sidebar: [
          { text: '快速上手', items: [
            { text: '简介', link: '/zh/guide/introduction' },
            { text: '安装', link: '/zh/guide/installation' },
            { text: '首次定价', link: '/zh/guide/first-price' },
          ] },
          { text: '深入了解', items: [
            { text: '定价引擎', link: '/zh/guide/engines' },
            { text: 'Python API 概览', link: '/zh/reference/python' },
            { text: '构建 C++ 库', link: '/zh/cpp/building' },
          ] },
          { text: 'API 参考（英文）', items: [
            { text: '概览', link: '/api/' },
            { text: 'C++ API', link: '/api/cpp/' },
            { text: 'Python API', link: '/api/python/' },
          ] },
        ],
        outline: { level: [2, 3], label: '本页目录' },
        docFooter: { prev: '上一页', next: '下一页' },
        langMenuLabel: '切换语言',
        sidebarMenuLabel: '菜单',
        returnToTopLabel: '返回顶部',
        skipToContentLabel: '跳转到正文',
        darkModeSwitchLabel: '外观',
        lightModeSwitchTitle: '切换到浅色模式',
        darkModeSwitchTitle: '切换到深色模式',
        footer: {
          message: 'kiyosi · 开源衍生品定价库',
          copyright: '<a href="https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt">本项目采用 MIT 许可证</a>',
        },
      },
    },
  },
  base: process.env.DOCS_BASE || '/',
  appearance: true,
  head: [['link', { rel: 'icon', href: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"%3E%3Crect width="32" height="32" rx="6" fill="%2308776b"/%3E%3Ctext x="8" y="25" fill="%23fcfdfc" font-family="sans-serif" font-weight="700" font-size="28"%3Ek%3C/text%3E%3C/svg%3E' }]],
  markdown: {
    theme: { light: 'github-light-high-contrast', dark: 'github-dark-high-contrast' },
  },
  themeConfig: {
    siteTitle: 'kiyosi',
    // Switch to locale homepages because generated API pages are English-only.
    i18nRouting: false,
    nav: [
      { text: 'Guide', link: '/guide/introduction', activeMatch: '/guide/' },
      { text: 'API reference', link: '/api/', activeMatch: '/api/' },
    ],
    sidebar: [
      {
        text: 'Get started',
        items: [
          { text: 'Introduction', link: '/guide/introduction' },
          { text: 'Installation', link: '/guide/installation' },
          { text: 'Your first price', link: '/guide/first-price' },
        ],
      },
      {
        text: 'Explore kiyosi',
        items: [
          { text: 'Pricing engines', link: '/guide/engines' },
          { text: 'Python API overview', link: '/reference/python' },
          { text: 'Build the C++ library', link: '/cpp/building' },
        ],
      },
      {
        text: 'API reference',
        items: [
          { text: 'Overview', link: '/api/' },
          { text: 'C++ API', link: '/api/cpp/' },
          { text: 'Python API', link: '/api/python/' },
        ],
      },
    ],
    search: {
      provider: 'local',
      options: { locales: { zh: { translations: {
        button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
        modal: {
          noResultsText: '未找到相关结果',
          resetButtonTitle: '清空搜索',
          backButtonTitle: '关闭搜索',
          displayDetails: '显示详细列表',
          footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
        },
      } } } },
    },
    socialLinks: [{ icon: 'github', link: 'https://github.com/lilkui/kiyosi' }],
    outline: { level: [2, 3] },
    footer: {
      message: 'kiyosi · Open-source derivatives pricing',
      copyright: '<a href="https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt">Project released under the MIT License</a>',
    },
  },
})
