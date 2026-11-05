# -*- coding: utf-8 -*-
"""Add one idea line to each card, move the idea-led pieces to the top of the grid, allow 3 previews at once (Sarit 5 Nov 2026).
Line = thing + what happens, from spatialsites analysis. Must describe what is visibly in the piece; no results or client claims. Run once from 60_site/."""
import io, re

IDEAS = {
 'menu_ushi_tall': u'ภาพเนื้อ นำทุกหมวด บนเมนูดำ',
 'ba_after_45': u'ร้านเดิม แสงใหม่',
 'brand_jedkrueng': u'เลข 7 กับเศษครึ่ง รวมเป็นตัวเดียว',
 'poster_cafe': u'กาแฟหยดอยู่ใต้ คำว่าเปิดแล้ว',
 'v_edit_postprod_ba': u'ฟุตเทจเดิมที่มีอยู่ ตัดใหม่ให้น่าดู',
 'v_edit_pink_story': u'ภาพนิ่งซ้อนกัน เล่าเรื่องตอนเช้า',
 'pack_nuan': u'ฉลาก กล่อง ขวด พูดภาษาเดียวกัน',
 'info_01_tall': u'จากเชอร์รี่สุก ถึงถุงกาแฟ',
 'retouch_cake': u'เค้กออกจากโต๊ะรก มาอยู่พื้นขาว',
 'poster_wine': u'ขวดไวน์ยืนทับ คำว่าไวน์',
 'v_motion_plan_to_house': u'เส้นแบบแปลน ยกตัวเป็นบ้านทีละส่วน',
 'v_motion_invora_kinetic': u'ยอดค้างจ่าย วิ่งลงจนเหลือศูนย์',
 'retouch_event': u'หน้าคนชัด สีผิวกลับมาเป็นธรรมชาติ',
 'iso_siam': u'โรงงานเหล็ก เล่าจบใน 10 หน้า',
 'retouch_food': u'จานเดิม ชีสน่ากินขึ้น',
 'brand_eventide': u'หงส์คู่กลายเป็นโลโก้ ไปถึงเครื่องเขียน',
 'product_tuen': u'ถุงเดียว วางครบ 10 ฉาก',
 'v_subtitle_sample': u'คำสำคัญเปลี่ยนสี ตามเสียงพูด',
 'nametent': u'พับครึ่งแล้ว ตั้งบนโต๊ะได้เลย',
 'v_sub_talk_wildfire': u'คนพูดอังกฤษ อ่านเป็นไทยตามทัน',
 'info_04': u'3 ทางขาย วางเทียบกันในแผ่นเดียว',
 'v_reel_fashion': u'เสื้อลินิน เดินผ่านแดดบ่าย',
 'iso_horapa': u'เล่าธุรกิจให้นักลงทุน ใน 12 หน้า',
 'v_motion_studybear': u'เด็กกับหมี แข่งกับเวลาก่อนสอบ',
 'v_review_classy': u'ราวเสื้อกับรีวิว เด้งตามเพลง',
 'pack_nuan_box': u'ขวดหยดยืนบนหิน ข้างกล่องของมัน',
 'poster_run': u'เส้นทางวิ่ง กลายเป็นตัวโปสเตอร์',
 'ig_baankua': u'เมล็ดไหลจากถุง ลงมือ',
 'info_07': u'เงินหายไปไหน ดูจากแถบสี',
 'v_motion_tuen': u'ถุงกาแฟกับเมล็ดลอย เล่าสินค้าด้วยเสียงไทย',
 'iso_velara': u'คลินิกเล่าตัวเอง ใน 10 หน้า',
 'brand_nuan': u'จากไร่สมุนไพร ถึงชุดบรรจุภัณฑ์',
 'v_reviewclip_demo': u'แคปรีวิวซ้อนกัน ไปตามจังหวะ',
 'phone_info': u'ขั้นตอนนัดหมาย อ่านจบบนจอมือถือ',
 'v_motion_invora': u'ตัวละครเดียว เล่าแอปตลอดคลิป',
 'v_sub_talk_teacher': u'ครูเล่าเรื่อง มีหัวข้อดึงคนดู',
 'info_03': u'5 จุดในบ้าน เรียงจากที่ลดได้มากสุด',
 'iso_info': u'8 เรื่อง ขยายพิมพ์ได้ทุกชิ้น',
 'v_motion_dca': u'เปิดเรื่องด้วยตัวเลขเดียว',
 'v_data_salary_film': u'เงินเดือนเท่านี้ ซื้อบ้านได้แค่ไหน',
}
FIRST = ['v_motion_plan_to_house', 'box_unfold', 'receipts_statement']  # idea-led pieces lead the grid

p = 'index.html'
s = io.open(p, encoding='utf-8').read()
assert 'class="idea"' not in s
a = s.index('<div class="grid" id="work">') + len('<div class="grid" id="work">')
b = s.index('</div>\n  <p class="showall"') if '</div>\n  <p class="showall"' in s else None
cards = list(re.finditer(r'[ \t]*<a class="card[^>]*>.*?</a>\n', s, re.S))
start, end = cards[0].start(), cards[-1].end()
items = []
for m in cards:
    c = m.group(0)
    key = re.search(r'<img[^>]*src="[^"]*/([^"/]+)\.jpg"', c).group(1)
    line = ' '.join('<span class="nw">%s</span>' % w for w in IDEAS[key].split(' '))
    c2 = c.replace('<p class="what">', '<p class="idea">%s</p><p class="what">' % line, 1)
    assert c2 != c, key
    items.append((key, c2))
head = [x for k in FIRST for x in items if x[0] == k]
rest = [x for x in items if x[0] not in FIRST]
ordered = head + rest
out = []
for i, (k, c) in enumerate(ordered):
    c = re.sub(r'<a class="card[^"]*"( style="[^"]*")?', '<a class="card%s"%s' % (' rise' if i < 8 else '', ' style="--d:%.2fs"' % (.5 + i * .07) if i < 8 else ''), c, 1)
    if i < 8:
        c = c.replace(' loading="lazy"', '', 1)
    elif ' loading="lazy"' not in c:
        c = c.replace('<img ', '<img loading="lazy" ', 1)
    out.append(c)
s = s[:start] + ''.join(out) + s[end:]
s = s.replace("  .what{font-size:.9rem;font-weight:600;line-height:1.45;margin-top:1px}",
              "  .idea{font-size:.92rem;font-weight:600;line-height:1.4;margin-top:1px}\n  .what{font-size:.78rem;color:var(--muted);line-height:1.4;margin-top:3px}", 1)
assert '.idea{' in s
n = s.count('.slice(0,2)')
assert n == 1
s = s.replace('.slice(0,2)', '.slice(0,3)').replace(u'ไม่เกิน 2 ตัว', u'ไม่เกิน 3 ตัว')
io.open(p, 'w', encoding='utf-8').write(s)
print('cards', len(ordered), 'first', [k for k, _ in ordered[:4]])
