from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os, math, random

OUT_DIR = "images"
os.makedirs(OUT_DIR, exist_ok=True)
W, H = 600, 400

def gradient(draw, x1, y1, x2, y2, color1, color2):
    for y in range(y1, y2):
        ratio = (y - y1) / max(y2 - y1 - 1, 1)
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(x1, y), (x2, y)], fill=(r, g, b))

def add_noise(img, intensity=8):
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if random.random() < 0.15:
                n = random.randint(-intensity, intensity)
                r, g, b = pixels[i, j][:3]
                pixels[i, j] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return img

# -------------------------------------------------
# 1. HDPE sheet (blue semi-translucent sheet)
# -------------------------------------------------
img = Image.new("RGB", (W, H), (50, 60, 70))
draw = ImageDraw.Draw(img)
gradient(draw, 0, 0, W, H, (80, 120, 160), (40, 60, 90))
margin = 50
sw, sh = W - 2 * margin, H - 2 * margin - 30
draw.rounded_rectangle([margin, margin, margin + sw, margin + sh], radius=8, fill=(120, 170, 220), outline=(180, 210, 240), width=2)
for i in range(10):
    y = margin + 20 + i * (sh // 10)
    draw.line([(margin + 10, y), (margin + sw - 10, y)], fill=(150, 190, 230), width=1)
draw.rounded_rectangle([margin + 15, margin + 10, margin + sw - 15, margin + 40], radius=4, fill=(200, 230, 255, 80))
draw.text((W // 2, H - 20), "HDPE 聚乙烯板材", fill=(200, 215, 230), anchor="mt", font_size=14)
img = add_noise(img, 5)
img.save(os.path.join(OUT_DIR, "hdpe_sheet.jpg"), quality=92)
print("1/6 HDPE sheet done")

# -------------------------------------------------
# 2. PP pipe (white pipes)
# -------------------------------------------------
img = Image.new("RGB", (W, H), (50, 55, 50))
draw = ImageDraw.Draw(img)
gradient(draw, 0, 0, W, H, (90, 95, 85), (50, 55, 50))

pipes = [(180,200,25,45),(320,200,25,45),(460,200,25,45),(120,280,20,38),(260,280,20,38),(400,280,20,38),(540,280,20,38)]
for cx, cy, r_in, r_out in pipes:
    draw.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], fill=(200, 200, 195), outline=(160, 160, 155), width=2)
    draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=(70, 75, 70))
    draw.ellipse([cx - r_out + 5, cy - r_out + 5, cx + r_out - 15, cy + r_out - 10], fill=(230, 230, 225))

