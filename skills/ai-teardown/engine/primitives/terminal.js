/**
 * Terminal phát lại terminal: phát các khung hình do scripts/term_record.py ghi thật và term_frames.py phát lại.
 * Màn hình là một cửa sổ terminal tối kiểu macOS; chữ được dàn từng ô (ký tự rộng chiếm hai ô), nên giống hệt terminal thật nhưng phóng to không bị mờ.
 *
 * params
 *   data        đầu ra của term_frames.py ({cols, rows, frames, marks, duration})
 *   at, out     thời điểm xuất hiện và rời đi trong bài
 *   from, to    phát đoạn nào của bản quay màn hình (tính theo giây của chính bản quay; mặc định cả đoạn)
 *   rate        tốc độ phát (mặc định 1); mẫu cảnh sẽ tự tính theo độ dài cảnh
 *   w           chiều rộng cửa sổ (pixel, mặc định 1400)
 *   title       chữ trên thanh tiêu đề
 *   rowsShown   chỉ hiển thị từ dòng nào đến dòng nào của bản quay màn hình [a, b] (cắt bỏ phần trống, chữ sẽ to lên theo)
 *   hi          làm nổi bật [{rows: [a, b], at, until, color}]: phủ một khung màu lên vài dòng, nhắc người xem nhìn vào đây
 *   zoom        [{at, until, rows: [a, b], scale}]: đẩy ống kính cận vào vài dòng
 * render(t) chỉ phụ thuộc vào t.
 */
import { h, setStyle } from "../runtime/dom.js";
import { appear, UI } from "../runtime/spring.js";
import { clamp01, cubicInOut } from "../runtime/ease.js";

const CSS = `
.tm{position:absolute;left:0;top:0;transform-origin:50% 50%;border-radius:18px;overflow:hidden;background:#1B1F2A;
  box-shadow:0 30px 70px rgba(20,30,40,.28),0 0 0 1.5px rgba(255,255,255,.06) inset}
.tm-bar{height:44px;display:flex;align-items:center;gap:9px;padding:0 18px;background:#262B38;color:#AEB6C8;font:600 18px/1 "Geist","Noto Sans SC",sans-serif}
.tm-bar i{width:13px;height:13px;border-radius:50%;display:block}
.tm-bar span{margin-left:10px}
.tm-view{position:relative;overflow:hidden}
.tm-body{position:absolute;left:0;top:0;transform-origin:0 0;padding:14px 20px 18px;font-family:"Geist Mono","SF Mono",Menlo,"Noto Sans SC",monospace;color:#E4E8F1;white-space:pre}
.tm-row{height:1.32em;line-height:1.32em}
.tm-w{display:inline-block;width:2ch;text-align:center}
.tm-cur{position:absolute;width:1ch;height:1.2em;background:#9FE2C8;opacity:.85}
.tm-hi{position:absolute;left:10px;right:10px;border-radius:10px;border:3px solid #FFD666;background:rgba(255,214,102,.10);box-shadow:0 0 0 6px rgba(255,214,102,.12)}
`;

