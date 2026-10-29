# Lời cảm ơn và tuyên bố tham khảo / Acknowledgements

Code, phong cách mẫu và tài liệu của vibe-knowledge đều do dự án này tự viết. Trong quá trình làm, chúng tôi đã khảo sát và tham khảo các dự án mã nguồn mở dưới đây. Để tôn trọng tác giả gốc và tránh hiểu lầm, ở đây liệt kê từng cái: tham khảo gì, dùng ở đâu, bên kia dùng giấy phép gì.

Nếu bạn là tác giả của một trong các dự án này, thấy ở đây viết chưa chính xác, hoặc muốn bổ sung, sửa lời giải thích, xin hãy mở issue hoặc liên hệ trực tiếp [@Berryxia](https://x.com/berryxia), chúng tôi sẽ sửa ngay lập tức.

## I. Mượn cách làm hoặc ý tưởng triển khai (giấy phép MIT, ghi rõ nguồn)

Các dự án loại này đều dùng giấy phép MIT. Chúng tôi mượn phương pháp và quy tắc của họ, **triển khai lại bằng code và văn bản của chính dự án này**, không sao chép mã nguồn, nguyên văn prompt hay tư liệu của họ.

| Dự án | Tác giả | Giấy phép | Chúng tôi tham khảo gì | Dùng ở đâu trong kho này |
|---|---|---|---|---|
| [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | Lemomo (lemomo-ai) | MIT | Cách tổ chức "phong cách = mô tả phong cách + một đoạn mẫu bằng code"; quy trình studio phong cách "đổi phong cách thành của riêng bạn"; cách phân loại nhóm phong cách "dựng phim và phi hư cấu" (tin tức phụ đề, điều tra trực quan); lời kết "phong cách chỉ là vật chuyên chở, nội dung mới là quan trọng nhất" | `references/09-style-studio.md`, `styles/caption-news`, `styles/investigation`, `styles/_samples/styles2_film.js`, `styles/INDEX.md` |
| [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | alchaincyf (Hoa Thúc) | MIT | 9 loại ngữ pháp giảng giải (xuyên thang đo, tư liệu trên bàn, bảng trắng, biến hình kiểu 3b1b, v.v.); các quy tắc ống kính như "ống kính là dấu câu". Hình tượng Hoa Thúc và nhân vật Clawd không nằm trong phạm vi mượn, dự án này không sử dụng | `references/11-absorbed.md` mục I, II |
| [bang-motion](https://github.com/bangtutorial/bang-motion) | bangtutorial | MIT | "Người, vật, sách được nhắc tới trong lời dẫn bắt buộc phải có hình" | `references/11-absorbed.md` |
| [khan-explainer](https://github.com/haiderfarooq3/khan-explainer) | haiderfarooq3 | MIT | Ngữ pháp bảng viết vừa nói vừa viết, gợi cảm hứng cho phong cách "bảng đen phấn trắng" | `styles/chalk` |
| [paper2video](https://github.com/Lunamos/paper2video) | Lunamos | MIT | Hình ảnh dữ liệu nền tối kiểu 3Blue1Brown; cách viết "sổ cái xuất xứ" | `styles/darkmath`; cấu trúc danh sách sự thật `facts.md` |
| [anatomy-explainer](https://github.com/gnipbao/anatomy-explainer) | gnipbao | MIT | Ý tưởng hình ảnh mặt cắt cơ khí đẳng cự | `styles/isometric` |
| [Paper-Cut](https://github.com/aijiduonadegou/Paper-Cut) | aijiduonadegou | MIT | Cách làm: chốt ảnh tạo ra → tách lớp từ ảnh gốc → hoạt ảnh cắt dán điều khiển bằng code | `styles/collage`(cắt dán bán sắc, bản nâng cao) |
| [SketchNarrator](https://github.com/qingyabailu-git/SketchNarrator) | qingyabailu-git | MIT | Ngữ pháp hình ảnh của giảng giải vẽ tay bằng tiếng Trung | `styles/chalk`, `styles/sketch` |
| [vibe-knowledge-video-skill](https://github.com/LuZhong-Li/vibe-knowledge-video-skill) | LuZhong-Li | MIT | Kết luận đo thực tế về các tác phẩm "Vibe Tri Thức Đại Thưởng" trên Douyin (ví dụ cả 7 tác phẩm đều không có lời dẫn); các đề xuất quy trình như tránh vùng đáy màn hình dọc, khâu đặt tên khái niệm, bộ ba phần cuối phim, "ý kiến thẩm định bên ngoài phải kiểm chứng trước rồi mới sửa" | `references/11-absorbed.md` mục I, III, IV |
| [earshot](https://github.com/Leonxlnx/earshot) | Leonxlnx | MIT | Hiệu ứng âm thanh sinh bằng code. **Không phân phối cùng kho mã**, người dùng tự cài khi cần | `references/10-earshot.md`, `tools/earshot_render.py`, `tools/patch_earshot.py` |

## II. Chỉ tham khảo ý tưởng (không dùng code, nguyên văn prompt hay tư liệu của họ)

Các dự án dưới đây không có giấy phép mã nguồn mở chuẩn, giấy phép hạn chế thương mại, hoặc chứa tư liệu của bên thứ ba. Chúng tôi **chỉ xem phần mô tả công khai, mượn những ý tưởng mang tính chung**, không sao chép bất kỳ code, prompt, văn bản hay tư liệu nào.

| Dự án | Tác giả | Tình trạng giấy phép | Tham khảo gì |
|---|---|---|---|
| [anything2explainer](https://github.com/Vincentwei1021/anything2explainer) | Vincentwei1021 | Giấy phép không chuẩn (GitHub hiển thị NOASSERTION) | Các nguyên tắc chung về khớp lời dẫn với hình ảnh (căn khung xuất hiện, ngân sách hình đứng yên, phụ đề vào ra theo cả câu, làm phim mẫu trước) |
| [video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | Vincentwei1021 | Giấy phép không chuẩn (kho tự mô tả là PolyForm Noncommercial) | Các nguyên tắc chung như ngân sách nhấn mạnh, dàn phụ đề thô |
| [opus-5-5-86-styles-in-motion](https://github.com/GODGOD126/opus-5-5-86-styles-in-motion) | GODGOD126 | Chưa khai báo giấy phép (chứa tư liệu bên thứ ba) | Tầm nhìn tổng thể về phân loại phong cách |
| [opus-video-style-library](https://github.com/limingzhaox/opus-video-style-library) | limingzhaox | Chưa khai báo giấy phép | Cách sắp xếp các ví dụ phong cách |
| [vibe-knowledge](https://github.com/worlds3/vibe-knowledge) | worlds3 | Chưa khai báo giấy phép | Cách làm ở tầng phát hành như nhãn góc "minh họa", cấu trúc cuối phim. **Lưu ý trùng tên: dự án đó trùng tên với dự án này, nhưng hai bên là các dự án khác nhau được phát triển độc lập, không có quan hệ về code hay tư liệu.** |

## III. Các dự án được dẫn trong engine và mẫu bài giảng (skills/ai-teardown)

| Dự án | Tác giả | Giấy phép | Dùng thế nào |
|---|---|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) | HeyGen | Apache-2.0 | Kết nối tùy chọn: `engine/scripts/hf_host.py` gọi dòng lệnh của nó để render mẫu hiệu ứng, không chứa mã nguồn của nó |
| [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | yihui-dev | MIT | Dùng làm liên kết tài liệu tham khảo trong ví dụ bài giảng |
| [WorkBuddyGuide](https://github.com/AlephAITech/WorkBuddyGuide) | AlephAITech | MIT | Nguồn nội dung cho ví dụ mẫu bài giảng, trong phim ghi rõ xuất xứ theo MIT |

## IV. Các thành phần bên thứ ba phân phối cùng kho mã

three.js, Rough.js, lottie-web, AntV X6, Geist, Noto Sans SC, LXGW WenKai, biểu tượng Tabler / Lucide / Iconoir / IconPark, âm thanh bàn phím CC0, v.v., giấy phép và vị trí xem [THIRD_PARTY.md](THIRD_PARTY.md).

## V. Dịch vụ bên ngoài

Xiaomi MiMo (lồng tiếng và nhận dạng giọng nói), [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) (ảnh minh họa, cảnh quay động, hiệu ứng âm thanh của bản nâng cao), Anthropic Claude Code / Claude Opus(dàn dựng và viết code). Các dịch vụ này do người dùng tự đăng ký, kho mã này không chứa bất kỳ khóa nào.

---

**English summary.** All code, style demos and docs in this repository were written for this project. We studied the open-source projects listed above. From the MIT-licensed ones (section 1) we adopted methods and rules, re-implemented in our own code and words, with no source code, prompt text or assets copied. From the projects in section 2, which are unlicensed, non-commercial or contain third-party assets, we took only general ideas. worlds3/vibe-knowledge shares our name but is an unrelated, independently developed project. If anything here is inaccurate, please open an issue and we will fix it promptly.
