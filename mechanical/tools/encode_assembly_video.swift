import AVFoundation
import CoreGraphics
import ImageIO
import Foundation

guard CommandLine.arguments.count >= 3 else {
    fputs("usage: encode_assembly_video.swift <frames-dir> <output.mp4> [fps]\n", stderr)
    exit(2)
}

let framesURL = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
let fps = Int32(CommandLine.arguments.dropFirst(3).first ?? "24") ?? 24

let files = try FileManager.default.contentsOfDirectory(at: framesURL, includingPropertiesForKeys: nil)
    .filter { $0.pathExtension.lowercased() == "png" }
    .sorted { $0.lastPathComponent < $1.lastPathComponent }
guard let first = files.first,
      let source = CGImageSourceCreateWithURL(first as CFURL, nil),
      let firstImage = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
    fputs("no readable PNG frames\n", stderr)
    exit(3)
}

try? FileManager.default.removeItem(at: outputURL)
let writer = try AVAssetWriter(outputURL: outputURL, fileType: .mp4)
let settings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: firstImage.width,
    AVVideoHeightKey: firstImage.height,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: 3_000_000,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
    ],
]
let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
input.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(
    assetWriterInput: input,
    sourcePixelBufferAttributes: [
        kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32ARGB),
        kCVPixelBufferWidthKey as String: firstImage.width,
        kCVPixelBufferHeightKey as String: firstImage.height,
        kCVPixelBufferCGImageCompatibilityKey as String: true,
        kCVPixelBufferCGBitmapContextCompatibilityKey as String: true,
    ]
)
writer.add(input)
writer.startWriting()
writer.startSession(atSourceTime: .zero)

for (index, file) in files.enumerated() {
    while !input.isReadyForMoreMediaData {
        Thread.sleep(forTimeInterval: 0.005)
    }
    guard let source = CGImageSourceCreateWithURL(file as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else { continue }
    var buffer: CVPixelBuffer?
    CVPixelBufferCreate(
        kCFAllocatorDefault,
        firstImage.width,
        firstImage.height,
        kCVPixelFormatType_32ARGB,
        [
            kCVPixelBufferCGImageCompatibilityKey: true,
            kCVPixelBufferCGBitmapContextCompatibilityKey: true,
        ] as CFDictionary,
        &buffer
    )
    guard let pixelBuffer = buffer else { continue }
    CVPixelBufferLockBaseAddress(pixelBuffer, [])
    if let base = CVPixelBufferGetBaseAddress(pixelBuffer),
       let context = CGContext(
           data: base,
           width: firstImage.width,
           height: firstImage.height,
           bitsPerComponent: 8,
           bytesPerRow: CVPixelBufferGetBytesPerRow(pixelBuffer),
           space: CGColorSpaceCreateDeviceRGB(),
           bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
       ) {
        context.draw(image, in: CGRect(x: 0, y: 0, width: firstImage.width, height: firstImage.height))
    }
    CVPixelBufferUnlockBaseAddress(pixelBuffer, [])
    let time = CMTime(value: CMTimeValue(index), timescale: CMTimeScale(fps))
    adaptor.append(pixelBuffer, withPresentationTime: time)
}

input.markAsFinished()
let semaphore = DispatchSemaphore(value: 0)
writer.finishWriting { semaphore.signal() }
semaphore.wait()
guard writer.status == .completed else {
    fputs("video encoding failed: \(writer.error?.localizedDescription ?? "unknown error")\n", stderr)
    exit(4)
}
print("wrote \(outputURL.path)")