const NAMED = {
  default: null, black: "#3B4252", red: "#F2777A", green: "#99C794", brown: "#F9D071", yellow: "#F9D071", blue: "#6699CC",
  magenta: "#C594C5", cyan: "#5FB3B3", white: "#D8DEE9",
  brightblack: "#6B7385", brightred: "#FF8F91", brightgreen: "#B5E6A8", brightbrown: "#FFE08A", brightyellow: "#FFE08A",
  brightblue: "#8AB4F8", brightmagenta: "#DDA9E6", brightcyan: "#7ED6D6", brightwhite: "#FFFFFF",
};
const FG0 = "#E4E8F1", BG0 = "#1B1F2A";
const color = (c, fallback) => (c == null || c === "default" ? fallback : NAMED[c] !== undefined ? NAMED[c] ?? fallback : /^[0-9a-f]{6}$/i.test(c) ? `#${c}` : fallback);
// Ký tự toàn chiều rộng (CJK, dấu câu toàn chiều rộng, emoji) chiếm hai ô. So sánh bằng mã điểm thay vì regex lớp ký tự: trong mã nguồn không xuất hiện ký tự không phải ASCII, nên khi trang không khai báo mã hoá cũng không báo lỗi (comment này không tính)
const WIDE_RANGES = [[0x1100, 0x115f], [0x2e80, 0xa4cf], [0xac00, 0xd7a3], [0xf900, 0xfaff], [0xfe30, 0xfe4f], [0xff00, 0xff60], [0xffe0, 0xffe6], [0x1f300, 0x1faff]];
const isWide = (ch) => { const c = ch.codePointAt(0); return WIDE_RANGES.some(([a, b]) => c >= a && c <= b); };
const esc = (s) => s.replace(/[&<>]/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[m]);

function rowHTML(runs) {
  let out = "";
  for (const [text, fg, bg, fl] of runs) {
    let f = color(fg, FG0), b = color(bg, null);
    if (fl & 8) [f, b] = [b ?? BG0, f];
    const st = `color:${f}${b ? `;background:${b}` : ""}${fl & 1 ? ";font-weight:700" : ""}${fl & 2 ? ";font-style:italic" : ""}${fl & 4 ? ";text-decoration:underline" : ""}`;
    let inner = "";
    for (const ch of text) inner += isWide(ch) ? `<span class="tm-w">${esc(ch)}</span>` : esc(ch);
    out += `<span style="${st}">${inner}</span>`;
  }
  return out || " ";
}

