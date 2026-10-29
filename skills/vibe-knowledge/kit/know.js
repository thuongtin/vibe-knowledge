// Bộ thành phần phim ngắn tri thức (vibe-knowledge): đẩy kéo ảnh minh hoạ, từ khoá, bộ đếm, chú thích nguồn, nút lựa chọn, mở đầu series, cổ văn dọc,
// vệt sáng, lan toả bản đồ, so sánh cột, thẻ chương. Tất cả là "hàm thuần tuý của thời gian t": khi build thì dựng DOM, trong render đặt trạng thái theo t, không phụ thuộc khung hình trước.
// Cách cài: tools/new_film.py sẽ sao chép tệp này vào <series>/cine/engine/know.js; trong film.js
//   import { TH, bg, layers, plate, vclip, keyword, counter, foot, foots, choice, seriesCard, vquote, trail, spread, bars, chapter, ask } from "../../cine/engine/know.js";
import { el, css, clamp, lerp, inv, eOutCubic, eInOutCubic, eOutQuint, spring, rng } from "./util.js";

// ── Hệ thống hình ảnh (tương ứng references/03-visual-systems.md) ──
export const TH = {
  starfield: { bg: 0x05070d, ink: "#eef0f6", dim: "#8a90a3", accent: "#f2c46d", accent2: "#7fb8ff", line: "rgba(242,196,109,0.55)", font: "NotoSC" },
  gufeng:    { bg: 0x140d0b, ink: "#f3e6cc", dim: "#a8977c", accent: "#d9472b", accent2: "#e2b45a", line: "rgba(226,180,90,0.6)", font: "NotoSC" },
  darkgold:  { bg: 0x0b0a08, ink: "#f4ead6", dim: "#9c917c", accent: "#f0b44c", accent2: "#ff6a3d", line: "rgba(240,180,76,0.6)", font: "NotoSC" },
  paper:     { bg: 0xece4d4, ink: "#2a2420", dim: "#7d7266", accent: "#b23a2e", accent2: "#3c6e71", line: "rgba(42,36,32,0.5)", font: "NotoSC", light: true },
  pixel:     { bg: 0x10122a, ink: "#f8f4e3", dim: "#9aa0c8", accent: "#ffd23f", accent2: "#3fe0a0", line: "rgba(255,210,63,0.7)", font: "NotoSC" },
};

// Gọi ở đầu mỗi ống kính: xoá lớp cảnh WebGL về màu nền của chủ đề (ống kính không vẽ hạt cũng phải xoá, nếu không sẽ còn sót hình của ống kính trước)
export function bg(ctx, theme, o = {}) {
  ctx.r.setRenderTarget(ctx.post.sceneRT);
  ctx.r.setClearColor(o.color ?? theme.bg, 1);
  ctx.r.clear();
  Object.assign(ctx.post.params, { bloom: o.bloom ?? 0.5, grain: o.grain ?? 0.02, vig: o.vig ?? 0.5 });
}

const fadeIO = (t, a, b, fi = 0.5, fo = 0.5) => clamp((t - a) / fi) * (1 - clamp((t - (b - fo)) / fo));

// Đồng bộ khi quay: khi ảnh, khung hình video chưa giải mã xong thì đăng ký ở đây; record.py / stills.py sau mỗi lần seek đều await window.__vk.wait() rồi mới chụp
// (tools/new_film.py khi tạo series đã vá sẵn cho hai công cụ này)
const VK = (window.__vk ||= { pend: [], async wait() { while (this.pend.length) { const ps = this.pend.splice(0); await Promise.all(ps.map((f) => f())); } } });
const decodeLater = (src) => { const im = new Image(); im.src = src; const p = im.decode().catch(() => {}); VK.pend.push(() => p); return im; };

// Đường dẫn tài nguyên: trong film.js viết const A = (f) => new URL(`./assets/${f}`, import.meta.url).href;  plate({ src: A("a01.jpg") })

