// OCR one PNG with Apple's Vision framework; prints one line per recognised line:
// x0 y0 x1 y1 (page fractions, top-left origin) TAB text
import Foundation
import Vision
import AppKit

let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
  FileHandle.standardError.write("cannot read \(path)\n".data(using: .utf8)!); exit(1)
}
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try handler.perform([req])
let obs = (req.results ?? []).sorted { $0.boundingBox.maxY > $1.boundingBox.maxY }
for o in obs {
  guard let t = o.topCandidates(1).first else { continue }
  let b = o.boundingBox
  print(String(format: "%.3f %.3f %.3f %.3f\t", b.minX, 1 - b.maxY, b.maxX, 1 - b.minY) + t.string)
}
