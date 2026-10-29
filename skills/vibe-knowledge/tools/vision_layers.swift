// Phân đoạn thể hiện tiền cảnh của Vision: xuất mặt nạ xám bằng kích thước ảnh gốc (_all = toàn bộ thể hiện, _N = một thể hiện đơn), rồi dùng PIL ghép lớp chủ thể, vá lỗ để làm lớp nền.
// Biên dịch: swiftc -O vision_layers.swift -o ~/.cache/vibe-knowledge/vision_layers   Cách dùng: vision_layers in.jpg out/prefix
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers
let a = CommandLine.arguments
guard a.count >= 3 else { print("usage: layers in.jpg outPrefix"); exit(1) }
let ci = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let ctx = CIContext(); let cg = ctx.createCGImage(ci, from: ci.extent)!
let req = VNGenerateForegroundInstanceMaskRequest(); let h = VNImageRequestHandler(cgImage: cg)
try h.perform([req])
guard let r = req.results?.first else { print("no subject"); exit(2) }
func save(_ set: IndexSet, _ path: String) throws {
  let buf = try r.generateScaledMaskForImage(forInstances: set, from: h)
  let im = CIImage(cvPixelBuffer: buf); let o = ctx.createCGImage(im, from: im.extent, format: .L8, colorSpace: CGColorSpaceCreateDeviceGray())!
  let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
  CGImageDestinationAddImage(d, o, nil); CGImageDestinationFinalize(d)
}
try save(r.allInstances, a[2] + "_all.png")
for i in r.allInstances { try save(IndexSet(integer: i), a[2] + "_\(i).png") }
print("instances", Array(r.allInstances))
