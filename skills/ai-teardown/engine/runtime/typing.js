/**
 * Thành phần chung của hiệu ứng gõ chữ: tách một đoạn chữ thành các khối chữ xuất hiện lần lượt, sắp thời gian theo nhịp gõ, render(t, t0) bật ra từng chữ.
 *   *từ* biểu thị làm nổi bật: sau khi gõ xong cả đoạn, bút dạ quang vạch màu nền từ trái sang phải.
 *   Từ tiếng Tây và số xuất hiện nguyên cả từ (nếu xuất hiện từng chữ cái sẽ bị xuống dòng giữa từ).
 * Chữ của tất cả Typer, thẻ nhân vật, dòng thời gian, sơ đồ tư duy đều đi qua đây, nhịp thống nhất.
 */
import { h, setStyle } from "./dom.js";
import { appear, hz } from "./spring.js";
import { clamp01, hash01 } from "./ease.js";

const CSS = `
.tp{position:relative;z-index:0}
.tp-c{display:inline-block;white-space:pre}
.tp-c.dot{margin:0 .08em}
.tp-hl{position:relative;display:inline}
.tp-mk{position:absolute;left:-0.1em;right:-0.1em;bottom:0.04em;height:0.44em;border-radius:0.14em;transform-origin:0 50%;z-index:-1}
`;

const PUNCT = /[，。！？；：、,.!?;:）)」』”]/;
const TOKEN = /[A-Za-z0-9][A-Za-z0-9.+#'’\-]*|\s+|./gsu;
const POP = { w: hz(7), z: 0.55 };
const MARK = { w: hz(2.6), z: 1 };

export const typingCss = (css) => css("rt-typing", CSS);

/** Tách dấu hiệu "*nổi bật*" ra, trả về [{text, hl}] */
const segments = (text) => {
  const out = [];
  let hl = false;
  for (const part of String(text).split("*")) {
    if (part) out.push({ text: part, hl });
    hl = !hl;
  }
  return out;
};

/**
 * Dựng sẵn các khối chữ trong container. Trả về { dur, render(t, t0), last }, t0 là thời điểm bắt đầu gõ.
 * opts: cps (số chữ mỗi giây, mặc định 11), seed, hl (màu nổi bật, màu CSS hoặc biến, mặc định var(--hl)), pop (có bật vào hay không, mặc định true)
 */
export function mountTyping(container, text, { cps = 11, seed = 1, hl = "var(--hl)", pop = true } = {}) {
  const toks = [];
  const marks = [];
  const wrap = h("span", { class: "tp" });
  for (const seg of segments(text)) {
    let host = wrap;
    let mark = null;
    if (seg.hl) {
      host = h("span", { class: "tp-hl" });
      mark = h("span", { class: "tp-mk", style: { background: hl, transform: "scaleX(0)" } });
      host.append(mark);
      wrap.append(host);
    }
    for (const m of seg.text.matchAll(TOKEN)) {
      const ch = m[0];
      // Dấu chấm giữa tên người "·" có nét rất hẹp, hai bên chừa một chút, để khỏi bị chen với các chữ trước sau
      const el = h("span", { class: ch === "·" ? "tp-c dot" : "tp-c", text: ch });
      host.append(el);
      toks.push({ ch, el, kind: /^\s+$/.test(ch) ? "space" : PUNCT.test(ch) ? "punct" : /^[A-Za-z0-9]/.test(ch) ? "latin" : "cjk" });
    }
    if (mark) marks.push({ mark, last: toks.length - 1 });
  }
  container.append(wrap);

  // Nhịp gõ: rung có hạt giống, dấu câu dừng thêm một nhịp, khoảng trắng rất nhanh, từ Tây nguyên cả từ tính theo độ dài
  const rel = [];
  let at = 0;
  toks.forEach((tk, i) => {
    rel.push(at);
    const j = 0.72 + 0.56 * hash01(i, seed);
    const w = tk.kind === "punct" ? 2.4 : tk.kind === "space" ? 0.4 : tk.kind === "latin" ? Math.min(2.6, 0.45 + 0.28 * tk.ch.length) : 1;
    at += (j * w) / cps;
  });
  const dur = rel.length ? rel[rel.length - 1] + 0.05 : 0;

  return {
    dur,
    tokens: toks,
    rel,
    /** Thời điểm tương đối khi chữ cuối cùng xuất hiện */
    last: rel.length ? rel[rel.length - 1] : 0,
    render(t, t0) {
      for (let i = 0; i < toks.length; i++) {
        const ti = t0 + rel[i];
        const el = toks[i].el;
        const on = t >= ti;
        setStyle(el, "display", on ? "" : "none");
        if (!on) continue;
        if (pop && t - ti < 0.9) {
          const a = appear(t, ti, POP);
          setStyle(el, "opacity", clamp01(a * 1.6).toFixed(3));
          setStyle(el, "transform", `translateY(${((1 - a) * 0.28).toFixed(3)}em) scale(${(0.72 + 0.28 * a).toFixed(3)})`);
        } else {
          setStyle(el, "opacity", "1");
          setStyle(el, "transform", "none");
        }
      }
      for (const m of marks) {
        const p = appear(t, t0 + rel[m.last] + 0.14, MARK);
        setStyle(m.mark, "transform", `scaleX(${clamp01(p).toFixed(4)})`);
      }
    },
  };
}

/** Gợi ý hiệu ứng âm gõ chữ: cứ một hai chữ lại một tiếng, âm lượng hạ thấp; trả về [{t, name, gain}] (thời điểm tuyệt đối = t0 + thời điểm tương đối) */
export function typingSfx(ty, t0, { every = 2, gain = -27, seed = 3 } = {}) {
  const out = [];
  let n = 0;
  ty.tokens.forEach((tk, i) => {
    if (tk.kind === "space" || tk.kind === "punct") return;
    if (n++ % every) return;
    out.push({ t: t0 + ty.rel[i], name: `key-${1 + Math.floor(hash01(i, seed) * 8)}`, gain });
  });
  return out;
}
