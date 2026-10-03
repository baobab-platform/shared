// Use Codegen's supported programmatic API for local SDL. The general-purpose
// CLI loaders introduce braces (GHSA-vfj7-8cjw-p6xm) although this package only
// reads local .graphql files. Keep the existing plugin and generation config.
import { globSync } from 'node:fs';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { codegen } from '@graphql-codegen/core';
import * as typescript from '@graphql-codegen/typescript';
import { buildASTSchema, lexicographicSortSchema, parse, printSchema } from 'graphql';
import config from '../codegen.ts';

const root = fileURLToPath(new URL('..', import.meta.url));
const paths = globSync(config.schema, { cwd: root }).sort();
if (paths.length === 0) throw new Error(`No GraphQL schemas match ${config.schema}`);
const sources = await Promise.all(paths.map((path) => readFile(resolve(root, path), 'utf8')));
// Match the CLI's deterministic schema ordering before invoking the same plugin.
const schema = parse(printSchema(lexicographicSortSchema(buildASTSchema(parse(sources.join('\n'))))));
for (const [filename, output] of Object.entries(config.generates)) {
  const generated = await codegen({
    filename,
    schema,
    documents: [],
    config: {},
    plugins: output.plugins.map((name) => ({ [name]: {} })),
    pluginMap: { typescript },
  });
  const destination = resolve(root, filename);
  await mkdir(dirname(destination), { recursive: true });
  await writeFile(destination, generated);
}
