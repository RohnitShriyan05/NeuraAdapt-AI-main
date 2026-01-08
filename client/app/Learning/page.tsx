'use client';
import { useState, useEffect, useRef } from 'react';

export default function VideoPage() {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const mainVideoRef = useRef<HTMLVideoElement>(null);
  const webcamVideoRef = useRef<HTMLVideoElement>(null);
  const [webcamStream, setWebcamStream] = useState<MediaStream | null>(null);

  useEffect(() => {
    return () => {
      if (webcamStream) webcamStream.getTracks().forEach(track => track.stop());
      if (videoUrl) URL.revokeObjectURL(videoUrl);
    };
  }, [webcamStream, videoUrl]);

  const handleFile = async (file: File) => {
    if (!file.type.startsWith('video/')) {
      setError('Please upload a video file');
      return;
    }

    const url = URL.createObjectURL(file);
    setVideoUrl(url);
    setError(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      setWebcamStream(stream);
      webcamVideoRef.current!.srcObject = stream;

      if (mainVideoRef.current) {
        mainVideoRef.current.src = url;
        mainVideoRef.current.load();
        mainVideoRef.current.play().catch(error => {
          setError('Click the video to start playback');
        });
      }
    } catch (error) {
      setError('Please allow camera access to continue');
    }
  };

  const handleDrag = (e: React.DragEvent, isEntering: boolean) => {
    e.preventDefault();
    setIsDragging(isEntering);
  };

  return (
    <div className="min-h-screen bg-[#f9fbff] font-open-dyslexic">
      {!videoUrl && (
        <div
          className={`fixed inset-0 flex items-center justify-center transition-colors ${
            isDragging ? 'bg-blue-50' : 'bg-[#f9fbff]'
          }`}
          onDragOver={(e) => handleDrag(e, true)}
          onDragLeave={(e) => handleDrag(e, false)}
          onDrop={(e) => {
            e.preventDefault();
            handleDrag(e, false);
            e.dataTransfer.files[0] && handleFile(e.dataTransfer.files[0]);
          }}
        >
          <div className="text-center p-8 max-w-2xl">
            <div
              className={`p-12 rounded-3xl transition-all ${
                isDragging 
                ? 'bg-gradient-to-br from-blue-100 to-indigo-100 border-4 border-dashed border-blue-400'
                : 'bg-white border-2 border-gray-200 shadow-xl'
              }`}
            >
              <h2 className="text-4xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Upload Learning Material
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Drag and drop video file or click to browse supported formats
              </p>
              
              <input
                type="file"
                id="file-input"
                className="hidden"
                accept="video/*"
                onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              />
              <label
                htmlFor="file-input"
                className="px-8 py-3 bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-shadow cursor-pointer"
              >
                Choose Video File
              </label>
              
              {error && (
                <div className="mt-6 px-4 py-2 bg-red-100 text-red-600 rounded-lg">
                  {error}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {videoUrl && (
        <div className="relative h-screen bg-gradient-to-br from-gray-50 to-indigo-50">
          <div className="h-full w-full flex items-center justify-center p-8">
            <video
              ref={mainVideoRef}
              controls
              className="w-full max-w-6xl rounded-2xl shadow-2xl bg-white"
              onClick={(e) => (e.target as HTMLVideoElement).play()}
            />
          </div>
          <button className='text-black absolute bottom-10 left-8 bg-blue-400 text-2xl p-3 rounded-md text-white font-bold'>Generate Notes</button>
          <div className="absolute bottom-8 right-8 w-80 aspect-video rounded-xl bg-white shadow-2xl border-2 border-indigo-50 overflow-hidden transition-transform hover:scale-105 hover:shadow-2xl group">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-indigo-600/20" />
            <video
              ref={webcamVideoRef}
              autoPlay
              playsInline
              className="w-full h-full object-cover"
            />
            <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/60 to-transparent">
              <h3 className="text-white font-semibold text-lg flex items-center gap-2 text-sm">
                <span className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                  👁️
                </span>
                Cognitive Engagement Monitor
              </h3>
            </div>
          </div>

          {error && (
            <div className="absolute top-8 left-8 px-6 py-3 bg-red-100 text-red-600 rounded-lg flex items-center gap-3">
              <span>⚠️</span>
              {error}
            </div>
          )}
        </div>
      )}
    </div>
  );
}