import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'kiyosi',
  description: 'C++23 derivatives pricing with Python bindings. Learn to price vanilla options, exotic instruments, and structured products.',
  lang: 'en-US',
  base: process.env.DOCS_BASE || '/',
  appearance: true,
  head: [['link', { rel: 'icon', href: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"%3E%3Crect width="32" height="32" rx="6" fill="%2308776b"/%3E%3Ctext x="8" y="25" fill="%23fcfdfc" font-family="sans-serif" font-weight="700" font-size="28"%3Ek%3C/text%3E%3C/svg%3E' }]],
  markdown: {
    theme: { light: 'github-light-high-contrast', dark: 'github-dark-high-contrast' },
  },
  themeConfig: {
    siteTitle: 'kiyosi',
    nav: [
      { text: 'Guide', link: '/guide/introduction', activeMatch: '/guide/' },
      { text: 'API reference', link: '/api/', activeMatch: '/api/' },
      { text: 'C++', link: '/cpp/building', activeMatch: '/cpp/' },
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
          { text: 'Documentation coverage', link: '/api/coverage' },
        ],
      },
    ],
    search: { provider: 'local' },
    socialLinks: [{ icon: 'github', link: 'https://github.com/lilkui/kiyosi' }],
    outline: { level: [2, 3] },
    footer: {
      message: 'kiyosi · Open-source derivatives pricing',
      copyright: '<a href="https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt">Project released under the MIT License</a>',
    },
  },
})
