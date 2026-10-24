from PIL import Image, ImageDraw, ImageFilter
import numpy as np
def make(src,out,seed=0):
    S=900
    y,x=np.mgrid[0:S,0:S].astype(float)
    # studio backdrop: warm-neutral dark grey, lighter top-center
    d=np.sqrt(((x-S*0.5)/S)**2+((y-S*0.32)/S)**2)
    v=np.clip(74-d*95,22,74)
    rng=np.random.default_rng(seed); v=v+rng.normal(0,1.6,(S,S))  # grain
    bg=np.stack([v,v,v*1.03],-1).clip(0,255).astype(np.uint8)
    im=Image.fromarray(bg).convert('RGBA')
    shoe=Image.open(src).convert('RGBA')
    w=int(S*0.80); h=int(shoe.height*w/shoe.width); shoe=shoe.resize((w,h),Image.LANCZOS)
    ox=(S-w)//2; oy=int(S*0.47-h/2)
    sh=Image.new('L',(S,S),0); dr=ImageDraw.Draw(sh)
    dr.ellipse([ox+w*0.08,oy+h*0.86,ox+w*0.95,oy+h*1.03],fill=150)
    sh=sh.filter(ImageFilter.GaussianBlur(22))
    im.paste(Image.new('RGBA',(S,S),(0,0,0,255)),(0,0),sh)
    im.alpha_composite(shoe,(ox,oy))
    im.convert('RGB').save(out,quality=88)
make('../official/aj1-chicago.webp','ph-chicago.jpg',1)
make('../official/aj1-unc.webp','ph-unc.jpg',2)
