'use client';
import { useState, useEffect, useRef } from 'react';

export default function VideoPage() {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const mainVideoRef = useRef<HTMLVideoElement>(null);
  const webcamVideoRef = useRef<HTMLVideoElement>(null);
  const [webcamStream, setWebcamStream] = useState<MediaStream | null>(null);
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:5000';

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
    setSelectedFile(file);
    setAnalysisResult(null);
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

  const analyzeVideo = async () => {
    if (!selectedFile) {
      setError('Select a video before analyzing');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('video', selectedFile);

      const response = await fetch(`${apiBase}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const payload = await response.json();
        throw new Error(payload.error || 'Analysis failed');
      }

      const payload = await response.json();
      setAnalysisResult(payload);
    } catch (err: any) {
      setError(err.message || 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
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
          <div className="absolute bottom-10 left-8 flex flex-col gap-3">
            <button
              className="bg-blue-600 text-white text-lg px-5 py-3 rounded-md font-semibold shadow-lg disabled:opacity-60"
              onClick={analyzeVideo}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze Engagement'}
            </button>
          </div>
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

          {analysisResult && (
            <div className="absolute top-8 right-8 w-96 bg-white shadow-2xl rounded-2xl p-6 space-y-4 border border-indigo-50">
              <h3 className="text-lg font-semibold text-indigo-900">Engagement Summary</h3>
              <div className="text-sm text-gray-600">
                Avg engagement: {analysisResult.summary?.avg_engagement?.toFixed(2)}
              </div>
              <div className="text-sm text-gray-600">
                Confusion events: {analysisResult.summary?.confusion_events}
              </div>

              <div className="space-y-2">
                <div className="text-sm font-semibold text-indigo-900">Heatmap</div>
                <div className="grid grid-cols-12 gap-1">
                  {analysisResult.heatmap?.slice(0, 48).map((bin: any, idx: number) => (
                    <div
                      key={idx}
                      className="h-3 rounded"
                      style={{
                        backgroundColor: `rgba(59, 130, 246, ${Math.min(1, bin.avg_engagement + 0.2)})`,
                      }}
                      title={`${bin.start.toFixed(1)}s - ${bin.end.toFixed(1)}s`}
                    />
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <div className="text-sm font-semibold text-indigo-900">Notes</div>
                <div className="max-h-40 overflow-y-auto space-y-2 text-xs text-gray-600">
                  {analysisResult.notes?.map((note: any, idx: number) => (
                    <div key={idx} className="p-2 bg-indigo-50 rounded">
                      <div className="font-semibold">{note.timestamp.toFixed(1)}s</div>
                      <div>{note.text}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}