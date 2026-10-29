/**
 * Biểu tượng mã nguồn mở (định dạng Iconify: IconPark, tabler, lucide, iconoir), lúc build được scripts/icons.py trích thành JSON nhỏ đóng vào bundle, kết xuất không cần nối mạng.
 *   registerIcons(json)            đăng ký một loạt biểu tượng
 *   ico("icon-park:robot", 48, {tone: "m6"})   tạo một <svg>; nét biểu tượng đường nét theo currentColor
 *   drawIcon(svg, p)               biểu tượng đường nét "tự vẽ ra": p từ 0 đến 1; phần có tô màu mờ vào ở nửa sau
 *
 * Biểu tượng nhiều màu của IconPark (tiền tố icon-park:) vốn có bốn màu cố định: #000 viền, #2F88FF tô, #FFF viền trong, #43CCF8 tô trong.
 * Ở đây đổi thành biến CSS --ic-s / --ic-f / --ic-i / --ic-if, dùng ico(name, size, {tone: "m5"}) đổi một lần sang một ô màu macaron.
 */
import { s } from "./dom.js";

const REG = {};
export const registerIcons = (json) => Object.assign(REG, json);
export const hasIcon = (name) => name in REG;

const SHAPES = "path,circle,rect,line,polyline,polygon,ellipse";

const PARK = { "#000": "--ic-s", "#000000": "--ic-s", "#2f88ff": "--ic-f", "#fff": "--ic-i", "#ffffff": "--ic-i", "#43ccf8": "--ic-if" };

export const ico = (name, size = 24, { color = "currentColor", stroke = null, draw = false, tone = null } = {}) => {
  const rec = REG[name];
  if (!rec) throw new Error(`Biểu tượng chưa đăng ký: ${name} (chạy scripts/icons.py trước)`);
  const svg = s("svg", { viewBox: `0 0 ${rec.w} ${rec.h}`, width: size, height: size, style: { color, overflow: "visible", display: "block" } });
  svg.innerHTML = rec.body;
  if (name.startsWith("icon-park:")) {
    // Thuộc tính trình bày không viết được var(), đổi thành style nội tuyến
    for (const el of svg.querySelectorAll("*")) {
      for (const a of ["fill", "stroke"]) {
        const v = PARK[(el.getAttribute(a) || "").toLowerCase()];
        if (v) el.style[a] = `var(${v})`;
      }
    }
    const c = tone ?? "m6";
    for (const [k, v] of Object.entries({ "--ic-s": `var(--${c}-d)`, "--ic-f": `var(--${c})`, "--ic-i": "var(--surface)", "--ic-if": `var(--${c}-t)` })) svg.style.setProperty(k, v);
  }
  // stroke tính theo lưới 24; IconPark là lưới 48, phải phóng to theo tỉ lệ
  if (stroke != null) for (const el of svg.querySelectorAll("[stroke-width]")) el.setAttribute("stroke-width", ((stroke * rec.w) / 24).toFixed(2));
  if (draw) {
    // pathLength=1 để mỗi đoạn viền đều tính độ dài theo 0..1, dashoffset nhờ đó điều khiển thống nhất
    for (const el of svg.querySelectorAll(SHAPES)) {
      el.setAttribute("pathLength", "1");
      el.setAttribute("stroke-dasharray", "1 1");
      el.setAttribute("stroke-dashoffset", "1");
    }
    svg.dataset.draw = "1";
  }
  return svg;
};

export const drawIcon = (svg, p) => {
  // Nét vẽ xong trong 70% đầu, tô màu mờ vào ở nửa sau (biểu tượng chỉ có nét không có tô màu, không bị ảnh hưởng)
  const pc = Math.min(1, Math.max(0, p));
  const v = (1 - Math.min(1, pc / 0.7)).toFixed(4);
  const f = Math.min(1, Math.max(0, (pc - 0.5) / 0.5)).toFixed(3);
  for (const el of svg.querySelectorAll(SHAPES)) {
    if (el.getAttribute("stroke-dashoffset") !== v) el.setAttribute("stroke-dashoffset", v);
    if (el.style.fillOpacity !== f) el.style.fillOpacity = f;
  }
  for (const g of svg.querySelectorAll("g")) if (g.style.fillOpacity !== f) g.style.fillOpacity = f;
};
