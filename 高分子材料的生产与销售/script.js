/* ============================================
   高分子材料生产与销售 - 共享脚本 v2
   ============================================ */

// ---- 产品数据 ----
const products = [
  {
    id: 1,
    name: "高分子聚乙烯板材",
    spec: "HDPE-1000×2000×10mm",
    desc: "高密度聚乙烯板材，耐酸碱、耐冲击，广泛用于化工、食品、建筑行业。",
    price: 268.00,
    unit: "张",
    img: "images/hdpe_sheet.jpg"
  },
  {
    id: 2,
    name: "聚丙烯管材",
    spec: "PP-R DN25×4.2mm",
    desc: "优质聚丙烯管材，耐高温、耐腐蚀，适用于给排水及化工流体输送。",
    price: 45.50,
    unit: "米",
    img: "images/pp_pipe.jpg"
  },
  {
    id: 3,
    name: "聚碳酸酯板材",
    spec: "PC-2100×12000×6mm",
    desc: "高透光聚碳酸酯实心板，抗冲击强度是玻璃的250倍，用于采光顶棚、隔断。",
    price: 185.00,
    unit: "张",
    img: "images/pc_sheet.jpg"
  },
  {
    id: 4,
    name: "工程塑料粒子",
    spec: "PA6-GF30 25kg/袋",
    desc: "玻纤增强尼龙6粒子，高强度、高刚性，适用于注塑成型各类工程部件。",
    price: 32.00,
    unit: "公斤",
    img: "images/plastic_pellets.jpg"
  },
  {
    id: 5,
    name: "高分子防水卷材",
    spec: "PVC-P 1.5mm×2m×20m",
    desc: "聚氯乙烯防水卷材，优异的耐候性和防水性能，适用于屋面、地下工程。",
    price: 56.00,
    unit: "平方米",
    img: "images/waterproof_membrane.jpg"
  },
  {
    id: 6,
    name: "聚氨酯密封胶",
    spec: "PU-SL 600ml/支",
    desc: "单组分聚氨酯密封胶，高强度粘接，弹性好，广泛用于建筑接缝密封。",
    price: 38.00,
    unit: "支",
    img: "images/pu_sealant.jpg"
  }
];

// ---- 购物车操作 ----
function getCart() {
  try { return JSON.parse(localStorage.getItem("polymerCart")) || []; }
  catch { return []; }
}

function saveCart(cart) {
  localStorage.setItem("polymerCart", JSON.stringify(cart));
  updateCartBadge();
}

function addToCart(productId, quantity) {
  if (!quantity || quantity < 1) quantity = 1;
  let cart = getCart();
  const existing = cart.find(item => item.id === productId);
  if (existing) {
    existing.qty += quantity;
  } else {
    const prod = products.find(p => p.id === productId);
    if (!prod) return;
    cart.push({ id: productId, name: prod.name, price: prod.price, unit: prod.unit, qty: quantity });
  }
  saveCart(cart);
  showToast("已加入购物车：" + products.find(p => p.id === productId).name);
}

function removeFromCart(productId) {
  let cart = getCart().filter(item => item.id !== productId);
  saveCart(cart);
  renderCart();
}

function updateCartQty(productId, qty) {
  let cart = getCart();
  const item = cart.find(i => i.id === productId);
  if (item) {
    qty = parseInt(qty) || 1;
    if (qty < 1) qty = 1;
    item.qty = qty;
  }
  saveCart(cart);
  renderCart();
}

function getCartTotal() {
  return getCart().reduce((sum, item) => sum + item.price * item.qty, 0);
}

function getCartCount() {
  return getCart().reduce((sum, item) => sum + item.qty, 0);
}

function updateCartBadge() {
  document.querySelectorAll(".cart-count").forEach(el => {
    const count = getCartCount();
    el.textContent = count;
    el.style.display = count > 0 ? "flex" : "none";
  });
}

// ---- AI 图片生成功能 ----
function openAiGenerator(productName) {
  const modal = document.getElementById("ai-gen-modal");
  if (!modal) return;
  modal.classList.add("show");
  document.getElementById("ai-gen-prompt").value = "高质量产品摄影、工业产品图，" + productName + "，白色背景，真实质感";
  document.getElementById("ai-gen-result").innerHTML = "";
  document.getElementById("ai-gen-product").value = productName;
}

function closeAiGenerator() {
  document.getElementById("ai-gen-modal").classList.remove("show");
}

