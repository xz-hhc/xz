import re

# Update products.html - add AI gen nav link and modal
with open('products.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add AI nav button
content = content.replace(
    '<li><a href="products.html">产品中心</a></li>',
    '<li><a href="products.html">产品中心</a></li>\n      <li><a href="#" onclick="event.preventDefault();openAiGenerator(\'\')" style="background:linear-gradient(135deg,var(--accent),#e67e22);color:#fff;padding:8px 12px;border-radius:6px;font-weight:700">AI 生图</a></li>'
)

modal_html = '\n<!-- AI 图片生成弹窗 -->\n<div id="ai-gen-modal" class="modal-overlay">\n  <div class="modal-content">\n    <div class="modal-header">\n      <h2>AI 产品图生成器</h2>\n      <button class="modal-close" onclick="closeAiGenerator()">&times;</button>\n    </div>\n    <div class="modal-body">\n      <p style="color:var(--text-muted);font-size:0.9rem;margin-bottom:16px">\n        使用 AI 为产品生成高质量展示图片。输入提示词即可获得可复制到图像生成工具中使用的描述。\n      </p>\n      <div class="form-group">\n        <label for="ai-gen-product">产品名称</label>\n        <input type="text" id="ai-gen-product" class="form-control" placeholder="输入产品名称">\n      </div>\n      <div class="form-group">\n        <label for="ai-gen-prompt">AI 提示词</label>\n        <textarea id="ai-gen-prompt" class="form-control" rows="4" placeholder="描述您想要的图片效果..."></textarea>\n      </div>\n      <button class="btn btn-primary" onclick="generateAiImage()" style="width:100%">生成提示词</button>\n      <div id="ai-gen-result" style="margin-top:12px"></div>\n    </div>\n    <div class="modal-footer">\n      <p style="font-size:0.78rem;color:var(--text-light)">生成的提示词可直接用于 DALL·E、Midjourney 等 AI 图像生成工具</p>\n    </div>\n  </div>\n</div>\n'

content = content.replace('<div id="toast" class="toast"></div>', modal_html + '<div id="toast" class="toast"></div>')

with open('products.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('products.html updated')

# Update index.html - add counter section and other animations
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

counter_html = '\n<section class="section" id="counter-section">\n  <div class="container">\n    <div class="counter-section">\n      <div class="counter-item">\n        <h3 data-count="15" data-suffix="年">0</h3>\n        <p>行业经验</p>\n      </div>\n      <div class="counter-item">\n        <h3 data-count="50000" data-suffix="+">0</h3>\n        <p>服务客户</p>\n      </div>\n      <div class="counter-item">\n        <h3 data-count="200" data-suffix="+">0</h3>\n        <p>产品种类</p>\n      </div>\n      <div class="counter-item">\n        <h3 data-count="98" data-suffix="%">0</h3>\n        <p>客户满意度</p>\n      </div>\n    </div>\n  </div>\n</section>\n'

content = content.replace(
    '<section class="section" style="background:#fff">',
    counter_html + '<section class="section" style="background:#fff">',
    1
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('index.html updated')

# Update checkout.html - add some animation classes
for page in ['index.html', 'production.html', 'products.html', 'checkout.html', 'orders.html']:
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    # Add animate-on-scroll class to page-header
    content = content.replace(
        '<div class="page-header">',
        '<div class="page-header animate-on-scroll">',
        1
    )
    with open(page, 'w', encoding='utf-8') as f:
        f.write(content)
    print(page + ' - animations added')

print('All pages updated!')
