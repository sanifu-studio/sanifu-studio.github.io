# -*- coding: utf-8 -*-
"""Remove the fictional-brand chips baked into site images and PDFs (Sarit 5 Nov 2026).
Captions on made-up figures and demo reviews stay: PDF footers, info_0x lower notes, v_reviewclip_demo.
Run from 60_site/ with ~/.venvs/pageart/bin/python. Originals are in git."""
import subprocess, sys
import cv2, fitz, numpy as np

OCR = sys.argv[1]
WORDS = (u'ตัวอย่างงาน', u'ตัวอย่างผลงาน', u'ชุดสาธิต', u'ชุดสาริต', u'เทศบาลสมมติ', u'บริษัทสมชติ', u'ชุดสาชิต')
# file, chip margin as a share of image width, solid fill (flat background) or inpaint (texture)
IMAGES = [('assets/w/poster_cafe.jpg', .006, 'clone'), ('assets/w/poster_cafe_full.jpg', .006, 'clone'),
          ('assets/w/poster_wine.jpg', .006, 'clone'), ('assets/w/poster_wine_full.jpg', .006, 'clone'),
          ('assets/w/poster_run_full.jpg', .006, 'clone'),
          ('assets/w/info_01.jpg', .022, 'solid'), ('assets/w/info_01_tall.jpg', .022, 'solid'),
          ('assets/w/info_04.jpg', .022, 'solid'), ('assets/w/info_07.jpg', .022, 'solid'), ('assets/w/info_03.jpg', .022, 'solid'),
          ('assets/iso_info.jpg', .006, 'inpaint')]
PDF_CHIPS = {'info_01': u'ตัวอย่างผลงาน', 'info_04': u'ชุดสาธิต', 'info_07': u'ชุดสาธิต', 'info_02': u'ชุดสาธิต', 'info_03': u'ชุดสาธิต'}


def ocr_lines(path):
    out = subprocess.run([OCR, path], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8', 'replace')
    for line in out.splitlines():
        a = line.split('\t')
        if len(a) == 3 and a[0] != 'DONE':
            yield [float(v) for v in a[1].split(',')], a[2]


def strip_image(path, margin, mode):
    im = cv2.imread(path)
    if im is None:
        print('missing', path); return
    h, w = im.shape[:2]
    n = 0
    for (x, y, bw, bh), text in ocr_lines(path):
        # chips sit in the top or bottom 9%; body text with the same words is not a chip
        if not any(k in text for k in WORDS) or not (y > .9 or y < .09 and path.endswith(('iso_info.jpg', 'poster_run_full.jpg'))):
            continue
        m = int(margin * w)
        x0, x1 = max(0, int(x * w) - m), min(w, int((x + bw) * w) + m)
        y0, y1 = max(0, int((1 - y - bh) * h) - m), min(h, int((1 - y) * h) + m)
        if mode == 'clone':
            # poster texture: copy the same-sized patch from beside the chip, feathered
            bw_px, bh_px = x1 - x0, y1 - y0
            sx = x0 - bw_px - 10 if x0 > w * .5 else x1 + 10
            patch = im[y0:y1, sx:sx + bw_px].astype(np.float32)
            a = np.ones((bh_px, bw_px), np.float32)
            f = max(3, m)
            for i in range(f):
                v = (i + 1.) / f
                a[i, :] = np.minimum(a[i, :], v); a[-i - 1, :] = np.minimum(a[-i - 1, :], v)
                a[:, i] = np.minimum(a[:, i], v); a[:, -i - 1] = np.minimum(a[:, -i - 1], v)
            a = a[..., None]
            im[y0:y1, x0:x1] = (patch * a + im[y0:y1, x0:x1].astype(np.float32) * (1 - a)).astype(np.uint8)
        elif mode == 'solid':
            band = im[y0:y1, max(0, x0 - 6):max(1, x0 - 2)].reshape(-1, 3)
            im[y0:y1, x0:x1] = np.median(band, axis=0)
        else:
            mask = np.zeros((h, w), np.uint8)
            mask[y0:y1, x0:x1] = 255
            im = cv2.inpaint(im, mask, 5, cv2.INPAINT_TELEA)
        n += 1
    if n:
        cv2.imwrite(path, im, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(path, 'chips', n)


def strip_pdf(name, word):
    p = 'assets/%s.pdf' % name
    d = fitz.open(p)
    pg = d[0]
    n = 0
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            text = ''.join(s['text'] for s in l['spans'])
            r = fitz.Rect(l['bbox'])
            if word in text and r.y0 < 90 and r.x1 > 600:
                r = r + (-15, -9, 15, 9)
                px = pg.get_pixmap(clip=fitz.Rect(r.x0 - 5, r.y0, r.x0 - 3, r.y1), alpha=False)
                c = np.frombuffer(px.samples, np.uint8).reshape(-1, 3)
                fill = tuple(np.median(c, axis=0) / 255.)
                pg.add_redact_annot(r, fill=fill)
                n += 1
    pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED)
    d.save(p + '.tmp', garbage=3, deflate=True)
    d.close()
    import os
    os.replace(p + '.tmp', p)
    print(p, 'chips', n)


for a in IMAGES:
    strip_image(*a)
for k, v in PDF_CHIPS.items():
    strip_pdf(k, v)
