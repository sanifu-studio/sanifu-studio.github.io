"""เพิ่มผลงาน 6 ชุดหลังหน้าแรก 23 ต.ค. (Sarit 2 พ.ย. 2569 "ขึ้นครบ 6 ชุด")
แบรนด์ 3 ตัว · แอด INVORA ชุดใหม่ · แอด StudyBear · คลิปโทนชมพู · คลิปคนพูดซับแปลไทย 2 ตัว · โพสต์ IG ร้านกาแฟ
รัน: python3 _build/add_2026-11-02.py  (จากโฟลเดอร์ 60_site)
"""
import os, subprocess
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FW = os.path.abspath(os.path.join(ROOT, '..'))
A = os.path.join(ROOT, 'assets'); OUT = os.path.join(A, 'w')
TW, TH = 640, 800

def thumb(im, name, focus=0.5):
    im = im.convert('RGB'); w, h = im.size; r = TW / TH
    if w / h > r:
        nw = int(h * r); x = int((w - nw) * focus); im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / r); y = int((h - nh) * focus); im = im.crop((0, y, w, y + nh))
    im.resize((TW, TH), Image.LANCZOS).save(os.path.join(OUT, name + '.jpg'), quality=80, optimize=True, progressive=True)

def full(im, name, long=2400):
    im = im.convert('RGB'); im.thumbnail((long, long), Image.LANCZOS)
    im.save(os.path.join(OUT, name + '_full.jpg'), quality=84, optimize=True, progressive=True)

def P(p): return Image.open(os.path.join(FW, p))

# แบรนด์: บอร์ด 16:9 → การ์ดตัดเฉพาะส่วนโลโก้ (กล่อง x0,y0,x1,y1 บนภาพ 3840×2160) · ลิงก์ไปบอร์ดเต็ม
BRAND = {
  'brand_jedkrueng': ('40_jobs/practice/b01_cafe_brand/out/board1_concepts_attach.jpg', (1320, 180, 2520, 1680)),
  'brand_nuan':      ('40_jobs/practice/b02_skincare_brand/out/brand_board_web.jpg', (0, 0, 1728, 2160)),
  'brand_eventide':  ('40_jobs/practice/b05_hotel_brand/out/brand_board_v2.png', (60, 80, 1660, 2080)),
}
for name, (p, box) in BRAND.items():
    im = P(p).convert('RGB'); thumb(im.crop(box), name); full(im, name)
# เจ็ดครึ่ง: ภาพเต็มต่อหน้า 1 (แนวทาง 3 แบบ) กับหน้า 2 (คู่มือแบรนด์) บนล่าง
b1 = P('40_jobs/practice/b01_cafe_brand/out/board1_concepts_attach.jpg').convert('RGB')
b2 = P('40_jobs/practice/b01_cafe_brand/out/board2_guideline_attach.jpg').convert('RGB').resize(b1.size)
st = Image.new('RGB', (b1.width, b1.height * 2 + 24), 'white'); st.paste(b1, (0, 0)); st.paste(b2, (0, b1.height + 24))
full(st, 'brand_jedkrueng', long=2800)

# โพสต์ IG 3 ใบ: การ์ด = ใบกาแฟ · ลิงก์ = ภาพรวม 3 ใบ
thumb(P('40_jobs/practice/p07_ig_posts/v2_handkit/out/v3_coffee.jpg'), 'ig_baankua')
full(P('40_jobs/practice/p07_ig_posts/v2_handkit/out/v3_set.jpg'), 'ig_baankua', long=3280)

# คลิป: (ต้นฉบับ, วินาทีที่ใช้ทำปก, จุดตัดปก, วิธีทำพรีวิว)
#   None = ย่อ 9:16 ตามเดิม · 'crop' = ตัด 4:5 ตามจุดเดียวกับปก (หัวข้อบน+ซับล่างอยู่ครบ) · 'pad' = คลิปแนวนอนวางกลางพื้นชมพู
VIDS = {
  'motion_invora_kinetic': ('30_offer/portfolio/kinetic_en_2026-10-28/pack/out/INVORA_9x16_hookA.mp4', '3.0', 0.5, None),
  'motion_studybear':      ('30_offer/portfolio/studybear_batch_ads_2026-10-31/StudyBear_A2_stuck_9x16.mp4', '2.0', 0.4, None),
  'edit_pink_story':       ('40_jobs/jobboard/offer_2026-11-02_pink_clip/out/ตัวอย่างคลิปโทนชมพู_16วิ.mp4', '4.8', 0.5, 'pad'),
  'sub_talk_wildfire':     ('40_jobs/_attach/Talking_Subtitle_TH_Wildfire_9x16.mp4', '6.0', 0.28, 'crop'),
  'sub_talk_teacher':      ('40_jobs/_attach/Talking_Subtitle_TH_Teacher_9x16.mp4', '6.0', 0.28, 'crop'),
}
PAD_BG = '#F9DCE8'
def pad45(im):
    im = im.convert('RGB'); im = im.resize((TW, int(im.height * TW / im.width)), Image.LANCZOS)
    o = Image.new('RGB', (TW, TH), PAD_BG); o.paste(im, (0, (TH - im.height) // 2)); return o
for v, (src, at, foc, mode) in VIDS.items():
    src = os.path.join(FW, src)
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-c','copy','-movflags','+faststart',os.path.join(A, v + '.mp4')], check=True)
    vf = {None: 'scale=540:960',
          'crop': 'crop=iw:iw*5/4:0:(ih-iw*5/4)*%s,scale=544:680' % foc,
          'pad':  'scale=544:-2,pad=544:680:0:(oh-ih)/2:color=%s' % PAD_BG}[mode]
    subprocess.run(['ffmpeg','-v','error','-y','-ss','0.3','-t','7','-i',src,'-an','-vf',vf,'-c:v','libx264','-crf','30',
                    '-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',os.path.join(A, v + '_preview.mp4')], check=True)
    tmp = os.path.join(OUT, '_f.png')
    subprocess.run(['ffmpeg','-v','error','-y','-ss',at,'-i',src,'-frames:v','1',tmp], check=True)
    im = Image.open(tmp)
    if mode == 'pad': pad45(im).save(os.path.join(OUT, 'v_' + v + '.jpg'), quality=80, optimize=True, progressive=True)
    else: thumb(im, 'v_' + v, foc)
    os.remove(tmp)
print('ok')
