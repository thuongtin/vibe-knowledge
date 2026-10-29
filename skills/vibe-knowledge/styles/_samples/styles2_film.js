// Tuyển tập phim mẫu phong cách · đợt hai "Dựng phim và tư liệu": tin phụ đề, điều tra hình ảnh. Cùng một đoạn mở đầu (dùng lại lời dẫn B01 của kỳ 01), 0 điểm.
// Ý tưởng tham khảo loại "Dựng phim và tư liệu" của Lemo-Opuscar (tin phụ đề / điều tra hình ảnh), phần triển khai và mô tả đều là nguyên bản của skill này.
import { clamp, lerp, eOutCubic, eInOutCubic, el, css } from "../../cine/engine/util.js";
import { TH, bg, plate, marker, ring, focus, capNews, srcChip, lowerThird } from "../../cine/engine/know.js";

export const COLD = 0;
export const TAIL = 2.4;
export const meta = { title: "Tuyển tập phim mẫu phong cách · Dựng phim và tư liệu", n: "styles2" };
export let hits = [], blur = [], clips = [], music = [];
export const sfx = [], sections = [];

const IMG = (f) => new URL(`../01/assets/img/${f}`, import.meta.url).href;
const STY = [
  { name: "Tin phụ đề", en: "CAPTION NEWS", fit: "Tin nóng · tin dữ liệu · câu chuyện có đảo chiều (tắt tiếng vẫn xem hiểu)", th: { bg: 0x0a0a0a, ink: "#ffffff", dim: "#9a9a9a", accent: "#ffd600" } },
  { name: "Điều tra hình ảnh", en: "VISUAL INVESTIGATION", fit: "Khảo chứng sử liệu · nhìn lại sự kiện · bác tin đồn (đưa thẳng nguồn lên màn hình)", th: { bg: 0x101114, ink: "#f2efe8", dim: "#8d8f96", accent: "#ff3b30" } },
];
const beatsOf = (T, id) => ({ ten: T(`${id}.ten`), nobody: T(`${id}.nobody`), fifty: T(`${id}.fifty`) });

// ── Tin phụ đề: cảnh hiện trường làm tối làm nền, mỗi câu một màn phụ đề siêu lớn, từ khoá đè khối vàng, số cuộn, nguồn trượt vào ──
function captionNews(s, h, z, B) {
  const p = plate(s, { src: IMG("a01.jpg"), ai: false });
  css(p.img, { filter: "brightness(0.38) saturate(0.7) blur(2px)" });
  const tag = el(s, "abs mono", "left:110px;top:90px;padding:6px 16px;background:#ffd600;color:#111;font-size:24px;font-weight:700;letter-spacing:3px;", "VIBE Tin nhanh · Lịch sử");
  const c1 = capNews(s, [["Một cây gỗ", 0], ["Nam Môn → Bắc Môn", 0]], { y: 330, size: 110 });
  const c2 = capNews(s, [["Thưởng", 0], ["mười vàng", 1]], { y: 330, size: 150 });
  const c3 = capNews(s, [["Kết quả:", 0], ["không ai động", 1]], { y: 330, size: 150 });
  const c4 = capNews(s, [["Tăng gấp năm", 0], ["năm mươi vàng", 1]], { y: 330, size: 150 });
  const num = el(s, "abs", "left:110px;top:560px;font-family:Geist;font-variant-numeric:tabular-nums;font-size:96px;font-weight:800;color:#fff;white-space:nowrap;");
  const s1 = srcChip(s, "«Sử ký · Thương Quân liệt truyện» \"cho mười vàng\"", { x: 110, y: 690 });
  const s2 = srcChip(s, "\"người dời được cho năm mươi vàng\"", { x: 110, y: 690 });
  return (t) => {
    p.update(t, h - 0.2, z + 0.2, { from: [1.06, 0, 0], to: [1.14, -40, 0] });
    css(tag, { opacity: String(clamp((t - h) / 0.2)) });
    c1.update(t, h + 0.15, B.ten - 0.05); c2.update(t, B.ten, B.nobody - 0.05); c3.update(t, B.nobody, B.fifty - 0.05); c4.update(t, B.fifty, z);
    const v = t < B.ten ? 0 : t < B.fifty ? 10 : Math.round(lerp(10, 50, eOutCubic(clamp((t - B.fifty - 0.3) / 0.6))));
    num.textContent = `${v} vàng`; css(num, { opacity: String(t >= B.ten && (t < B.nobody - 0.05 || t >= B.fifty) ? 1 : 0) });
    s1.update(t, B.ten + 0.4, B.nobody - 0.05); s2.update(t, B.fifty + 0.6, z);
  };
}

