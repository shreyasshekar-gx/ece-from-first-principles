/* Keep the browser runtime local and reproducible from package-lock.json. */
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const pkg=path.join(root,'node_modules/@lucasmarkes/hairline');
const out=path.join(root,'site/vendor/hairline');
fs.mkdirSync(out,{recursive:true});
for(const [source,target] of [['dist/index.js','index.js'],['dist/index.js.map','index.js.map'],['LICENSE','LICENSE']])fs.copyFileSync(path.join(pkg,source),path.join(out,target));
const version=JSON.parse(fs.readFileSync(path.join(pkg,'package.json'),'utf8')).version;
fs.writeFileSync(path.join(out,'version.json'),JSON.stringify({package:'@lucasmarkes/hairline',version},null,2)+'\n');
console.log(`Bundled Hairline ${version} for static hosting.`);
