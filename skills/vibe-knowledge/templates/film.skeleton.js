// Tập __ID__ · __TITLE__ (bản gốc __TPL__)
// Hợp đồng giống ai-teardown cine (references/10-cine.md): cảnh quay { from, to, build(root), render(t, u) }, render chỉ nhìn thời gian tuyệt đối t, không phụ thuộc khung hình trước.
// Các thành phần dùng riêng cho tập này nằm ở ../../cine/engine/know.js (bộ vibe-knowledge), tài nguyên luôn dùng A("img/xx.jpg") để lấy đường dẫn.
import { clamp, lerp, inv, eOutCubic, eInOutCubic, el, css } from "../../cine/engine/util.js";
import { appear, slam } from "../../cine/engine/ui.js";
import { TH, bg, layers, plate, vclip, keyword, counter, foot, foots, choice, seriesCard, vquote, trail, spread, bars, chapter, ask } from "../../cine/engine/know.js";

const A = (f) => new URL(`./assets/${f}`, import.meta.url).href;
const P = (f) => decodeURIComponent(new URL(`./assets/${f}`, import.meta.url).pathname).slice(1);   // mục music: đường dẫn tương đối so với thư mục series (finish.py đã được vá)
const TM = TH.starfield;                                                   // hệ thống thị giác: starfield / gufeng / darkgold / paper / pixel

export const COLD = 0;                     // không ghép phần mở đầu lạnh bên ngoài
export const TAIL = 2.5;                   // sau khi lời dẫn kết thúc dừng 2,5 giây (thẻ kết)
export const meta = { title: "__TITLE__", n: "__ID__" };
export let hits = [], blur = [], clips = [], music = [];
export const sfx = [], sections = [];

export async function build(ctx) {
  const N = ctx.narr, T = (s) => N.t(s), END = N.total;
  const shots = [];
  const add = (from, to, b, r) => shots.push({ from, to, build: b, render: r });
  const cue = (t, type, o = {}) => sfx.push({ t, type, ...o });

  // Nhạc nền: Renoise Lyria Pro làm riêng (assets/audio/score.wav), đoạn có lời dẫn finish.py sẽ tự hạ thêm; nếu không có thì dùng sections để tổng hợp nền
  // BGM mặc định (skill có sẵn vibe-bgm, fit_bgm.py --lesson cắt theo độ dài phim rồi đặt ở assets/audio/bgm.wav)
  music.push({ src: P("audio/bgm.wav"), from: 0, at: 0, dur: END + TAIL, gain_curve: [[0, -11], [END, -11], [END + TAIL, -8]], fade_in: 0.3, fade_out: 1.8 });
  // Hiệu ứng âm thanh đơn lẻ (ElevenLabs SFX): music.push({ src: P("audio/sfx_bell.wav"), from: 0, at: T("B07.reveal"), dur: 3, gain: -8 });
  sections.push({ t: 0, t_to: END + 2.5, level: 0 });

  // ── B01 Mở đầu lạnh ──
  add(0, T("B03"), (root) => {
    const s = el(root, "shot");
    const p = plate(s, { src: A("img/a01.jpg") });
    const q = ask(s, "Viết câu hỏi mở đầu ở đây", { accent: TM.accent });
    const f = foot(s);
    return { s, p, q, f };
  }, (t, u) => {
    bg(ctx, TM);
    u.p.update(t, 0, T("B03"), { from: [1.02, 0, 0], to: [1.12, -30, 0] });
    u.q.update(t, T("B01") + 0.2, T("B02"));
    foots(u.f, t, [[T("B01"), T("B02"), "Nguồn: ..."]]);
  });

  // ── Thẻ kết ──
  add(END, END + TAIL, (root) => {
    const s = el(root, "shot");
    const k = keyword(s, "__TITLE__", { y: 440, size: 96, color: TM.ink, sub: "Vibe Knowledge · Phim này do Claude Opus 5.5 thực hiện", subColor: TM.dim });
    return { s, k };
  }, (t, u) => { bg(ctx, TM); u.k.update(t, END + 0.1); });

  return shots;
}
