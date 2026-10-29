// Trục thời gian lời dẫn: đọc timings.json do lồng tiếng sinh ra (thời gian từng chữ, thời gian [[cue]]), cung cấp "câu nào nói tới chữ nào là ở giây thứ mấy" và phụ đề.
// Đoạn mở đầu lạnh (đoạn mẫu) chiếm off giây, lời dẫn toàn bộ lùi về sau off giây.
export class Narr {
  constructor(tl, off = 0) {
    this.tl = tl;
    this.off = off;
    this.beats = tl.beats;
    this.ids = Object.keys(tl.beats);
    this.total = tl.total + off;
    this.subs = this.buildSubs();
  }

  // "B03" bắt đầu / "B03.count" đọc tới [[count]] / "B03@三千" đọc tới "三千" (chuỗi chữ trong lời dẫn) / "B03.end" kết thúc; có thể thêm "+0.4" "-0.2"
  t(spec) {
    const m = /^(B\d+)(?:\.([a-z0-9_]+)|@([^+\-]+))?([+-]\d+(?:\.\d+)?)?$/.exec(spec);
    if (!m) throw new Error(`Cách viết thời gian không đúng: ${spec}`);
    const b = this.beats[m[1]];
    if (!b) throw new Error(`Không có nhịp này: ${spec}`);
    let v;
    if (m[2] === "end") v = b.end;
    else if (m[2]) {
      if (b.cues[m[2]] === undefined) throw new Error(`${m[1]} không có [[${m[2]}]]`);
      v = b.cues[m[2]];
    } else if (m[3]) {
      const i = b.text.indexOf(m[3]);
      if (i < 0) throw new Error(`${m[1]} không có "${m[3]}"`);
      v = b.chars[i];
    } else v = b.start;
    return v + this.off + (m[4] ? parseFloat(m[4]) : 0);
  }

  // Phụ đề: ngắt câu theo dấu câu, câu quá dài thì cắt tiếp ở dấu phẩy hoặc khoảng trắng giữa câu; mỗi dòng kéo dài từ lúc chữ đầu tiên xuất hiện đến khi dòng sau bắt đầu (trong cùng một nhịp)
  buildSubs() {
    const out = [];
    const P = "，。；：！？、,.;:!?";
    for (const id of this.ids) {
      const b = this.beats[id];
      const txt = b.text;
      let segs = [], s0 = 0;
      for (let i = 0; i <= txt.length; i++) {
        const num = txt[i] === "." && /\d/.test(txt[i - 1] || "") && /\d/.test(txt[i + 1] || "");   // dấu thập phân như 5.5 thì không ngắt câu
        if (i === txt.length || (P.includes(txt[i]) && !num)) {
          if (i > s0) segs.push([s0, i]);
          s0 = i + 1;
        }
      }
      // Gộp những câu quá ngắn, cắt những câu quá dài
      const merged = [];
      for (const sg of segs) {
        const last = merged[merged.length - 1];
        if (last && sg[1] - last[0] <= 16 && sg[0] - last[1] <= 1 && (last[1] - last[0]) < 7) last[1] = sg[1];
        else merged.push([...sg]);
      }
      merged.forEach(([a, z], k) => {
        const start = b.chars[a] + this.off;
        const next = k + 1 < merged.length ? b.chars[merged[k + 1][0]] + this.off : b.end + this.off + 0.15;
        out.push({ text: txt.slice(a, z).trim().replace(/[，。；：、]/g, "　"), start: start - 0.05, end: next - 0.04 });   // Trong phụ đề không giữ dấu câu, dùng khoảng trắng toàn chiều rộng để ngăn cách
      });
    }
    return out;
  }

  sub(t) {
    for (const s of this.subs) if (t >= s.start && t < s.end) return s;
    return null;
  }
}