// ── Điều tra hình ảnh: nguyên văn «Sử ký» xếp thành một trang văn hiến, theo lời dẫn gạch trọng điểm, vẽ vòng, đẩy gần; bên trái ảnh hiện trường, phía dưới dòng thời gian (nguyên văn cổ văn giữ chữ Hán: bố cục ô theo từng chữ) ──
const CW = 44, X0 = 230;
const LINES = [
  { y: 330, text: "令既具，未布，恐民之不信，已乃立三丈之木於國都市南門，" },
  { y: 420, text: "募民有能徙置北門者予十金。民怪之，莫敢徙。" },
  { y: 510, text: "復曰『能徙者予五十金』。有一人徙之，輒予五十金，以明不欺。" },
];
const at = (line, i, n) => ({ x: X0 + i * CW, y: LINES[line].y, w: n * CW, h: 52 });
function investigation(s, h, z, B) {
  const world = el(s, "abs", "left:0;top:0;width:1920px;height:1080px;");
  el(world, "abs", "left:160px;top:180px;width:1600px;height:460px;background:linear-gradient(180deg,#efe6d0,#e2d4b4);box-shadow:0 30px 90px rgba(0,0,0,0.6);border-radius:4px;");
  el(world, "abs", "left:230px;top:220px;font-family:'Songti SC','STSong',serif;font-size:30px;font-weight:700;color:#7a2a1d;letter-spacing:6px;", "史記 · 卷六十八　商君列傳");
  el(world, "abs mono", "left:1380px;top:226px;font-size:18px;color:#8a7a60;", "Theo bản lưu trên Wikisource");
  for (const L of LINES) {
    const row = el(world, "abs", `left:${X0}px;top:${L.y}px;height:52px;display:flex;font-family:'Songti SC','STSong',serif;font-size:40px;font-weight:600;color:#2a2420;`);
    for (const ch of L.text) el(row, "", `width:${CW}px;text-align:center;line-height:52px;`, ch);
  }
  const m1 = marker(world, at(1, 9, 3)), m2 = marker(world, at(2, 6, 4)), m3 = marker(world, at(2, 24, 4), { color: "rgba(255,120,90,0.5)" });
  const r1 = ring(world, { cx: X0 + 18 * CW, cy: LINES[1].y + 26, rx: 92, ry: 42 });
  const ph = el(world, "abs", "left:160px;top:690px;width:360px;height:202px;overflow:hidden;border:6px solid #f2efe8;box-shadow:0 20px 50px rgba(0,0,0,0.6);transform:rotate(-2deg);");
  el(ph, "abs", `left:0;top:0;width:360px;height:202px;background:url(${IMG("a01.jpg")}) center/cover;`);
  el(ph, "abs mono", "right:6px;bottom:4px;font-size:13px;color:#fff;background:rgba(0,0,0,0.5);padding:1px 6px;", "Minh hoạ · Nam Môn");
  const r2 = ring(world, { cx: 160 + 202, cy: 690 + 100, rx: 34, ry: 80, seed: 7 });
  const steps = ["Dựng cột", "Không dám dời", "Tăng thưởng", "Thực hiện", "Ban lệnh"];
  const tlBg = el(s, "abs", "left:780px;top:36px;width:1040px;height:84px;background:rgba(16,17,20,0.85);border-radius:10px;");
  const tl = el(s, "abs", "left:820px;top:96px;width:960px;height:4px;background:rgba(255,255,255,0.18);");
  const tlf = el(tl, "abs", "left:0;top:0;height:4px;background:#ff3b30;");
  const nodes = steps.map((w, i) => { const n = el(s, "abs cn", `left:${820 + i * 240 - 40}px;top:52px;width:80px;text-align:center;font-size:24px;font-weight:800;color:#8d8f96;`, w); return n; });
  const stamp = el(s, "abs mono", "left:110px;top:58px;font-size:22px;letter-spacing:4px;color:#ff3b30;background:rgba(16,17,20,0.85);padding:6px 12px;z-index:3;", "● EVIDENCE · Đối chiếu sử liệu");
  return (t) => {
    focus(world, t, [[h, { x: 960, y: 540, s: 1 }], [B.ten - 0.2, { x: 960, y: 520, s: 1 }], [B.ten + 0.4, { x: X0 + 12 * CW, y: 450, s: 1.45 }], [B.fifty - 0.2, { x: X0 + 14 * CW, y: 470, s: 1.45 }], [B.fifty + 0.5, { x: X0 + 17 * CW, y: 540, s: 1.6 }], [z, { x: X0 + 18 * CW, y: 540, s: 1.68 }]]);
    m1.update(t, B.ten + 0.35); r1.update(t, B.nobody); m2.update(t, B.fifty + 0.45); m3.update(t, B.fifty + 1.1); r2.update(t, h + 0.5, 0.5, B.ten);
    const prog = t < B.ten ? 0 : t < B.nobody ? 0.25 : t < B.fifty ? 0.5 : t < B.fifty + 1.0 ? 0.75 : 1;
    css(tlf, { width: `${(prog * 100).toFixed(1)}%` });
    nodes.forEach((n, i) => css(n, { color: i / 4 <= prog + 0.001 ? "#f2efe8" : "#5d5f66" }));
    css(stamp, { opacity: String(0.6 + 0.4 * Math.round((Math.sin(t * 6) + 1) / 2)) });
  };
}
const MAKERS = [captionNews, investigation];

