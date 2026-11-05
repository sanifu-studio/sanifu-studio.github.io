# -*- coding: utf-8 -*-
"""Add the molu box clip as the third card, after NETT (Sarit passed it 5 Nov 2026). Run from 60_site/. Going live needs "ขึ้นได้"."""
import io, os, re, shutil
FW = os.path.abspath('..')
R = os.path.join(FW, '30_offer/portfolio/box_unfold_2026-11-05/out')
V = 'product_box_unfold'
shutil.copy(os.path.join(R, 'box_unfold_9x16.mp4'), 'assets/%s.mp4' % V)
shutil.copy(os.path.join(R, 'card_preview.mp4'), 'assets/%s_preview.mp4' % V)
shutil.copy(os.path.join(R, 'card_cover.jpg'), 'assets/w/v_%s.jpg' % V)
CARD = (u'    <a class="card" data-cat="product" href="assets/%s.mp4" target="_blank"><div class="media"><img src="assets/w/v_%s.jpg" width="640" height="800" alt="คลิปกล่องเซรั่มคลี่ออกเป็นกระดาษแผ่นเดียว">'
        u'<video muted loop playsinline preload="none" data-src="assets/%s_preview.mp4"></video><span class="badge">▶ 15 วิ</span></div>'
        u'<div class="cap"><p class="biz">แบรนด์สกินแคร์</p><p class="idea"><span class="nw">กล่องคลี่ออก</span> <span class="nw">เหลือกระดาษแผ่นเดียว</span></p>'
        u'<p class="what"><span class="nw">ออกแบบกล่อง</span> <span class="nw">พร้อมแผ่นคลี่</span></p></div></a>\n') % (V, V, V)
s = io.open('index.html', encoding='utf-8').read()
assert V not in s
assert 'motion_receipts_statement' in s
nett = re.search(r'[ \t]*<a class="card[^>]*href="assets/motion_receipts_statement\.mp4".*?</a>\n', s, re.S)
s = s[:nett.end()] + CARD + s[nett.end():]
# only the first 8 cards animate in and skip lazy loading
cards = list(re.finditer(r'<a class="card[^"]*"( style="[^"]*")?', s))
for i, m in reversed(list(enumerate(cards))):
    s = s[:m.start()] + ('<a class="card rise" style="--d:%.2fs"' % (.5 + i * .07) if i < 8 else '<a class="card"') + s[m.end():]
io.open('index.html', 'w', encoding='utf-8').write(s)
print('cards', len(cards))
