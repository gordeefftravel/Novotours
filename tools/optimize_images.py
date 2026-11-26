#!/usr/bin/env python3
"""Создаёт WebP-копии картинок (оригиналы не трогает) и og-banner.jpg. Требуется Pillow."""
import glob, os
from PIL import Image
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
tot0=tot1=0
for f in sorted(glob.glob("static/img/*.jpg")+glob.glob("static/img/*.png")):
    b,ext=os.path.splitext(f)
    if os.path.basename(f) in("og-banner.png",): continue
    im=Image.open(f)
    if im.width>1280: im=im.resize((1280,round(im.height*1280/im.width)),Image.LANCZOS)
    has_a=im.mode in("RGBA","LA","P")
    im=im.convert("RGBA" if has_a else "RGB")
    out=b+".webp"; im.save(out,"WEBP",quality=78,method=6)
    tot0+=os.path.getsize(f); tot1+=os.path.getsize(out)
im=Image.open("static/img/og-banner.png").convert("RGB")
im=im.resize((1200,round(im.height*1200/im.width)),Image.LANCZOS); im.save("static/img/og-banner.jpg","JPEG",quality=82,optimize=True)
print("оригиналы %d КБ → webp %d КБ; og-banner.jpg %d КБ"%(tot0//1024,tot1//1024,os.path.getsize("static/img/og-banner.jpg")//1024))