export async function build(ctx) {
  const N = ctx.narr, T = (s) => N.t(s), END = N.total, SEG = END / 2;
  const shots = [];
  const add = (from, to, b, r) => shots.push({ from, to, build: b, render: r });
  sections.push({ t: 0, t_to: END + TAIL, level: 1 });
  STY.forEach((st, i) => {
    const a = i * SEG, h = a + 1.8, z = (i + 1) * SEG, id = `B${String(i + 1).padStart(2, "0")}`, B = beatsOf(T, id);
    sfx.push({ t: a + 0.15, type: "whoosh" }, { t: B.nobody, type: i ? "click" : "tick" }, { t: B.fifty, type: "slam" });
    add(a, h, (root) => {
      const s = el(root, "shot");
      const no = el(s, "abs", `left:0;width:1920px;top:340px;text-align:center;font-family:Geist;font-size:26px;letter-spacing:10px;color:${st.th.dim};`, `NEW STYLE ${i + 1} / 2 · ${st.en}`);
      const nm = el(s, "abs cn", `left:0;width:1920px;top:400px;text-align:center;font-size:150px;font-weight:900;color:${st.th.ink};letter-spacing:12px;`, st.name);
      const ft = el(s, "abs cn", `left:0;width:1920px;top:600px;text-align:center;font-size:38px;color:${st.th.accent};letter-spacing:3px;`, `Phù hợp: ${st.fit}`);
      return { s, ns: [no, nm, ft] };
    }, (t, u) => {
      bg(ctx, st.th, { bloom: 0.5 });
      const k = eOutCubic(clamp((t - a) / 0.4)), o = 1 - clamp((t - h + 0.25) / 0.25);
      u.ns.forEach((n) => css(n, { opacity: String(k * o), transform: `translateY(${((1 - k) * 20).toFixed(1)}px)` }));
    });
    add(h, z, (root) => { const s = el(root, "shot"); return { s, draw: MAKERS[i](s, h, z, B) }; }, (t, u) => { bg(ctx, st.th); u.draw(t); });
  });
  add(END, END + TAIL, (root) => {
    const s = el(root, "shot");
    el(s, "abs cn", "left:0;width:1920px;top:380px;text-align:center;font-size:80px;font-weight:900;color:#f6f2ea;", "Thư viện phong cách +2: Dựng phim và tư liệu");
    el(s, "abs cn", "left:0;width:1920px;top:520px;text-align:center;font-size:34px;color:#a8a29a;", "Tin phụ đề · Điều tra hình ảnh  |  dùng riêng được, cũng có thể chồng lên bất kỳ hệ thống thị giác nào");
    return { s };
  }, () => bg(ctx, STY[1].th));
  return shots;
}
