"""เพิ่มคลิปแบบแปลนกลายเป็นบ้าน (Sarit 5 พ.ย. 2569 "ขึ้นได้") ขึ้นต้นหมวดโมชัน
รัน: python3 _build/add_2026-11-05.py  (จากโฟลเดอร์ 60_site)
"""
import os, subprocess
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FW = os.path.abspath(os.path.join(ROOT, '..'))
A = os.path.join(ROOT, 'assets'); OUT = os.path.join(A, 'w')
TW, TH = 640, 800
V = 'motion_plan_to_house'
SRC = os.path.join(FW, '40_jobs/_attach/Contractor_Scroll_House_9x16.mp4')

subprocess.run(['ffmpeg','-v','error','-y','-i',SRC,'-c','copy','-movflags','+faststart',os.path.join(A, V + '.mp4')], check=True)
# พรีวิวเร่ง 2 เท่า ให้เห็นครบตั้งแต่แบบแปลนจนบ้านเสร็จใน 7.5 วิ
subprocess.run(['ffmpeg','-v','error','-y','-i',SRC,'-an','-vf','setpts=0.5*PTS,fps=24,scale=540:960','-c:v','libx264','-crf','30',
                '-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',os.path.join(A, V + '_preview.mp4')], check=True)
tmp = os.path.join(OUT, '_f.png')
subprocess.run(['ffmpeg','-v','error','-y','-ss','13.5','-i',SRC,'-frames:v','1',tmp], check=True)
im = Image.open(tmp).convert('RGB'); w, h = im.size
nh = int(w * TH / TW); y = int((h - nh) * 0.62)
im.crop((0, y, w, y + nh)).resize((TW, TH), Image.LANCZOS).save(os.path.join(OUT, 'v_' + V + '.jpg'), quality=80, optimize=True, progressive=True)
os.remove(tmp)

CARD = ('    <a class="card" data-cat="motion" href="assets/%s.mp4" target="_blank"><div class="media"><img loading="lazy" src="assets/w/v_%s.jpg" width="640" height="800" alt="คลิปแบบแปลนกลายเป็นบ้านสามมิติ">'
        '<video muted loop playsinline preload="none" data-src="assets/%s_preview.mp4"></video><span class="badge">▶ 15 วิ</span></div>'
        '<div class="cap"><p class="biz">รับสร้างบ้าน</p><p class="what"><span class="nw">คลิปแบบแปลน</span> <span class="nw">กลายเป็นบ้าน</span></p></div></a>\n') % (V, V, V)
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()
if CARD not in s:
    k = s.index('    <a class="card" data-cat="motion"')
    s = s[:k] + CARD + s[k:]
    open(p, 'w', encoding='utf-8').write(s)
print('ok')
