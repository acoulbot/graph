import json, pathlib, re, hashlib, concurrent.futures, io
import openpyxl, httpx
from PIL import Image, ImageOps, ImageDraw
R=pathlib.Path(__file__).resolve().parent
import sys
if len(sys.argv)!=2:
 raise SystemExit('Usage: python prepare.py /path/to/products.xlsx')
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
rows=[]
for row in list(wb['Товары'].values)[1:34]:
 rows.append(dict(id=row[0],supplier_article=str(row[3] or ''),type=row[4],brand=row[5],model=row[6],features=row[7] or '',per_package=row[8],unit=row[9],variants=[1,3,5] if row[15]==3 else [1]))
(R/'data/products.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
filters={3:'128e_',4:'Gizeh_Papers6',5:'617_gizeh',8:'587-Rolling',9:'20260507_285053',10:'473_Akikis',11:'FullSizeRender',12:'31_25d2',14:'Light-Green',15:'128b_',17:'Mascotte_Papers2',18:'mascotte-vloei-original-king-size-slim-magnet-pakje_1',19:'mascotte-regular-01',20:'',22:'Gizeh-filters',23:'Standard_filters'}
manifest=[]
for p in rows:
 k=p['id']; src=R/f'sources/product-{k:02d}.json'
 if not src.exists():continue
 d=json.loads(src.read_text());imgs=[]
 for im in d.get('images',[]):
  u=im['url']
  if k>=24:
   main=next((i['url'] for i in d['images'] if 'hotfrost.ru/admin/images/products/' in i['url']),None)
   ok=main and u.split('/thumb')[0]==main.split('/thumb')[0]
  elif k in [1,2,6,7,13,16,21]:ok=u.startswith('https://cdn.shopify.com/') and '/files/' in u
  elif k==20:ok='Mascotte' in im.get('alt','') and '66' in im.get('alt','')
  else:ok=bool(filters.get(k)) and filters[k] in u
  if ok and u not in imgs:imgs.append(u)
 for n,u in enumerate(imgs):manifest.append(dict(product_id=k,image_index=n+1,url=u,page=d['source_url'],path=f'assets/{k:02d}-{n+1:02d}.jpg'))
def download(m):
 try:
  res=httpx.get(m['url'],follow_redirects=True,timeout=35);res.raise_for_status()
  img=Image.open(io.BytesIO(res.content)).convert('RGB');img.thumbnail((1600,1600));img.save(R/m['path'],quality=93)
  m['width'],m['height']=img.size;m['sha256']=hashlib.sha256((R/m['path']).read_bytes()).hexdigest();m['status']='downloaded'
 except Exception as e:m['status']='failed';m['error']=str(e)
 return m
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:manifest=list(ex.map(download,manifest))
# Remove exact duplicate files within each product, not distinct photos.
seen=set();unique=[]
for m in manifest:
 key=(m['product_id'],m.get('sha256'))
 if m['status']=='downloaded' and key in seen:
  (R/m['path']).unlink();continue
 seen.add(key);unique.append(m)
(R/'data/photos.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2))
good=[m for m in unique if m['status']=='downloaded'];print('PRODUCTS',len(rows),'PHOTOS',len(good))
cols=6;w=240;h=210
sheet=Image.new('RGB',(cols*w,((len(good)+cols-1)//cols)*h),'#eeeeee');draw=ImageDraw.Draw(sheet)
for n,m in enumerate(good):
 im=Image.open(R/m['path']);im.thumbnail((w-12,h-35));x=(n%cols)*w;y=(n//cols)*h
 sheet.paste(im,(x+(w-im.width)//2,y+25));draw.text((x+8,y+5),m['path'],fill='black')
sheet.save('/home/user/graph-contact.jpg')