import { spawnSync } from 'node:child_process'

const windows = process.platform === 'win32'
const probe = 'import sys; print(sys.executable if sys.version_info >= (3, 12) else "")'
const candidates = [
  ...(windows ? [['py', '-3', '-c', probe]] : []),
  [windows ? 'python' : 'python3', '-c', probe],
  [windows ? 'python3' : 'python', '-c', probe],
  ['uv', 'python', 'find', '--offline', '>=3.12'],
]
let python
for (const [command, ...args] of candidates) {
  const result = spawnSync(command, args, { encoding: 'utf8' })
  if (!result.error && result.status === 0 && result.stdout.trim()) {
    python = result.stdout.trim()
    break
  }
}
if (!python) {
  console.error('Python 3.12+ was not found. Install Python with venv and pip, or make an existing uv-managed Python available.')
  process.exit(1)
}
const result = spawnSync(python, process.argv.slice(2), { stdio: 'inherit' })
if (result.error) console.error(result.error.message)
process.exit(result.status ?? 1)
