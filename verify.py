import pathlib,json,re,hashlib
from PIL import Image
R=pathlib.Path(__file__).resolve().parent
p=json.loads((R/'data/catalog.json').read_text())
assert len(p)==33
assert sum(len(x['variants']) for x in p)==91
photos=json.loads((R/'data/photos.json').read_text())
for m in photos:
 f=R/m['path'];assert f.exists(),f
 with Image.open(f) as im:im.verify()
 assert hashlib.sha256(f.read_bytes()).hexdigest()==m['sha256'],f
for f in (R/'catalog').rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if target.startswith(('https:','http:','#')):continue
  assert (f.parent/target).exists(),(f,target)
for x in p:
 assert all(k not in x for k in ['price','purchase_price','invoice','quantity_purchased'])
print(f"OK: {len(p)} products, 91 quantity variants, {len(photos)} images; all local Markdown links and image checksums valid.")