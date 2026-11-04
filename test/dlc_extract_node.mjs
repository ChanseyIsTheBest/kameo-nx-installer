// kameo-nx-installer: the levels and models inside the DLC packs, written to a folder with the page's own reader (lib/kameo_files.js),
// for test/full_node.mjs --dlc=<folder>. The output is game data: never committed or shared.
//   node test/dlc_extract_node.mjs <folder of packages> <out folder>
import fs from 'node:fs';
import path from 'node:path';
import { dlcArchives } from '../lib/kameo_files.js';

const [from, out] = process.argv.slice(2);
const files = fs.readdirSync(from).filter((n) => fs.statSync(path.join(from, n)).isFile() && !n.endsWith('.txt'))
  .map((n) => new File([fs.readFileSync(path.join(from, n))], n));
const archives = await dlcArchives(files);
for (const a of archives) {
  const target = path.join(out, a.path);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, await a.read(0, a.size));
}
console.log(`${files.length} packages: ${archives.length} levels and models, ${archives.reduce((n, a) => n + a.size, 0) >> 20} MB`);