// ── Ảnh minh hoạ (ảnh do Renoise tạo): đẩy kéo lia dịch (Ken Burns) + mờ vào mờ ra + tối góc + nhãn góc "Hình minh hoạ AI" tuỳ chọn ──
// p = plate(s, { src: "assets/a01.jpg", x:0, y:0, w:1920, h:1080, ai: true, radius: 0, shade: 0.35 })
// p.update(t, t0, t1, { from: [1.06, 0, 0], to: [1.14, -40, 10], fi: 0.6, fo: 0.6 })   // [thu phóng, dịch x, dịch y]
export function plate(parent, { src, x = 0, y = 0, w = 1920, h = 1080, ai = true, radius = 0, shade = 0.35, pos = "50% 50%", tag = "Hình minh hoạ AI" }) {
  decodeLater(src);
  const box = el(parent, "abs", `left:${x}px;top:${y}px;width:${w}px;height:${h}px;overflow:hidden;border-radius:${radius}px;`);
  const img = el(box, "abs",`left:0;top:0;width:${w}px;height:${h}px;background:#000 url(${src}) ${pos}/cover no-repeat;will-change:transform;`);
  el(box, "abs", `inset:0;background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,${shade}) 100%),linear-gradient(180deg, rgba(0,0,0,0) 62%, rgba(0,0,0,${shade + 0.25}) 100%);`);
  const lab = ai ? el(box, "abs mono", "right:22px;top:18px;font-size:15px;letter-spacing:2px;color:rgba(255,255,255,0.55);background:rgba(0,0,0,0.28);padding:3px 10px;border-radius:6px;", tag) : null;
  return { box, img, lab,
    update(t, t0, t1, o = {}) {
      const { from = [1.04, 0, 0], to = [1.12, 0, 0], fi = 0.6, fo = 0.6, ease = eInOutCubic } = o;
      const k = ease(inv(t, t0, t1));
      const s = lerp(from[0], to[0], k), dx = lerp(from[1], to[1], k), dy = lerp(from[2], to[2], k);
      css(img, { transform: `translate(${dx.toFixed(2)}px,${dy.toFixed(2)}px) scale(${s.toFixed(4)})` });
      const a = fadeIO(t, t0, t1, fi, fo);
      css(box, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
      return a;
    } };
}

// ── Tranh minh hoạ nhiều lớp (chủ lực của bản cơ bản): Opus viết thẳng SVG / ảnh cục bộ chia thành vài lớp, dịch chuyển thị sai theo độ sâu, thay cho ảnh AI ──
// sc = layers(s, [{ svg: "<svg viewBox='0 0 1920 1080'>…núi xa…</svg>", depth: 0.2 }, { svg: lớp giữa, depth: 0.6 }, { src: A("img/x.png"), depth: 1 }])
// sc.update(t, t0, t1, { pan: [-80, 0], zoom: [1, 1.06], fi, fo })   lớp gần dịch nhiều, lớp xa dịch ít
export function layers(parent, list, { x = 0, y = 0, w = 1920, h = 1080 } = {}) {
  const box = el(parent, "abs", `left:${x}px;top:${y}px;width:${w}px;height:${h}px;overflow:hidden;`);
  const ls = list.map((L) => {
    if (L.src) decodeLater(L.src);
    const d = el(box, "abs", `left:${-w * 0.05}px;top:${-h * 0.05}px;width:${w * 1.1}px;height:${h * 1.1}px;will-change:transform;${L.src ? `background:url(${L.src}) center/${L.fit || "cover"} no-repeat;` : ""}`, L.svg || "");
    const sv = d.querySelector("svg"); if (sv) { sv.setAttribute("width", "100%"); sv.setAttribute("height", "100%"); sv.setAttribute("preserveAspectRatio", L.par || "xMidYMid slice"); }
    return { d, depth: L.depth ?? 1 };
  });
  return { box, ls,
    update(t, t0, t1, o = {}) {
      const { pan = [-60, 0], zoom = [1, 1.05], fi = 0.5, fo = 0.5, ease = eInOutCubic } = o;
      const k = ease(inv(t, t0, t1)), z = lerp(zoom[0], zoom[1], k);
      for (const { d, depth } of ls) css(d, { transform: `translate(${(pan[0] * k * depth).toFixed(2)}px,${(pan[1] * k * depth).toFixed(2)}px) scale(${(1 + (z - 1) * depth).toFixed(4)})` });
      const a = fadeIO(t, t0, t1, fi, fo);
      css(box, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
      return a;
    } };
}

// ── Ống kính động (video do Renoise tạo): tools/clip2frames.py tách thành chuỗi khung hình, ở đây vẽ từng khung lên canvas theo thời gian ──
// Phụ đề, chú thích nguồn, từ khoá đều nằm trên nó (lớp clips của finish.py chồng ở trên cùng, sẽ đè lên phụ đề, B-roll toàn màn hình đều dùng vclip).
// v = vclip(s, { dir: A("clips/v01"), n: 241, fps: 30 }); v.update(t, t0, t1, { rate: 1, from: [1, 0, 0], to: [1.06, 0, 0], loop: false })
export function vclip(parent, { dir, n, fps = 30, ext = "jpg", x = 0, y = 0, w = 1920, h = 1080, ai = true, tag = "Hình ảnh do AI tạo", shade = 0.3, keep = 45 }) {
  const box = el(parent, "abs", `left:${x}px;top:${y}px;width:${w}px;height:${h}px;overflow:hidden;`);
  const cv = document.createElement("canvas"); cv.width = w; cv.height = h; cv.style.cssText = `position:absolute;left:0;top:0;width:${w}px;height:${h}px;`;
  box.appendChild(cv);
  el(box, "abs", `inset:0;background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 50%, rgba(0,0,0,${shade}) 100%),linear-gradient(180deg, rgba(0,0,0,0) 62%, rgba(0,0,0,${shade + 0.25}) 100%);`);
  if (ai) el(box, "abs mono", "right:22px;top:18px;font-size:15px;letter-spacing:2px;color:rgba(255,255,255,0.55);background:rgba(0,0,0,0.28);padding:3px 10px;border-radius:6px;", tag);
  const g = cv.getContext("2d"), cache = new Map();
  const url = (i) => `${dir}/${String(i + 1).padStart(4, "0")}.${ext}`;
  const get = (i) => { let im = cache.get(i); if (!im) { im = new Image(); im.src = url(i); im._p = im.decode().catch(() => {}); cache.set(i, im); } return im; };
  decodeLater(url(0));
  let want = -1, view = [1, 0, 0];
  const paint = (im) => {
    const [s, dx, dy] = view, r = Math.max(w / im.naturalWidth, h / im.naturalHeight) * s;
    const dw = im.naturalWidth * r, dh = im.naturalHeight * r;
    g.drawImage(im, (w - dw) / 2 + dx, (h - dh) / 2 + dy, dw, dh);
  };
  return { box, cv,
    update(t, t0, t1, o = {}) {
      const { rate = 1, from = [1, 0, 0], to = [1.05, 0, 0], loop = false, fi = 0.5, fo = 0.5, at0 = 0 } = o;
      const a = fadeIO(t, t0, t1, fi, fo);
      css(box, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
      if (a <= 0.001) return a;
      const k = eInOutCubic(inv(t, t0, t1));
      view = [lerp(from[0], to[0], k), lerp(from[1], to[1], k), lerp(from[2], to[2], k)];
      let i = Math.floor((t - t0) * fps * rate + at0 * fps);
      i = loop ? ((i % n) + n) % n : clamp(i, 0, n - 1);
      want = i;
      for (const key of cache.keys()) if (key < i - 5 || key > i + keep) cache.delete(key);
      for (let j = 1; j <= 12; j++) if (i + j < n) get(i + j);          // tải trước vài khung hình tiếp theo
      const im = get(i);
      if (im.complete && im.naturalWidth) paint(im);
      else VK.pend.push(async () => { await im._p; if (want === i && im.naturalWidth) paint(im); });
      return a;
    } };
}

// ── Từ khoá: chữ trên màn hình chỉ đặt từ khoá (≤8 ký tự), lời dẫn đã có phụ đề ──
export function keyword(parent, text, { x = 960, y = 420, size = 120, color = "#f6f2ea", weight = 900, align = "center", sub = "", subColor = "#bdb6aa", glow = "" } = {}) {
  const plain = text.replace(/<[^>]+>/g, "");
  if (plain.length > 8) console.warn(`Từ khoá vượt quá 8 ký tự: ${plain}`);
  const left = align === "center" ? `left:${x - 900}px;width:1800px;text-align:center;` : `left:${x}px;`;
  const k = el(parent, "abs cn", `${left}top:${y}px;font-size:${size}px;line-height:1.15;font-weight:${weight};color:${color};white-space:nowrap;letter-spacing:${size > 90 ? 6 : 2}px;${glow ? `text-shadow:0 0 40px ${glow};` : ""}`, text);
  const s = sub ? el(parent, "abs cn", `${left}top:${y + size * 1.25}px;font-size:${Math.round(size * 0.28)}px;color:${subColor};white-space:nowrap;letter-spacing:3px;`, sub) : null;
  return { k, s,
    update(t, at, out = null, o = {}) {
      const { scale = 0.06, blur = 8, dy = 0 } = o;
      const kk = eOutCubic(clamp((t - at) / 0.35)), ko = out == null ? 0 : clamp((t - out) / 0.25);
      const a = kk * (1 - ko);
      css(k, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden", transform: `translateY(${((1 - kk) * dy).toFixed(1)}px) scale(${(1 + (1 - kk) * scale).toFixed(4)})`, filter: `blur(${((1 - kk) * blur + ko * 6).toFixed(2)}px)` });
      if (s) { const ks = eOutCubic(clamp((t - at - 0.25) / 0.35)) * (1 - ko); css(s, { opacity: ks.toFixed(3), visibility: ks > 0.001 ? "visible" : "hidden" }); }
    } };
}

// ── Bộ đếm: kiểu "con số cuộn lên" như 83 → 328 → 390 ──
// c = counter(s, { x, y, size, color, label: "Tử tù được cho về nhà", suffix: " người" }); c.update(t, [[T0, 0], [T1, 83], [T2, 328], [T3, 390]])
export function counter(parent, { x = 960, y = 400, size = 150, color = "#f6f2ea", label = "", suffix = "", labelColor = "#bdb6aa", align = "center", decimals = 0, font = "Geist" } = {}) {
  const pos = align === "center" ? `left:${x - 700}px;width:1400px;text-align:center;` : `left:${x}px;`;
  const lab = label ? el(parent, "abs cn", `${pos}top:${y - 50}px;font-size:32px;color:${labelColor};letter-spacing:4px;`, label) : null;
  const n = el(parent, "abs", `${pos}top:${y}px;font-family:${font};font-variant-numeric:tabular-nums;font-size:${size}px;line-height:1;font-weight:800;color:${color};white-space:nowrap;`);
  return { lab, n,
    update(t, keys, o = {}) {           // keys: [[thời gian, giá trị], …], giữa hai điểm liền kề thì chuyển động mượt
      const { out = null } = o;
      let v = keys[0][1];
      for (let i = 1; i < keys.length; i++) if (t >= keys[i - 1][0]) v = lerp(keys[i - 1][1], keys[i][1], eOutQuint(clamp((t - keys[i - 1][0]) / Math.max(0.2, Math.min(1.2, keys[i][0] - keys[i - 1][0])))));
      const txt = v.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix;
      if (n.textContent !== txt) n.textContent = txt;
      const a = clamp((t - keys[0][0]) / 0.3) * (out == null ? 1 : 1 - clamp((t - out) / 0.25));
      css(n, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
      if (lab) css(lab, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
    } };
}

// ── Chú thích nguồn: một dòng chữ nhỏ dưới phụ đề (y≈1046), mỗi ống kính dữ kiện đều phải có; hình minh hoạ ghi rõ "chỉ mang tính minh hoạ" ──
// const f = foot(root); trong ống kính f.show(t, at, out, "Tư trị thông giám, quyển 194: 'Dù cho về nhà, hẹn mùa thu năm sau đến chịu chết'")
export function foot(parent, { color = "rgba(230,224,212,0.7)", y = 1043 } = {}) {
  const n = el(parent, "abs cn", `left:120px;width:1680px;top:${y}px;text-align:center;font-size:19px;line-height:26px;color:${color};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;z-index:60;pointer-events:none;`);
  return { n,
    show(t, at, out, text) {
      if (t < at || t >= out) return false;
      if (n.textContent !== text) n.textContent = text;
      const a = clamp((t - at) / 0.3) * (1 - clamp((t - (out - 0.25)) / 0.25));
      css(n, { opacity: a.toFixed(3), visibility: "visible" });
      return true;
    },
    hide() { css(n, { opacity: "0", visibility: "hidden" }); } };
}
// Nhiều chú thích xếp thành bảng: foots(f, t, [[bắt đầu, kết thúc, chữ], …]), cùng một thời điểm chỉ hiển thị một mục
export function foots(f, t, list) { for (const [a, b, s] of list) if (f.show(t, a, b, s)) return; f.hide(); }

// ── Nút lựa chọn lưỡng nan: "Quay về / Không quay về", dùng để đặt câu hỏi ở cuối ──
export function choice(parent, options, { y = 690, w = 360, gap = 60, colors = ["#d9472b", "#3c6e9a"] } = {}) {
  const total = options.length * w + (options.length - 1) * gap, x0 = 960 - total / 2;
  const bs = options.map(([main, sub], i) => el(parent, "abs", `left:${x0 + i * (w + gap)}px;top:${y}px;width:${w}px;height:150px;border-radius:20px;background:${colors[i % colors.length]};box-shadow:0 20px 60px rgba(0,0,0,0.45), inset 0 -6px 0 rgba(0,0,0,0.25);display:flex;flex-direction:column;align-items:center;justify-content:center;`,
    `<div class="cn" style="font-size:64px;font-weight:900;color:#fff;letter-spacing:8px">${main}</div>${sub ? `<div class="cn" style="font-size:22px;color:rgba(255,255,255,0.8);margin-top:4px">${sub}</div>` : ""}`));
  return { bs,
    update(t, at, o = {}) {
      const { pick = -1, pickAt = Infinity, out = null } = o;
      bs.forEach((b, i) => {
        const k = spring(t - at - i * 0.12, 2.4, 0.5), ko = out == null ? 0 : clamp((t - out) / 0.25);
        const picked = pick === i && t >= pickAt, dim = pick >= 0 && pick !== i && t >= pickAt;
        css(b, { opacity: String(clamp(k) * (1 - ko) * (dim ? 0.35 : 1)), visibility: t >= at ? "visible" : "hidden",
          transform: `translateY(${((1 - clamp(k)) * 40).toFixed(1)}px) scale(${(picked ? 1.08 : 1).toFixed(3)})` });
      });
    } };
}

// ── Mở đầu series: "Nếu bạn sống ở thời cổ đại · Tập 3" ──
export function seriesCard(parent, { series, ep, title, theme }) {
  const c = el(parent, "abs", "left:0;top:0;width:1920px;height:1080px;");
  const s1 = el(c, "abs cn", `left:0;width:1920px;top:360px;text-align:center;font-size:30px;letter-spacing:14px;color:${theme.dim};`, `${series}${ep ? ` · Tập ${ep}` : ""}`);
  const line = el(c, "abs", `left:860px;top:420px;width:200px;height:2px;background:${theme.accent};transform-origin:50% 50%;`);
  const t1 = el(c, "abs cn", `left:0;width:1920px;top:450px;text-align:center;font-size:112px;font-weight:900;color:${theme.ink};letter-spacing:10px;`, title);
  return { c,
    update(t, at, out) {
      const a = clamp((t - at) / 0.4) * (1 - clamp((t - out + 0.35) / 0.35));
      css(c, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
      css(line, { transform: `scaleX(${eOutCubic(clamp((t - at - 0.1) / 0.6)).toFixed(3)})` });
      css(t1, { filter: `blur(${(8 * (1 - eOutCubic(clamp((t - at - 0.2) / 0.5)))).toFixed(2)}px)`, transform: `scale(${(1 + 0.05 * (1 - eOutCubic(clamp((t - at - 0.2) / 0.6)))).toFixed(4)})` });
    } };
}

// ── Cổ văn viết dọc: hiện ra từng chữ một, chữ nhỏ nguồn ở góc dưới trái ──
export function vquote(parent, { text, src = "", x = 1500, y = 160, size = 52, color = "#f3e6cc", srcColor = "#a8977c", paper = true }) {
  const cols = text.split("\n");
  const box = el(parent, "abs", `left:${x}px;top:${y}px;${paper ? "padding:40px 34px;background:linear-gradient(180deg,#efe3c8,#e4d3b0);border-radius:6px;box-shadow:0 30px 80px rgba(0,0,0,0.5);" : ""}display:flex;flex-direction:row-reverse;gap:${Math.round(size * 0.45)}px;`);
  const chars = [];
  cols.forEach((col) => {
    const c = el(box, "cn", `writing-mode:vertical-rl;font-size:${size}px;line-height:1.2;font-weight:700;letter-spacing:6px;color:${paper ? "#2a2420" : color};`);
    for (const ch of col) chars.push(el(c, "", "display:inline;opacity:0;", ch));
  });
  const s = src ? el(parent, "abs cn", `left:${x}px;top:${y - 40}px;font-size:22px;color:${srcColor};white-space:nowrap;`, src) : null;
  return { box, s,
    update(t, t0, t1, out = null) {
      const n = Math.floor(chars.length * clamp((t - t0) / Math.max(0.01, t1 - t0)));
      chars.forEach((c, i) => css(c, { opacity: i < n ? "1" : "0" }));
      const a = clamp((t - t0 + 0.3) / 0.3) * (out == null ? 1 : 1 - clamp((t - out) / 0.3));
      css(box, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
      if (s) css(s, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
    } };
}

// ── Vệt sáng: một đường phát sáng lần lượt đi qua N nút (bản mẫu "một mạch chính") ──
// tr = trail(s, { pts: [[x,y],…], labels: ["Lịch sử","Kinh tế",…], color }); tr.update(t, t0, t1)  → đầu đường đi đến đâu, nút sáng đến đó
export function trail(parent, { pts, labels = [], color = "#f0b44c", width = 5, nodeR = 12, labelColor = "#f4ead6", labelSize = 30 }) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "1920"); svg.setAttribute("height", "1080"); svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible";
  parent.appendChild(svg);
  let d = `M${pts[0][0]} ${pts[0][1]}`;
  for (let i = 1; i < pts.length; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], mx = (x0 + x1) / 2; d += ` C${mx} ${y0} ${mx} ${y1} ${x1} ${y1}`; }
  const glow = document.createElementNS(svg.namespaceURI, "path"), p = document.createElementNS(svg.namespaceURI, "path");
  for (const [q, w, o] of [[glow, width * 4, 0.25], [p, width, 1]]) {
    q.setAttribute("d", d); q.setAttribute("fill", "none"); q.setAttribute("stroke", color); q.setAttribute("stroke-width", String(w));
    q.setAttribute("stroke-linecap", "round"); q.setAttribute("opacity", String(o)); svg.appendChild(q);
  }
  const L = p.getTotalLength();
  // Vị trí của mỗi nút trên đường đi (ước lượng theo điểm gần nhất)
  const at = pts.map(([x, y]) => { let best = 0, bd = 1e9; for (let s = 0; s <= L; s += 4) { const q = p.getPointAtLength(s); const dd = (q.x - x) ** 2 + (q.y - y) ** 2; if (dd < bd) { bd = dd; best = s; } } return best / L; });
  const head = el(parent, "abs", `width:${nodeR * 3}px;height:${nodeR * 3}px;border-radius:50%;background:radial-gradient(circle,#fff 0,${color} 35%,rgba(0,0,0,0) 70%);margin:-${nodeR * 1.5}px 0 0 -${nodeR * 1.5}px;`);
  const nodes = pts.map(([x, y], i) => {
    const n = el(parent, "abs", `left:${x - nodeR}px;top:${y - nodeR}px;width:${nodeR * 2}px;height:${nodeR * 2}px;border-radius:50%;border:3px solid ${color};background:#0b0a08;`);
    const lb = labels[i] ? el(parent, "abs cn", `left:${x - 200}px;width:400px;text-align:center;top:${y + (i % 2 ? -nodeR - labelSize - 26 : nodeR + 16)}px;font-size:${labelSize}px;font-weight:800;color:${labelColor};white-space:nowrap;`, labels[i]) : null;
    return { n, lb };
  });
  return { svg, nodes, at,
    update(t, t0, t1, o = {}) {
      const k = (o.ease || eInOutCubic)(inv(t, t0, t1));
      for (const q of [p, glow]) css(q, { strokeDasharray: `${L}`, strokeDashoffset: String(L * (1 - k)) });
      const h = p.getPointAtLength(L * k);
      css(head, { left: `${h.x}px`, top: `${h.y}px`, opacity: k > 0 && k < 1 ? "1" : "0" });
      nodes.forEach(({ n, lb }, i) => {
        const on = k >= at[i] - 0.002;
        css(n, { background: on ? color : "#0b0a08", boxShadow: on ? `0 0 26px ${color}` : "none", opacity: k > 0 || i === 0 ? "1" : "0.4" });
        if (lb) css(lb, { opacity: on ? "1" : "0", transform: `translateY(${on ? 0 : 10}px)` });
      });
      return k;
    } };
}

// ── Lan toả: từ một điểm trung tâm rải ra n điểm khắp xung quanh (tử tù tản về các châu, virus lây lan, thông tin lan truyền). Vẽ trên canvas 2D ──
// sp = spread(s, { cx, cy, n: 390, seed: 7, area: [x0,y0,x1,y1], color }); sp.update(t, t0, t1, { back: 0 })  khi back=1 các điểm lại bay về trung tâm
export function spread(parent, { cx = 960, cy = 540, n = 200, seed = 7, area = [260, 160, 1660, 900], color = "#e2b45a", r = 4, targets = null }) {
  const cv = document.createElement("canvas"); cv.width = 1920; cv.height = 1080; cv.style.cssText = "position:absolute;left:0;top:0;width:1920px;height:1080px;";
  parent.appendChild(cv);
  const g = cv.getContext("2d"), R = rng(seed);
  const tg = targets || Array.from({ length: n }, () => [lerp(area[0], area[2], R()), lerp(area[1], area[3], R())]);
  const dl = tg.map(() => R() * 0.35);
  return { cv, tg,
    update(t, t0, t1, o = {}) {
      const { back = 0, alpha = 1 } = o;
      g.clearRect(0, 0, 1920, 1080);
      if (alpha <= 0) return;
      g.globalAlpha = alpha; g.fillStyle = color; g.shadowColor = color; g.shadowBlur = 10;
      tg.forEach(([x, y], i) => {
        const k = eOutCubic(clamp((inv(t, t0, t1) - dl[i]) / 0.65)) * (1 - back);
        if (k <= 0 && back === 0) return;
        g.beginPath(); g.arc(lerp(cx, x, k), lerp(cy, y, k), r, 0, Math.PI * 2); g.fill();
      });
      g.globalAlpha = 1; g.shadowBlur = 0;
    } };
}

// ── So sánh cột: Benford 1–9, so sánh trước và sau ──
// b = bars(s, { x, y, w, h, values: [30.1,17.6,…], labels: ["1",…,"9"], color, fmt: v => v.toFixed(1)+"%" }); b.update(t, t0, t1)
export function bars(parent, { x = 360, y = 220, w = 1200, h = 560, values, labels = [], color = "#f2c46d", max = null, fmt = (v) => v.toFixed(1), labelColor = "#bdb6aa", valueColor = "#f6f2ea", gap = 0.28 }) {
  const box = el(parent, "abs", `left:${x}px;top:${y}px;width:${w}px;height:${h}px;`);
  const m = max ?? Math.max(...values), bw = w / values.length;
  const cols = values.map((v, i) => {
    const b = el(box, "abs", `left:${i * bw + bw * gap / 2}px;bottom:0;width:${bw * (1 - gap)}px;height:${(v / m) * (h - 60)}px;background:${color};border-radius:8px 8px 0 0;transform-origin:50% 100%;`);
    const vl = el(box, "abs mono", `left:${i * bw}px;width:${bw}px;text-align:center;bottom:${(v / m) * (h - 60) + 10}px;font-size:26px;color:${valueColor};`, fmt(v));
    const lb = el(box, "abs cn", `left:${i * bw}px;width:${bw}px;text-align:center;top:${h + 14}px;font-size:30px;font-weight:700;color:${labelColor};`, labels[i] ?? "");
    return { b, vl, lb };
  });
  return { box, cols,
    update(t, t0, t1, o = {}) {
      const { hl = -1, out = null } = o;
      const ko = out == null ? 0 : clamp((t - out) / 0.3);
      css(box, { opacity: String((t >= t0 - 0.3 ? 1 : 0) * (1 - ko)), visibility: t >= t0 - 0.3 && ko < 1 ? "visible" : "hidden" });
      cols.forEach(({ b, vl }, i) => {
        const k = eOutCubic(clamp((t - t0 - (i / cols.length) * (t1 - t0) * 0.6) / Math.max(0.3, (t1 - t0) * 0.4)));
        css(b, { transform: `scaleY(${k.toFixed(4)})`, opacity: hl >= 0 && hl !== i ? "0.35" : "1" });
        css(vl, { opacity: k > 0.95 ? "1" : "0" });
      });
    } };
}

// ── Thẻ chương: góc trên trái "01 · ĐOÁN THE GUESS" ──
export function chapter(parent, { n, cn, en = "", theme }) {
  const c = el(parent, "abs", "left:110px;top:70px;white-space:nowrap;");
  el(c, "", `display:inline-block;font-family:Geist;font-size:22px;font-weight:700;color:${theme.accent};letter-spacing:3px;margin-right:16px;`, String(n).padStart(2, "0"));
  el(c, "cn", `display:inline-block;font-size:26px;font-weight:800;color:${theme.ink};letter-spacing:4px;margin-right:14px;`, cn);
  if (en) el(c, "", `display:inline-block;font-family:Geist;font-size:18px;color:${theme.dim};letter-spacing:5px;`, en);
  return { c, update(t, at, out) { const a = clamp((t - at) / 0.35) * (1 - clamp((t - out + 0.3) / 0.3)); css(c, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden", transform: `translateX(${((1 - eOutCubic(clamp((t - at) / 0.4))) * -20).toFixed(1)}px)` }); } };
}

// ── Thẻ câu hỏi lớn: câu hỏi trong 3 giây đầu / câu hỏi hồi tưởng ở cuối ──
export function ask(parent, q, { y = 380, size = 76, color = "#f6f2ea", accent = "#f2c46d", tag = "" } = {}) {
  const c = el(parent, "abs", "left:0;top:0;width:1920px;height:1080px;");
  const tg = tag ? el(c, "abs cn", `left:0;width:1920px;top:${y - 70}px;text-align:center;font-size:30px;letter-spacing:12px;color:${accent};`, tag) : null;
  const qq = el(c, "abs cn", `left:210px;width:1500px;top:${y}px;text-align:center;font-size:${size}px;line-height:1.35;font-weight:900;color:${color};`, q);
  return { c,
    update(t, at, out = null) {
      const k = eOutCubic(clamp((t - at) / 0.45)), ko = out == null ? 0 : clamp((t - out) / 0.3);
      css(c, { opacity: String(k * (1 - ko)), visibility: k * (1 - ko) > 0.001 ? "visible" : "hidden" });
      css(qq, { transform: `translateY(${((1 - k) * 24).toFixed(1)}px)`, filter: `blur(${((1 - k) * 6).toFixed(2)}px)` });
      if (tg) css(tg, { opacity: String(clamp((t - at - 0.2) / 0.4)) });
    } };
}

// ════ Thành phần dựng phim và tư liệu (thêm ngày 2026-10-27: dùng cho phong cách tin phụ đề / điều tra hình ảnh) ════

// Bút dạ quang gạch ý chính: trên một đoạn chữ hoặc vùng hình ảnh, một nét quét từ trái sang phải một khối màu bán trong suốt
// m = marker(s, { x, y, w, h, color: "rgba(255,214,0,0.55)" }); m.update(t, at, dur = 0.35, out)
export function marker(parent, { x, y, w, h, color = "rgba(255,214,0,0.55)", skew = -6 }) {
  const b = el(parent, "abs", `left:${x}px;top:${y}px;width:${w}px;height:${h}px;background:${color};transform-origin:0 50%;transform:skewX(${skew}deg) scaleX(0);mix-blend-mode:multiply;border-radius:3px;`);
  return { b, update(t, at, dur = 0.35, out = null) {
    const k = eOutCubic(clamp((t - at) / dur)), a = out == null ? 1 : 1 - clamp((t - out) / 0.25);
    css(b, { transform: `skewX(${skew}deg) scaleX(${k.toFixed(4)})`, opacity: String(a), visibility: k > 0 && a > 0 ? "visible" : "hidden" });
  } };
}

// Khoanh chú thích vẽ tay: một vòng elip hơi lệch được vẽ ra theo thứ tự nét bút (động tác đặc trưng của điều tra hình ảnh)
// r = ring(s, { cx, cy, rx, ry, color }); r.update(t, at, dur = 0.5, out)
export function ring(parent, { cx, cy, rx, ry, color = "#ff3b30", width = 6, seed = 3 }) {
  const R = rng(seed), pts = [];
  for (let i = 0; i <= 64; i++) { const a = -0.6 + (i / 64) * Math.PI * 2.15, j = 1 + (R() - 0.5) * 0.06; pts.push([cx + Math.cos(a) * rx * j, cy + Math.sin(a) * ry * j]); }
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "1920"); svg.setAttribute("height", "1080"); svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;pointer-events:none;";
  const p = document.createElementNS(svg.namespaceURI, "path");
  p.setAttribute("d", "M" + pts.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join(" L"));
  p.setAttribute("fill", "none"); p.setAttribute("stroke", color); p.setAttribute("stroke-width", String(width)); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round");
  svg.appendChild(p); parent.appendChild(svg);
  const L = p.getTotalLength(); p.style.strokeDasharray = `${L}`;
  return { svg, update(t, at, dur = 0.5, out = null) {
    const k = eInOutCubic(clamp((t - at) / dur)), a = out == null ? 1 : 1 - clamp((t - out) / 0.25);
    p.style.strokeDashoffset = String(L * (1 - k)); css(svg, { opacity: String(k > 0 ? a : 0) });
  } };
}

// Phóng to cục bộ: đẩy một vùng chứa (tệp, ảnh chụp màn hình, ảnh minh hoạ) vào vùng chỉ định và giữ nguyên; dùng kèm ring / marker
// focus(box, t, [[t0, {x, y, s}], [t1, {x, y, s}], …]): x, y là điểm cần đặt vào giữa khung hình (toạ độ vùng chứa), s là hệ số phóng to
export function focus(box, t, keys, { W = 1920, H = 1080 } = {}) {
  let cur = keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t >= keys[i - 1][0]) { const [ta, A] = keys[i - 1], [tb, Bk] = keys[i]; const k = eInOutCubic(clamp((t - ta) / Math.max(0.01, tb - ta))); cur = { x: lerp(A.x, Bk.x, k), y: lerp(A.y, Bk.y, k), s: lerp(A.s, Bk.s, k) }; }
  css(box, { transformOrigin: "0 0", transform: `translate(${(W / 2 - cur.x * cur.s).toFixed(2)}px,${(H / 2 - cur.y * cur.s).toFixed(2)}px) scale(${cur.s.toFixed(4)})` });
}

// Tiêu đề lớn của tin phụ đề: một dòng chữ siêu lớn, từ khoá đè khối vàng (tắt tiếng vẫn hiểu được). words: [["Một khúc gỗ", 0], ["Thưởng mười vàng", 1]], 1 = đè khối vàng
export function capNews(parent, words, { y = 380, size = 120, color = "#ffffff", block = "#ffd600", blockInk = "#111", x = 110 } = {}) {
  const row = el(parent, "abs cn", `left:${x}px;top:${y}px;font-size:${size}px;font-weight:900;line-height:1.25;color:${color};white-space:nowrap;`);
  const spans = words.map(([w, hl]) => { const sp = document.createElement("span"); sp.textContent = w; sp.style.cssText = `display:inline-block;margin-right:${size * 0.18}px;padding:0 ${hl ? size * 0.12 : 0}px;${hl ? `color:${blockInk};` : ""}`; row.appendChild(sp); return { sp, hl }; });
  return { row, update(t, at, out = null, step = 0.16) {
    const ao = out == null ? 1 : 1 - clamp((t - out) / 0.2);
    spans.forEach(({ sp, hl }, i) => {
      const k = eOutCubic(clamp((t - at - i * step) / 0.22));
      css(sp, { opacity: String(k * ao), transform: `translateY(${((1 - k) * 30).toFixed(1)}px)`, background: hl ? `linear-gradient(90deg, ${block} ${(clamp((t - at - i * step - 0.12) / 0.2) * 100).toFixed(1)}%, transparent 0)` : "none" });
    });
  } };
}

// Nguồn trượt vào: nhãn nhỏ trượt vào cạnh con số hoặc khẳng định (tin phụ đề: mỗi con số đều phải có nguồn)
export function srcChip(parent, text, { x, y, color = "#ffd600" } = {}) {
  const c = el(parent, "abs mono", `left:${x}px;top:${y}px;padding:6px 14px;font-size:22px;color:#111;background:${color};white-space:nowrap;border-radius:4px;`, text);
  return { c, update(t, at, out = null) { const k = eOutCubic(clamp((t - at) / 0.3)), a = out == null ? 1 : 1 - clamp((t - out) / 0.2); css(c, { opacity: String(k * a), transform: `translateX(${((1 - k) * -40).toFixed(1)}px)`, visibility: k * a > 0 ? "visible" : "hidden" }); } };
}

// Thanh tiêu đề tin tức (đóng gói kiểu truyền hình / chuyên mục cố định): bên trái khối màu tên chuyên mục + bên phải tiêu đề chạy
export function lowerThird(parent, { tag = "VIBE Tri thức", title = "", y = 860, color = "#d9472b" } = {}) {
  const c = el(parent, "abs", `left:110px;top:${y}px;height:64px;display:flex;align-items:stretch;box-shadow:0 12px 40px rgba(0,0,0,0.45);`);
  el(c, "cn", `background:${color};color:#fff;font-size:28px;font-weight:900;padding:0 22px;display:flex;align-items:center;letter-spacing:3px;`, tag);
  const tt = el(c, "cn", "background:rgba(250,248,242,0.96);color:#111;font-size:30px;font-weight:800;padding:0 26px;display:flex;align-items:center;white-space:nowrap;", title);
  return { c, tt, update(t, at, out = null) { const k = eOutCubic(clamp((t - at) / 0.35)), a = out == null ? 1 : 1 - clamp((t - out) / 0.25); css(c, { opacity: String(a * (k > 0 ? 1 : 0)), clipPath: `inset(0 ${((1 - k) * 100).toFixed(1)}% 0 0)` }); } };
}

// ════ earshot hiệu ứng âm thanh bằng code (github.com/Leonxlnx/earshot, MIT; bảng đối chiếu xem references/10-earshot.md) ════
// const ES = earshot(music);  ES("cut_hit/punch", T("B10.die"));  ES("whoosh_fast/tight", t, { align: "peak" });
// Tuỳ chọn: gain (dB, mặc định -9), align ("onset" mặc định / "peak"), duck (mặc định false), seed / dur / apex / pitch (giao cho earshot render)
// Khi cùng một hiệu ứng âm thanh xuất hiện nhiều lần trong phim, hãy cho mỗi lần một seed khác nhau (earshot sẽ tạo các take khác nhau của cùng một vai, nghe không bị máy móc).
export function earshot(music) {
  return (id, at, o = {}) => {
    const { gain = -9, align = "onset", duck = false, ...es } = o;
    music.push({ src: `earshot:${id}`, at, dur: 3, gain, align, duck, es });
  };
}
// Một chuỗi hiệu ứng âm thanh liên tiếp (tích tắc khi số cuộn, gõ chữ từng ký tự): xếp theo khoảng cách tối thiểu, tránh dính thành một mảng (preset launch của earshot: tick 66ms, key 87ms, pop 114ms)
export function earshotRun(ES, id, t0, t1, gapMs = 90, o = {}) {
  const n = Math.max(1, Math.floor(((t1 - t0) * 1000) / gapMs));
  for (let i = 0; i < n; i++) ES(id, t0 + (i * gapMs) / 1000, { seed: 1 + i, ...o });
}

// ════ Thêm ngày 2026-10-28 (đúc kết từ 04b "Không có tủ lạnh") ════

// Con dấu: một từ "bộp" đóng xuống (lớn → nhỏ + xoay nhẹ), dùng cho điểm hạ của hook, kết luận then chốt
// st = stamp(s, "Chốt", { x: 960, y: 200, size: 130, color: "#d9472b", rot: -8 }); st.update(t, at, out)
export function stamp(parent, text, { x = 960, y = 470, size = 120, color = "#d9472b", rot = -8 } = {}) {
  const s = el(parent, "abs cn", `left:${x - 450}px;width:900px;top:${y}px;text-align:center;font-size:${size}px;font-weight:900;color:${color};letter-spacing:10px;`,
    `<span style="display:inline-block;border:6px solid ${color};border-radius:12px;padding:4px 26px;transform:rotate(${rot}deg)">${text}</span>`);
  return { s, update(t, at, out = null) {
    const k = t - at, a = clamp(k / 0.06) * (out == null ? 1 : 1 - clamp((t - out) / 0.25));
    css(s, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden", transform: `scale(${(k < 0 ? 1.6 : lerp(1.6, 1, eOutCubic(clamp(k / 0.18)))).toFixed(3)})` });
  } };
}

// Hình cắt ngang nét vẽ: đồ vật / kết cấu AI vẽ không chuẩn (băng giám, đồng hồ mặt trời, bánh răng, địa tầng…) thì dùng code vẽ: nét vẽ theo thứ tự, khối màu bật ra sau, nhãn mờ vào sau cùng
// Toạ độ đều nằm trong canvas cục bộ w×h; trên hình ghi "minh hoạ bằng code", trong chú thích nêu nguồn hiện vật / tài liệu
// cw = cutaway(s, { x: 1040, y: 240, w: 700, h: 600,
//   lines: [{ d: "M120 140 H580 V520 H120 Z", color: "#e2b45a", width: 7 }, …],      // vẽ nét theo thứ tự mảng
//   blocks: [{ x: 138, y: 180, w: 58, h: 46, fill: "rgba(191,227,242,0.55)", stroke: "#bfe3f2" }, …],
//   labels: [["Ngoài · Giám vuông", 596, 110, "#e2b45a"], …] });
// cw.update(t, at, out)    các nét bắt đầu vẽ từ khoảng at + i*0.12, mỗi nét 0,5 giây; khối màu bật lần lượt từ at+0.7; nhãn mờ vào lần lượt từ at+0.5
export function cutaway(parent, { x = 1040, y = 240, w = 700, h = 600, lines = [], blocks = [], labels = [], labelSize = 34, scale = 1, step = 0.12 } = {}) {
  const d = el(parent, "abs", `left:${x}px;top:${y}px;width:${w}px;height:${h}px;transform-origin:0 0;transform:scale(${scale});`);
  d.innerHTML = `<svg width="${w}" height="${h}" fill="none" stroke-linecap="round" stroke-linejoin="round">` +
    lines.map((l) => `<path class="q" d="${l.d}" stroke="${l.color || "#f3e6cc"}" stroke-width="${l.width || 5}"/>`).join("") +
    blocks.map((b) => `<rect class="b" x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="${b.r ?? 8}" fill="${b.fill || "rgba(255,255,255,0.3)"}" stroke="${b.stroke || "#fff"}" stroke-width="3"/>`).join("") + `</svg>`;
  const L = labels.map(([txt, lx, ly, c]) => el(d, "abs cn", `left:${lx}px;top:${ly}px;font-size:${labelSize}px;font-weight:900;color:${c || "#f3e6cc"};white-space:nowrap;`, txt));
  const Q = [...d.querySelectorAll(".q")], B = [...d.querySelectorAll(".b")];
  Q.forEach((p) => { const n = p.getTotalLength(); p.style.strokeDasharray = `${n} ${n}`; p.dataset.L = n; });
  return { d, update(t, at, out = null) {
    const a = clamp((t - at + 0.1) / 0.2) * (out == null ? 1 : 1 - clamp((t - out) / 0.25));
    css(d, { opacity: a.toFixed(3), visibility: a > 0.001 ? "visible" : "hidden" });
    Q.forEach((p, i) => { p.style.strokeDashoffset = String(p.dataset.L * (1 - eInOutCubic(clamp((t - at - i * step) / 0.5)))); });
    B.forEach((r, i) => css(r, { opacity: String(clamp((t - at - 0.7 - i * 0.06) / 0.2)) }));
    L.forEach((n, i) => css(n, { opacity: String(clamp((t - at - 0.5 - i * 0.35) / 0.25)) }));
    return a;
  } };
}

// Mảng khối vuông nhỏ: n khối lần lượt bật ra, có thể "tan" chỉ còn lại keep khối (băng tan, tiền tiêu hết, người đi mất)
// row = tokens(s, { x, y, n: 6, size: 80 }); row.update(t, at, meltAt, keep)
export function tokens(parent, { x, y, n, size = 70, gap = 18, fill = "linear-gradient(135deg,#eaf7ff,#9fd0e8)", border = "#dff3ff", glow = "rgba(191,227,242,0.45)", stagger = 0.4 }) {
  const bs = [...Array(n)].map((_, i) => el(parent, "abs", `left:${x + i * (size + gap)}px;top:${y}px;width:${size}px;height:${size}px;border-radius:8px;background:${fill};box-shadow:0 0 24px ${glow};border:2px solid ${border};`));
  return { bs, update(t, at, melt = null, keep = n, out = null) {
    const ko = out == null ? 0 : clamp((t - out) / 0.25);
    bs.forEach((b, i) => {
      const k = eOutCubic(clamp((t - at - i * 0.08) / 0.3));
      const m = melt != null && i >= keep ? clamp((t - melt - (n - 1 - i) * stagger) / 0.6) : 0;
      css(b, { opacity: String(k * (1 - m * 0.75) * (1 - ko)), visibility: k * (1 - ko) > 0 ? "visible" : "hidden", transform: `scale(${(lerp(0.6, 1, k) * (1 - m * 0.4)).toFixed(3)})`,
        background: m > 0.5 ? "transparent" : fill, borderStyle: m > 0.5 ? "dashed" : "solid" });   // đừng viết background: "", sẽ xoá mất màu nền
    });
  } };
}
