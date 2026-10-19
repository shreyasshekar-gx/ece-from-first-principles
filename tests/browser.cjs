/* npm install --no-save playwright; node tests/browser.cjs
   Or set PLAYWRIGHT_PATH to an existing package. ECE_CDP uses a caller-owned browser. */
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
 const attached=!!process.env.ECE_CDP;
 const browser=attached?await chromium.connectOverCDP(process.env.ECE_CDP):await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1050}});
 const page=await context.newPage();const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const base=process.env.ECE_URL||'http://127.0.0.1:8073/site/';
 const nav=async route=>{await page.goto(base+'#'+route);await page.waitForFunction(r=>document.querySelector('main').dataset.route===r,route);};
 const out=path.resolve('artifacts');fs.mkdirSync(out,{recursive:true});
 try{
  await page.goto(base);await page.waitForSelector('.hero');
  await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('.path-card').count(),4);
  for (let i=0;i<6;i++) {
   await page.waitForSelector('.is-mounted [data-hairline] svg');
   assert.equal(await page.locator('[data-hairline] svg').count(),1);
   assert.equal(await page.locator('[data-hairline]').getAttribute('data-hairline'),['phone','hub','dish'][i%3]);
   await page.locator('#plate-next').click();
  }
  await page.locator('#thought-reveal').click();
  assert.equal(await page.locator('#thought-answer').isVisible(),true);
  await page.locator('#thought-reveal').click();
  await page.locator('#menu-open').click();
  await page.locator('#theme-toggle').click();
  await page.reload();
  await page.waitForSelector('.hero');
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  await page.screenshot({path:path.join(out,'home-dark.png')});
  await page.locator('#menu-open').click();
  await page.locator('#theme-toggle').click();
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#site-menu').isVisible(),false);
  await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:path.join(out,'home-desktop.png'),fullPage:true});
  await page.getByRole('link',{name:'Explore the curriculum',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('main').dataset.route==='curriculum');
  assert.equal(await page.locator('.module').count(),24);
  await page.locator('#search').fill('metastability');
  assert.ok(await page.locator('.lesson-link').count()>0);
  await page.locator('#search').fill('no-such-lesson-999');
  assert.equal(await page.locator('.module').count(),0);
  await page.locator('#search').fill('');
  await page.locator('#path').selectOption('robotics');
  await page.waitForFunction(()=>document.querySelector('main').dataset.route==='curriculum/robotics');
  assert.equal(await page.locator('.module').count(),12);
  await nav('lesson/00-bench/01');
  await page.locator('#notes').fill('Prediction: loading reduces the voltage.');
  await page.locator('#complete').click();
  await page.reload();
  await page.waitForSelector('#notes');
  assert.equal(await page.locator('#notes').inputValue(),'Prediction: loading reduces the voltage.');
  assert.match(await page.locator('#complete').textContent(),/Practiced/);
  await page.locator('#complete').click();
  assert.match(await page.locator('#complete').textContent(),/Mark as practiced/);
  await nav('lesson/00-bench/03');
  await page.locator('input[value="1"]').check();
  await page.getByRole('button',{name:'Check my answer'}).click();
  assert.match(await page.locator('#feedback').textContent(),/Not quite/);
  await page.locator('input[value="0"]').check();
  await page.getByRole('button',{name:'Check my answer'}).click();
  assert.match(await page.locator('#feedback').textContent(),/Correct/);
  await page.screenshot({path:path.join(out,'lesson-desktop.png'),fullPage:true});
  await nav('lab');
  await page.waitForSelector('#experiment');
  for(const id of ['rc','sampling','pwm','reflection','control','power']){
   await page.locator('#experiment').selectOption(id);
   const range=page.locator('#knob');
   await range.fill(await range.getAttribute('max'));
   await range.dispatchEvent('input');
   assert.ok((await page.locator('#plot path').count())>=2);
   assert.ok(!(await page.locator('#readouts').textContent()).includes('NaN'));
  }
  await page.locator('#experiment').selectOption('rc');
  await page.screenshot({path:path.join(out,'workbench-desktop.png'),fullPage:true});
  await nav('progress');
  const downloadPromise=page.waitForEvent('download');
  await page.locator('#export').click();
  const download=await downloadPromise;const file=path.join(out,'test-progress.json');await download.saveAs(file);
  const data=JSON.parse(fs.readFileSync(file,'utf8'));assert.equal(data.quizzes['00-bench'],true);
  await page.locator('#file').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from('{bad')});
  assert.match(await page.locator('#notice').textContent(),/Could not import/);
  await page.locator('#file').setInputFiles({name:'valid.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({version:1,completed:['00-bench/01','evil'],notes:{'00-bench/01':'Imported note'},quizzes:{},last:'00-bench/01'}))});
  await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('merged'));
  assert.match(await page.locator('#progress-count').textContent(),/^1 \/ 72$/);
  await nav('lesson/00-bench/01');
  assert.equal(await page.locator('#notes').inputValue(),'Imported note');
  await nav('projects');
  assert.equal(await page.locator('.project-card').count(),5);
  await page.locator('.project-card summary').first().click();
  assert.ok(await page.locator('.project-card .command').first().isVisible());
  await nav('lesson/missing');
  assert.match(await page.locator('h1').textContent(),/not in this edition/);
  await nav('home');
  await page.waitForSelector('.is-mounted [data-hairline] svg');
  await page.locator('#search-open').click();
  await page.waitForFunction(()=>document.activeElement?.id==='search');
  await page.emulateMedia({reducedMotion:'reduce'});
  await nav('home');
  await page.waitForSelector('.is-mounted [data-hairline] svg');
  await page.setViewportSize({width:390,height:844});
  for(const route of ['home','curriculum','lesson/00-bench/01','lab','projects','resources','progress']){
   await nav(route);
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
   assert.equal(overflow,false,`Mobile overflow on ${route}`);
   if(route==='home')await page.waitForFunction(()=>!document.querySelector('#notice').textContent);
   if(route==='home')await page.screenshot({path:path.join(out,'home-mobile.png'),fullPage:true});
  }
  assert.deepEqual(errors,[]);
  console.log('PASS: home, search, paths, lesson notes/reload, completion/undo, wrong/right quiz, six simulators, export/import, projects, missing route, seven mobile routes; no JS errors.');
 }finally{await context.close();await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
