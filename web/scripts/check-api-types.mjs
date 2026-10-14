// Regenerates the API types into a temp file and fails when src/api/schema.d.ts is stale.
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const committed = 'src/api/schema.d.ts';
const dir = mkdtempSync(join(tmpdir(), 'ks-api-'));
const fresh = join(dir, 'schema.d.ts');
try {
  execFileSync('pnpm', ['exec', 'openapi-typescript', '../contracts/openapi.json', '-o', fresh], {
    stdio: 'ignore',
  });
  if (readFileSync(fresh, 'utf8') !== readFileSync(committed, 'utf8')) {
    console.error(`${committed} is stale. Run: pnpm --dir web gen:api`);
    process.exitCode = 1;
  } else {
    console.log('api types: up to date');
  }
} finally {
  rmSync(dir, { recursive: true, force: true });
}
