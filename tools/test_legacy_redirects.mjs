import assert from 'node:assert/strict'
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import test from 'node:test'
import { runInNewContext } from 'node:vm'
import { resolveConfig } from 'vitepress'

test('legacy URLs reach current guides and preserve queries and anchors', async (t) => {
  const outDir = await mkdtemp(join(tmpdir(), 'kiyosi-redirects-'))
  t.after(() => rm(outDir, { recursive: true, force: true }))
  const pages = [
    ['zh/index.html', 'index.html'],
    ['zh/guide/introduction.html', 'guide/introduction.html'],
    ['zh/guide/installation.html', 'guide/installation.html'],
    ['zh/guide/first-price.html', 'guide/first-price.html'],
    ['zh/guide/engines.html', 'guide/engines.html'],
    ['zh/reference/python.html', 'reference/python.html'],
    ['cpp/building.html', 'rust/building.html'],
    ['zh/cpp/building.html', 'rust/building.html'],
  ]
  for (const [, destination] of pages) {
    const file = join(outDir, destination)
    await mkdir(dirname(file), { recursive: true })
    await writeFile(file, 'current page')
  }
  const config = await resolveConfig('docs', 'build')
  await config.buildEnd({ ...config, outDir })
  for (const [source, destination] of pages) {
    const html = await readFile(join(outDir, source), 'utf8')
    const script = html.match(/<script>(.*?)<\/script>/s)[1]
    for (const base of ['/', '/kiyosi-website/']) {
      let redirected
      runInNewContext(script, { location: {
        search: '?from=bookmark', hash: '#building-from-source',
        replace: (target) => { redirected = target },
      } })
      assert.equal(
        new URL(redirected, `https://example.com${base}${source}`).href,
        `https://example.com${base}${destination}?from=bookmark#building-from-source`,
      )
    }
  }
})
