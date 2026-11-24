import json, subprocess, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
links=json.loads((ROOT/'sources/young-master-links.json').read_text())
ym=[x['url'] for x in links if '/model/' in x['url']]
spec={1:'gizeh-black-extra-fine-magnet-100',2:'gizeh-fine-magnet-100',7:'gizeh-original-magnet-100',13:'gizeh-super-fine-magnet-100',16:'gizeh-1-size-super-fine-50',21:'gizeh-extra-slim-5mm-filters-bag-150'}
urls={k:'https://www.gizeh-online.com/en/products/'+v for k,v in spec.items()}
for k,needle in {24:'red-84-mm-15-mm-filter-200',25:'blue-84-mm-15-mm-filter-200',26:'red-84-mm-24-mm-filter-200',27:'gray-84-mm-17-mm-recess',28:'slim-size-cigarette-tubes-young-master-red',29:'slim-size-cigarette-tubes-young-master-blue-84-mm-24',30:'red-84-mm-15-mm-filter-500',31:'papers-crp',32:'papers-sir-badger',33:'papers-young-master'}.items():
 urls[k]=next(u for u in ym if needle in u)
urls.update({3:'https://www.asimis-market.com/product/gizeh-paper-green-extra-slim-fine-regular-thickness-66-sheets/',4:'https://www.bullbrand.co.uk/products/gizeh-fine-cut-corners',9:'https://www.premiumcigarbox.com/products/gizeh-pure-rolling-paper-1-1-4-extra-fine-50-sheets/',10:'https://shopbyakikiscigars.com/products/gizeh-pure-extra-fine-50',11:'https://ronscigarstore.com/products/gizeh-pure-fine-rolling-papers',12:'https://shopbyakikiscigars.com/products/gizeh-pure-fine-50',14:'https://tabakeria.lv/en/product/rolling-paper-gizeh-super-fine-cut-corners',15:'https://www.asimis-market.com/product/gizeh-papers-light-green-extra-slim-super-fine-66-sheets/',22:'https://hempelf.com/products/gizeh-charcoal-filter-tips-8mm'})
(ROOT/'data/source-map.json').write_text(json.dumps(urls,indent=2,ensure_ascii=False))
urls.update({5:'https://www.hodnedobratrafika.cz/cigaretove-papirky-gizeh-fine-red--50-ks-/',6:'https://www.gizeh-online.com/en/products/gizeh-king-size-slim-extra-fine-34',8:'https://www.tobacconistas.gr/en/product/rolling-papers-gizeh-original-blue-50-pieces/',17:'https://www.bullbrand.co.uk/products/mascotte-extra-thin-rolls',18:'https://www.dutch-headshop.eu/mascotte-elements-king-size-slim-rolling-paper',19:'https://www.smokers.gr/en/Rolling-Papers/Mascotte-Rolling-Papers/',20:'https://www.sigarenkraam.nl/a-59336171/vloei/mascotte-original-66-slim-vloei/',23:'https://www.bullbrand.co.uk/products/gizeh-standard-filters'})
(ROOT/'data/source-map.json').write_text(json.dumps(urls,indent=2,ensure_ascii=False))
js='JSON.stringify({title:document.title,text:document.body.innerText,images:Array.from(document.images).map(i=>({url:i.currentSrc,alt:i.alt,width:i.naturalWidth,height:i.naturalHeight}))})'
for k,u in urls.items():
 out=ROOT/f'sources/product-{k:02d}.json'
 if out.exists(): continue
 try:
  subprocess.run(['mb','go',u],check=True,capture_output=True,timeout=45)
  r=subprocess.run(['mb','js',js],check=True,capture_output=True,text=True,timeout=30)
  d=json.loads(r.stdout); d['source_url']=u
  out.write_text(json.dumps(d,ensure_ascii=False,indent=2))
  print(k,d['title'],len(d['images']),flush=True)
 except Exception as e: print(k,'ERROR',str(e),flush=True)