function generateAiImage() {
  const prompt = document.getElementById("ai-gen-prompt").value.trim();
  if (!prompt) return;
  const result = document.getElementById("ai-gen-result");
  result.innerHTML = '<div style="background:var(--bg-light);border:1px solid var(--border);border-radius:6px;padding:16px;margin-top:12px"><p style="font-weight:600;margin-bottom:8px">提示词已生成：</p><code style="display:block;padding:10px;background:#fff;border:1px solid var(--border);border-radius:4px;font-size:0.85rem;line-height:1.6;word-break:break-all">' + prompt + '</code><p style="font-size:0.82rem;color:var(--text-muted);margin-top:8px">复制上方提示词，粘贴到 AI 图像生成工具（如 DALL·E）中使用。</p></div>';
}

// ---- 订单操作 ----
function generateOrderId() {
  return "ORD-" + Date.now().toString(36).slice(-4).toUpperCase() + Math.random().toString(36).slice(2, 6).toUpperCase();
}

function placeOrder(orderData) {
  const orders = getOrders();
  orderData.id = generateOrderId();
  orderData.time = new Date().toLocaleString("zh-CN", { hour12: false });
  orderData.items = getCart();
  orderData.itemNames = orderData.items.map(i => i.name).join("、");
  orderData.total = getCartTotal();
  orderData.status = "已付款";
  orders.unshift(orderData);
  localStorage.setItem("polymerOrders", JSON.stringify(orders));
  localStorage.removeItem("polymerCart");
  updateCartBadge();
  return orderData;
}

function getOrders() {
  try { return JSON.parse(localStorage.getItem("polymerOrders")) || []; }
  catch { return []; }
}

// ---- Toast 提示 ----
function showToast(msg, isError) {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = msg;
  el.className = "toast" + (isError ? " error" : "");
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 2800);
}

// ---- 渲染产品列表 ----
function renderProducts(filterId) {
  const el = document.getElementById("product-list");
  if (!el) return;
  const list = filterId
    ? products.filter(p => p.id === filterId)
    : products;
  el.innerHTML = list.map((p, idx) => `
    <div class="card animate-on-scroll" style="animation-delay:${idx * 0.1}s">
      <div class="card-img-wrapper">
        <span class="card-img-badge">热卖</span>
      </div>
      <img class="card-img" src="${p.img}" alt="${p.name}" loading="lazy">
      <div class="card-body">
        <h3>${p.name}</h3>
        <p>${p.desc}</p>
        <p style="font-size:0.82rem;color:var(--text-light)">规格：${p.spec}</p>
        <div class="price">¥${p.price.toFixed(2)} / ${p.unit}</div>
        <div class="card-actions">
          <div class="qty-control">
            <button class="qty-btn" onclick="adjustQty(${p.id},-1)">−</button>
            <input type="number" id="qty-${p.id}" value="1" min="1" readonly>
            <button class="qty-btn" onclick="adjustQty(${p.id},1)">+</button>
          </div>
          <button class="btn btn-primary btn-sm" onclick="addToCart(${p.id}, parseInt(document.getElementById('qty-${p.id}').value))">加入购物车</button>
        </div>
      </div>
    </div>
  `).join("");
}

function adjustQty(id, delta) {
  const input = document.getElementById("qty-" + id);
  if (!input) return;
  let val = parseInt(input.value) || 1;
  val += delta;
  if (val < 1) val = 1;
  if (val > 999) val = 999;
  input.value = val;
}

// ---- 渲染购物车 ----
function renderCart() {
  const el = document.getElementById("cart-items");
  if (!el) return;
  const cart = getCart();
  if (cart.length === 0) {
    el.innerHTML = '<div class="empty-state animate-on-scroll"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg><h3>购物车是空的</h3><p>去产品页面选购商品吧</p><a href="products.html" class="btn btn-primary" style="margin-top:12px">去选购</a></div>';
    const totalEl = document.getElementById("cart-total");
    if (totalEl) totalEl.innerHTML = "";
    return;
  }
  el.innerHTML = cart.map(item => `
    <div class="cart-item animate-on-scroll">
      <div class="cart-item-info">
        <h4>${item.name}</h4>
        <p>¥${item.price.toFixed(2)} / ${item.unit}</p>
      </div>
      <div class="cart-item-actions">
        <input type="number" value="${item.qty}" min="1" onchange="updateCartQty(${item.id}, this.value)">
        <span style="font-weight:700;min-width:70px;text-align:right">¥${(item.price * item.qty).toFixed(2)}</span>
        <button class="btn btn-danger btn-sm" onclick="removeFromCart(${item.id})">删除</button>
      </div>
    </div>
  `).join("");
  const totalEl = document.getElementById("cart-total");
  if (totalEl) {
    totalEl.innerHTML = '<div class="cart-total animate-on-scroll">合计：<span>¥' + getCartTotal().toFixed(2) + '</span></div>';
  }
}

