"""สร้างภาพการ์ดผลงาน 4:5 + ภาพเต็ม + ภาพปกคลิป สำหรับหน้าแรกใหม่ (22 ต.ค. 2569)
รัน: python3 _build/build_work_assets.py  (จากโฟลเดอร์ 60_site)
"""
import os, subprocess
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FW = os.path.abspath(os.path.join(ROOT, '..'))
OUT = os.path.join(ROOT, 'assets', 'w')
os.makedirs(OUT, exist_ok=True)
TW, TH = 640, 800

def thumb(im, name, focus=0.5):
    im = im.convert('RGB'); w, h = im.size; r = TW / TH
    if w / h > r:  # กว้างเกิน ตัดข้าง
        nw = int(h * r); x = int((w - nw) * focus); im = im.crop((x, 0, x + nw, h))
    else:          # สูงเกิน ตัดล่างบน (เน้นด้านบน)
        nh = int(w / r); y = int((h - nh) * focus); im = im.crop((0, y, w, y + nh))
    im.resize((TW, TH), Image.LANCZOS).save(os.path.join(OUT, name + '.jpg'), quality=80, optimize=True, progressive=True)

def full(im, name, long=1800):
    im = im.convert('RGB'); im.thumbnail((long, long), Image.LANCZOS)
    im.save(os.path.join(OUT, name + '_full.jpg'), quality=84, optimize=True, progressive=True)

def stack_pair(path, credit_px):
    """ภาพก่อน/หลังวางข้างกัน → วางซ้อนบนล่าง เก็บแถบเครดิตไว้ล่างสุด"""
    im = Image.open(path).convert('RGB'); w, h = im.size
    body = im.crop((0, 0, w, h - credit_px)); credit = im.crop((0, h - credit_px, w, h))
    a = body.crop((0, 0, w // 2, body.height)); b = body.crop((w // 2, 0, w, body.height))
    cw = w // 2; credit = credit.resize((cw, max(1, int(credit_px * cw / w * 2))))
    out = Image.new('RGB', (cw, a.height * 2 + 6 + credit.height), 'white')
    out.paste(a, (0, 0)); out.paste(b, (0, a.height + 6)); out.paste(credit, (0, a.height * 2 + 6))
    return out

def P(p): return Image.open(os.path.join(FW, p))

SRC = {
  'menu_ushi':   ('40_jobs/jobboard/offer_2026-10-13/menu_9f7422a5/out/menu_A4.jpg', 0.0),
  'poster_cafe': ('40_jobs/practice/p04_cafe_japandi/out/final_r2_2400x3200_attach.jpg', 0.0),
  'poster_wine': ('40_jobs/practice/p02_wine_luxury/out/final_r3_2400x3200_attach.jpg', 0.0),
  'poster_run':  ('40_jobs/practice/p01_g14_iso/out/A2.png', 0.0),
  'nametent':    ('40_jobs/jobboard/offer38_name_tent_card/1_แนวD_กรมท่าหินอ่อนทอง.png', 0.5),
  'retouch_event': ('40_jobs/practice/p06_photo_retouch/review/att_setA.jpg', 0.0),
  'retouch_dark':  ('40_jobs/practice/p06_photo_retouch/review/r3_A2_pair.jpg', 0.0),
  'pack_nuan':   ('40_jobs/practice/b02_skincare_brand/out/mockups/scene_family.jpg', 0.5),
  'pack_nuan_box': ('40_jobs/practice/b02_skincare_brand/out/mockups/dropper_a.jpg', 0.5),
  'product_tuen': ('30_offer/portfolio_product_images/out_photoreal/03_4x5.jpg', 0.5),
}
for name, (p, f) in SRC.items():
    im = P(p); thumb(im, name, f); full(im, name)
for name, p in [('retouch_cake', '40_jobs/practice/p06_photo_retouch/review/r2_B2_pair.jpg'),
                ('retouch_food', '40_jobs/practice/p06_photo_retouch/review/r2_B1_pair.jpg')]:
    st = stack_pair(os.path.join(FW, p), 22); thumb(st, name, 0.0); full(P(p), name)

# ภาพปกคลิป: เฟรมที่ 1.2 วิ จากไฟล์ preview
VIDS = ['reel_fashion','edit_postprod_ba','review_classy','edit_broll_pip','reviewclip_demo','subtitle_sample',
        'motion_tuen','motion_invora','motion_dca','data_salary_film']
SEEK = {'motion_dca': '2.5'}
VFOCUS = {'motion_dca': 0.0}
for v in VIDS:
    src = os.path.join(ROOT, 'assets', v + '_preview.mp4')
    tmp = os.path.join(OUT, '_f.png')
    subprocess.run(['ffmpeg','-v','error','-y','-ss',SEEK.get(v,'1.2'),'-i',src,'-frames:v','1',tmp], check=True)
    thumb(Image.open(tmp), 'v_' + v, VFOCUS.get(v, 0.35)); os.remove(tmp)

# งานเดิมในเว็บ ทำการ์ด 4:5 ให้เป็นผังเดียวกัน
A = os.path.join(ROOT, 'assets')
for name, f, foc in [('iso_siam','iso_siam.jpg',0.8),('iso_horapa','iso_horapa.jpg',0.8),('iso_velara','iso_velara.jpg',0.8),
                     ('iso_info','iso_info.jpg',0.8),('phone_info','m5_phone_info02.jpg',0.5),
                     ('info_01','info_01.png',0.0),('info_04','info_04.png',0.0),('info_07','info_07.png',0.0),('info_03','info_03.png',0.0)]:
    thumb(Image.open(os.path.join(A, f)), name, foc)
print('ok', len(os.listdir(OUT)))

# ภาพเลื่อนก่อน/หลัง (ร้านอาหารมืด A2 · Photo: Tony Barrett · CC BY-SA 4.0)
im = P('40_jobs/practice/p06_photo_retouch/review/r3_A2_pair.jpg').convert('RGB')
for n, box in [('ba_before', (0, 0, 1600, 1067)), ('ba_after', (0, 1073, 1600, 2140))]:
    c = im.crop(box); c.thumbnail((1200, 1200)); c.save(os.path.join(OUT, n + '.jpg'), quality=82, optimize=True, progressive=True)
