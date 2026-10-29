/**
 * Portrait thẻ nhân vật/ảnh: khung polaroid + hai dải băng dính, khi rơi xuống hơi xoay một chút; ảnh đẩy gần chậm rãi (biên độ rất nhỏ, không gây chóng mặt);
 * Tên được gõ ra, phía dưới ngoài khung đặt ghi công và giấy phép (ảnh lấy trên mạng bắt buộc phải có). Lấy gốc toạ độ làm tâm; render là hàm thuần.
 *
 * params
 *   src, w, h         địa chỉ ảnh và kích thước hiển thị
 *   pos               object-position, tiêu điểm cắt (mặc định "50% 30%")
 *   tilt              góc của khung (độ, mặc định -3)
 *   at, out           vào cảnh, rút ra
 *   kb {z0, z1, dur}  biên độ đẩy gần (mặc định 1 → 1.06, kéo dài đến out, không có out thì 12 giây)
 *   name, sub         tên ở mép dưới khung (gõ ra) và một câu mô tả
 *   credit            ghi công và giấy phép
 *   tape [c1, c2]     vị trí màu của hai dải băng dính (mặc định m1, m5); false thì không dùng băng dính
 *   facts             bấm vào ảnh để xem nguồn
 */
import { h, setStyle } from "../runtime/dom.js";
import { appear, hz, UI } from "../runtime/spring.js";
import { clamp01, sineInOut } from "../runtime/ease.js";
import { mountTyping, typingCss } from "../runtime/typing.js";

const CSS = `
.pt{position:absolute;left:0;top:0;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center}
.pt-card{position:relative;background:var(--surface);padding:16px 16px 0;border-radius:12px;box-shadow:var(--shadow)}
.pt-img{overflow:hidden;border-radius:6px;background:var(--surface2)}
.pt-img img{display:block;width:100%;height:100%;object-fit:cover;transform-origin:50% 40%}
.pt-cap{text-align:center;padding:16px 8px 20px}
.pt-name{font:750 40px/1.2 var(--sans);color:var(--ink)}
.pt-sub{font:500 24px/1.35 var(--sans);color:var(--ink2);margin-top:6px}
.pt-tape{position:absolute;top:-16px;width:132px;height:38px;border-radius:4px;opacity:.88}
.pt-credit{font:500 18px/1.4 var(--sans);color:var(--ink3);margin-top:16px;text-align:center;white-space:normal}
`;
const DROP = { w: hz(2.1), z: 0.58 };

export default {
  name: "portrait",
  create(root, p, ctx) {
    ctx.css("pr-portrait", CSS);
    typingCss(ctx.css);
    const at = p.at ?? 0;
    const out = p.out ?? Infinity;
    const tilt = p.tilt ?? -3;
    const kb = { z0: 1, z1: 1.06, dur: Number.isFinite(out) ? out - at : 12, ...(p.kb ?? {}) };
    const el = h("div", { class: "pt" });
    const card = h("div", { class: "pt-card" });
    const frame = h("div", { class: "pt-img", style: { width: `${p.w}px`, height: `${p.h}px` } });
    const img = h("img", { src: p.src, alt: p.name ?? "", style: { objectPosition: p.pos ?? "50% 30%" } });
    frame.append(img);
    card.append(frame);
    let name = null, sub = null, tyN = null, tyS = null;
    if (p.name || p.sub) {
      const cap = h("div", { class: "pt-cap", style: { width: `${p.w}px` } });
      // Cỡ chữ của tên theo chiều rộng thẻ, thẻ hẹp đặt tên dài cũng không xuống dòng
      const nameSize = p.nameSize ?? Math.min(40, Math.floor((p.w - 16) / Math.max(4, Array.from(p.name ?? "").length)));
      if (p.name) { name = h("div", { class: "pt-name", style: { fontSize: `${nameSize}px` } }); cap.append(name); tyN = mountTyping(name, p.name, { cps: 9, seed: 11 }); }
      if (p.sub) { sub = h("div", { class: "pt-sub" }); cap.append(sub); tyS = mountTyping(sub, p.sub, { cps: 15, seed: 17 }); }
      card.append(cap);
    }
    if (p.tape !== false) {
      const [c1, c2] = p.tape ?? ["m1", "m5"];
      const tape = (c, side) => h("div", { class: "pt-tape", style: {
        [side]: "-34px", transform: `rotate(${side === "left" ? -36 : 36}deg)`,
        background: `repeating-linear-gradient(45deg, var(--${c}) 0 10px, var(--${c}-t) 10px 20px)`,
      } });
      card.append(tape(c1, "left"), tape(c2, "right"));
    }
    el.append(card);
    let credit = null;
    if (p.credit) {
      credit = h("div", { class: "pt-credit", text: p.credit, style: { maxWidth: `${p.w + 60}px` } });
      el.append(credit);
    }
    root.append(el);

    return {
      duration: out,
      sfx: [{ t: at + 0.18, name: "paper-place-1", gain: -16 }],
      render(t) {
        const vis = t >= at - 0.05 && t <= out + 0.4;
        setStyle(el, "visibility", vis ? "visible" : "hidden");
        if (!vis) return;
        const a = appear(t, at, DROP);
        const o = clamp01((t - out) / 0.28);
        setStyle(el, "opacity", (clamp01(a * 2) * (1 - o)).toFixed(3));
        setStyle(el, "filter", o > 0.01 ? `blur(${(o * 8).toFixed(2)}px)` : "none");
        setStyle(card, "transform", `translateY(${((1 - a) * -70).toFixed(2)}px) rotate(${(tilt - (1 - a) * 9).toFixed(3)}deg) scale(${(0.9 + 0.1 * a).toFixed(4)})`);
        const z = kb.z0 + (kb.z1 - kb.z0) * sineInOut(clamp01((t - at) / kb.dur));
        setStyle(img, "transform", `scale(${z.toFixed(4)})`);
        if (tyN) tyN.render(t, at + 0.45);
        if (tyS) tyS.render(t, at + 0.55 + (tyN?.dur ?? 0));
        if (credit) setStyle(credit, "opacity", clamp01(appear(t, at + 0.8, UI)).toFixed(3));
      },
      hotspots(t) {
        return p.facts && t >= at && t <= out ? [{ el: card, facts: p.facts, label: p.name ?? "" }] : [];
      },
    };
  },
};