draw.rectangle([50, 150, W - 50, 165], fill=(210, 210, 205), outline=(170, 170, 165), width=2)
draw.rectangle([50, 155, W - 50, 160], fill=(230, 230, 225))
draw.text((W // 2, H - 20), "PP-R 聚丙烯管材", fill=(190, 195, 185), anchor="mt", font_size=14)
img = add_noise(img, 4)
img.save(os.path.join(OUT_DIR, "pp_pipe.jpg"), quality=92)
print("2/6 PP pipe done")

# -------------------------------------------------
# 3. PC sheet (clear/transparent sheet)
# -------------------------------------------------
img = Image.new("RGB", (W, H), (60, 70, 85))
draw = ImageDraw.Draw(img)
gradient(draw, 0, 0, W, H, (100, 120, 150), (50, 60, 80))
margin = 40
sw, sh = W - 2 * margin, H - 2 * margin
draw.rounded_rectangle([margin, margin, margin + sw, margin + sh], radius=6, fill=(160, 190, 220), outline=(200, 220, 245), width=3)

for i in range(12):
    x = margin + 15 + i * ((sw - 30) // 11)
    draw.line([(x, margin + 15), (x, margin + sh - 15)], fill=(180, 210, 240), width=1)
for i in range(8):
    y = margin + 15 + i * ((sh - 30) // 7)
    draw.line([(margin + 15, y), (margin + sw - 15, y)], fill=(180, 210, 240), width=1)

draw.rectangle([margin + 30, margin + 15, margin + sw - 30, margin + 55], fill=(220, 240, 255, 90))
draw.rectangle([margin + sw - 70, margin + sh - 50, margin + sw - 15, margin + sh - 15], fill=(220, 240, 255, 60))
draw.text((W // 2, H - 18), "PC 聚碳酸酯板材", fill=(190, 210, 230), anchor="mt", font_size=14)
img = add_noise(img, 3)
img.save(os.path.join(OUT_DIR, "pc_sheet.jpg"), quality=92)
print("3/6 PC sheet done")

# -------------------------------------------------
# 4. Engineering plastic pellets (PA6-GF30)
# -------------------------------------------------
img = Image.new("RGB", (W, H), (55, 50, 45))
draw = ImageDraw.Draw(img)
gradient(draw, 0, 0, W, H, (75, 70, 65), (45, 40, 35))
random.seed(42)
for _ in range(35):
    cx = random.randint(50, W - 50)
    cy = random.randint(40, H - 50)
    r = random.randint(14, 22)
    shade = random.randint(0, 30)
    base_r, base_g, base_b = 180 + shade, 170 + shade, 140 + shade
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(base_r, base_g, base_b), outline=(140 + shade, 130 + shade, 100 + shade), width=1)
    draw.ellipse([cx - r // 2, cy - r // 2, cx, cy], fill=(min(255, base_r + 50), min(255, base_g + 50), min(255, base_b + 40)))
for _ in range(8):
    cx = random.randint(40, W - 40)
    cy = random.randint(H - 60, H - 25)
    r = random.randint(12, 18)
    draw.ellipse([cx - r, cy - r + 3, cx + r, cy + r + 3], fill=(35, 32, 28))
draw.text((W // 2, H - 18), "PA6-GF30 增强尼龙粒子", fill=(180, 175, 165), anchor="mt", font_size=14)
img = add_noise(img, 5)
img.save(os.path.join(OUT_DIR, "plastic_pellets.jpg"), quality=92)
print("4/6 Pellets done")

# -------------------------------------------------
# 5. Waterproofing membrane (dark roll)
# -------------------------------------------------
img = Image.new("RGB", (W, H), (40, 45, 50))
draw = ImageDraw.Draw(img)
gradient(draw, 0, 0, W, H, (55, 60, 65), (35, 38, 42))
rw, rh = W - 100, H - 120
rx, ry = (W - rw) // 2, (H - rh) // 2
draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=12, fill=(30, 35, 38), outline=(55, 60, 65), width=3)
for i in range(8):
    y = ry + 15 + i * ((rh - 30) // 7)
    draw.line([(rx + 12, y), (rx + rw - 12, y)], fill=(45, 50, 53), width=2)
draw.rounded_rectangle([rx + 10, ry - 8, rx + rw - 10, ry + 12], radius=6, fill=(45, 50, 55), outline=(65, 70, 75), width=2)
draw.rectangle([rx + 60, ry + 40, rx + rw - 60, ry + 55], fill=(55, 62, 65))
draw.rectangle([rx + 60, ry + 90, rx + rw - 60, ry + 105], fill=(55, 62, 65))
draw.rectangle([rx + 60, ry + rh - 60, rx + rw - 60, ry + rh - 45], fill=(55, 62, 65))
draw.text((W // 2, H - 18), "PVC 高分子防水卷材", fill=(160, 170, 180), anchor="mt", font_size=14)
img = add_noise(img, 6)
img.save(os.path.join(OUT_DIR, "waterproof_membrane.jpg"), quality=92)
print("5/6 Waterproof membrane done")

# -------------------------------------------------
# 6. PU sealant (tube/cartridge)
# -------------------------------------------------
img = Image.new("RGB", (W, H), (65, 55, 50))
draw = ImageDraw.Draw(img)
gradient(draw, 0, 0, W, H, (85, 72, 65), (55, 45, 40))
tw, th = 160, 260
tx, ty = (W - tw) // 2, (H - th) // 2
draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=16, fill=(195, 175, 155), outline=(215, 195, 175), width=3)
draw.rounded_rectangle([tx + 50, ty - 30, tx + tw - 50, ty], radius=6, fill=(180, 160, 140), outline=(200, 180, 160), width=2)
draw.rounded_rectangle([tx + 15, ty + 50, tx + tw - 15, ty + 180], radius=8, fill=(220, 200, 180), outline=(200, 180, 160), width=1)
draw.text((W // 2, ty + 90), "PU", fill=(80, 60, 50), anchor="mt", font_size=36)
draw.text((W // 2, ty + 125), "密封胶", fill=(80, 60, 50), anchor="mt", font_size=20)
for i in range(5):
    y = ty + th - 35 + i * 7
    draw.line([(tx + 20, y), (tx + tw - 20, y)], fill=(170, 155, 140), width=1)
draw.text((W // 2, H - 18), "聚氨酯密封胶", fill=(180, 170, 160), anchor="mt", font_size=14)
img = add_noise(img, 4)
img.save(os.path.join(OUT_DIR, "pu_sealant.jpg"), quality=92)
print("6/6 PU sealant done")

print("\nAll 6 images generated successfully!")