// ---- 渲染订单表格 ----
function renderOrders() {
  const el = document.getElementById("orders-table-body");
  if (!el) return;
  const orders = getOrders();
  if (orders.length === 0) {
    el.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-light)">暂无订单记录</td></tr>';
    return;
  }
  el.innerHTML = orders.map((o, idx) => {
    const itemsStr = o.items.map(i => i.name + " × " + i.qty).join("；");
    return '<tr class="animate-on-scroll" style="animation-delay:' + (idx * 0.05) + 's">' +
      '<td><span class="order-id-badge">' + o.id + '</span></td>' +
      '<td>' + itemsStr + '</td>' +
      '<td>' + o.phone + '</td>' +
      '<td>' + o.address + '</td>' +
      '<td>¥' + o.total.toFixed(2) + '</td>' +
      '<td>' + o.time + '</td>' +
      '<td><span class="status-badge status-paid">' + o.status + '</span></td>' +
      '</tr>';
  }).join("");
}

// ---- 提交订单 ----
function submitOrder(event) {
  event.preventDefault();
  const form = document.getElementById("order-form");
  const data = {
    phone: form.phone.value.trim(),
    address: form.address.value.trim(),
    payment: form.payment.value,
    contact: form.contact.value.trim()
  };
  if (!data.contact) { showToast("请填写联系人姓名", true); return; }
  if (!data.phone || !/^1\d{10}$/.test(data.phone)) { showToast("请填写有效的手机号码", true); return; }
  if (!data.address) { showToast("请填写送货地址", true); return; }
  if (getCartCount() === 0) { showToast("购物车为空，请先选购商品", true); return; }
  const order = placeOrder(data);
  showToast("订单提交成功！订单号：" + order.id);
  renderCart();
  setTimeout(function() { window.location.href = "orders.html"; }, 1000);
}

// ---- 滚动动画检测 ----
function initScrollAnimation() {
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });

  document.querySelectorAll(".animate-on-scroll, .card, .feature, .process-step, section").forEach(function(el) {
    if (!el.classList.contains("no-animate")) {
      observer.observe(el);
    }
  });
}

// ---- 统计数字动画 ----
function animateCounter(el, target, suffix) {
  var current = 0;
  var step = Math.ceil(target / 40);
  var timer = setInterval(function() {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = current.toLocaleString() + (suffix || "");
  }, 30);
}

function initCounters() {
  document.querySelectorAll("[data-count]").forEach(function(el) {
    var target = parseInt(el.dataset.count);
    if (!isNaN(target)) animateCounter(el, target, el.dataset.suffix || "");
  });
}

// ---- 页面初始化 ----
document.addEventListener("DOMContentLoaded", function() {
  updateCartBadge();

  // 导航高亮
  var page = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach(function(a) {
    if (a.getAttribute("href") === page) a.classList.add("active");
  });

  // 移动端汉堡菜单
  var hamburger = document.querySelector(".hamburger");
  var navLinks = document.querySelector(".nav-links");
  if (hamburger && navLinks) {
    hamburger.addEventListener("click", function() { navLinks.classList.toggle("open"); });
    document.addEventListener("click", function(e) {
      if (!e.target.closest(".navbar")) navLinks.classList.remove("open");
    });
  }

  // 产品页
  if (document.getElementById("product-list")) renderProducts();

  // 滚动动画
  setTimeout(initScrollAnimation, 150);

  // 关闭 AI 生成弹窗
  document.addEventListener("click", function(e) {
    var modal = document.getElementById("ai-gen-modal");
    if (modal && e.target === modal) closeAiGenerator();
  });

  // 键盘 ESC 关闭弹窗
  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") closeAiGenerator();
  });

  // 统计数字动画（首页）
  if (document.getElementById("counter-section")) initCounters();

  // 购物车/结算页
  if (document.getElementById("cart-items")) renderCart();
  var orderForm = document.getElementById("order-form");
  if (orderForm) orderForm.addEventListener("submit", submitOrder);

  // 订单页
  if (document.getElementById("orders-table-body")) renderOrders();
});