export const Terminal = {
  name: "terminal",
  create(root, p, ctx) {
    ctx.css("pr-terminal", CSS);
    const D = p.data, at = p.at ?? 0, out = p.out ?? Infinity, rate = p.rate ?? 1;
    const from = p.from ?? 0, to = p.to ?? D.duration;
    const [r0, r1] = p.rowsShown ?? [0, D.rows - 1];
    const nRows = r1 - r0 + 1;
    // Cỡ chữ bị giới hạn cả hai đầu rộng và cao: rộng theo số cột (độ rộng chữ đơn cách khoảng 0,6em), cao theo số dòng, cả cửa sổ không vượt quá maxH
    const maxH = p.maxH ?? 900;
    const fs = Math.min(40, ((p.w ?? 1400) - 40) / (D.cols * 0.602), (maxH - 76) / (nRows * 1.32));
    const W = Math.round(D.cols * 0.602 * fs + 40);
    const lineH = fs * 1.32;
    const H = 44 + nRows * lineH + 32;

    // Khôi phục toàn bộ màn hình theo từng khung hình (mỗi dòng là một mảng runs, dòng không đổi dùng chung một tham chiếu, so sánh tham chiếu là biết có cần vẽ lại hay không)
    const states = [];
    let cur = Array.from({ length: D.rows }, () => []);
    for (const f of D.frames) {
      const next = cur.slice();
      for (const k in f.d) next[+k] = f.d[k];
      states.push({ t: f.t, rows: next, c: f.c });
      cur = next;
    }
    const times = states.map((s) => s.t);

    const el = h("div", { class: "tm", style: { width: `${W}px`, height: `${H}px`, marginLeft: `${-W / 2}px`, marginTop: `${-H / 2}px` } });
    const bar = h("div", { class: "tm-bar" });
    ["#FF5F57", "#FEBC2E", "#28C840"].forEach((c) => bar.append(h("i", { style: { background: c } })));
    bar.append(h("span", { text: p.title ?? "Terminal" }));
    const view = h("div", { class: "tm-view", style: { height: `${H - 44}px` } });
    const body = h("div", { class: "tm-body", style: { fontSize: `${fs}px`, top: `${-r0 * lineH}px` } });
    const rowEls = Array.from({ length: D.rows }, () => h("div", { class: "tm-row" }));
    rowEls.forEach((r) => body.append(r));
    const cursor = h("div", { class: "tm-cur" });
    body.append(cursor);
    view.append(body);
    const his = (p.hi ?? []).map((x) => {
      const e = h("div", { class: "tm-hi", style: { top: `${14 + (x.rows[0] - r0) * lineH - 4}px`, height: `${(x.rows[1] - x.rows[0] + 1) * lineH + 8}px`,
        borderColor: x.color ?? "#FFD666" } });
      view.append(e);
      return { ...x, e };
    });
    el.append(bar, view);
    // Kiểu sticker: viền trắng ngoài + nét viền mảnh + bóng đổ (vẽ bằng box-shadow ngoài khung, không đổi hình học cửa sổ, toạ độ chú thích giữ nguyên)
    if (p.sticker) el.style.boxShadow = "0 0 0 10px #fff, 0 0 0 11.5px rgba(55,53,47,.14), 0 26px 56px rgba(55,53,47,.24)";
    root.append(el);

    const drawn = new Array(D.rows).fill(null);
    let lastIdx = -1;
    const idxAt = (lt) => {
      let lo = 0, hi = times.length - 1, ans = 0;
      while (lo <= hi) { const m = (lo + hi) >> 1; if (times[m] <= lt) { ans = m; lo = m + 1; } else hi = m - 1; }
      return ans;
    };

    return {
      duration: out,
      render(t) {
        const vis = t >= at - 0.05 && t <= out + 0.4;
        setStyle(el, "visibility", vis ? "visible" : "hidden");
        if (!vis) return;
        const a = appear(t, at, UI);
        const ex = clamp01((t - out) / 0.3);
        // Đẩy ống kính cận
        let sc = 1, ty = 0;
        for (const z of p.zoom ?? []) {
          const k = cubicInOut(clamp01((t - z.at) / 0.6)) * (1 - cubicInOut(clamp01((t - (z.until ?? Infinity)) / 0.6)));
          if (k > 0) { sc = 1 + ((z.scale ?? 1.6) - 1) * k; ty = -(((z.rows[0] + z.rows[1]) / 2 - r0 + 0.5) * lineH - (H - 44) / 2) * k; }
        }
        setStyle(el, "opacity", (a * (1 - ex)).toFixed(3));
        setStyle(el, "transform", p.sticker ? `scale(${(1.06 - 0.06 * a).toFixed(4)})` : `translateY(${((1 - a) * 30).toFixed(1)}px)`);
        setStyle(body, "transform", `translateY(${(ty * sc).toFixed(1)}px) scale(${sc.toFixed(4)})`);
        setStyle(body, "transformOrigin", `50% ${(((p.zoom?.[0]?.rows?.[0] ?? r0) - r0) * lineH).toFixed(0)}px`);

        const lt = Math.min(to, from + Math.max(0, t - at) * rate);
        const i = idxAt(lt);
        if (i !== lastIdx) {
          const S = states[i];
          for (let y = 0; y < D.rows; y++) if (drawn[y] !== S.rows[y]) { rowEls[y].innerHTML = rowHTML(S.rows[y]); drawn[y] = S.rows[y]; }
          lastIdx = i;
        }
        const S = states[i];
        const blink = Math.floor((t - at) * 1.6) % 2 === 0;
        setStyle(cursor, "display", S.c[2] && blink ? "block" : "none");
        setStyle(cursor, "left", `calc(20px + ${S.c[0]}ch)`);
        setStyle(cursor, "top", `${14 + S.c[1] * lineH + fs * 0.06}px`);
        for (const x of his) {
          const k = clamp01((t - (typeof x.at === "number" ? x.at : at)) / 0.3) * (x.until != null ? clamp01((x.until - t) / 0.3) : 1);
          setStyle(x.e, "opacity", k.toFixed(3));
        }
      },
    };
  },
};

export default Terminal;
