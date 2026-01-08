import React from "react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[#f9fbff] font-open-dyslexic text-gray-800 leading-relaxed">
      {/* Hero Section */}
      {/* Hero Section */}
      <header className="relative py-32 px-8 bg-gradient-to-br from-blue-600 to-indigo-600 text-white text-center overflow-hidden">
        <div className="max-w-6xl mx-auto relative z-10">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
            <span className="block bg-gradient-to-r from-white to-indigo-100 bg-clip-text text-transparent">
              NeuroAdapt AI
            </span>
            <span className="text-4xl md:text-5xl">
              Dyslexia-Focused Learning Intelligence
            </span>
          </h1>
          <p className="text-xl max-w-3xl mx-auto mb-10 opacity-90">
            Transforming cognitive patterns into personalized learning pathways
            through multimodal AI analysis
          </p>
          <a href="/Learning" target="__blank" className="px-12 py-4 text-lg bg-gradient-to-br from-white to-indigo-100 rounded-full text-blue-600 font-semibold shadow-xl shadow-indigo-300/30 hover:scale-105 transition-transform">
            Try Now !
          </a>
        </div>
        <div className="absolute -bottom-20 left-1/2 -translate-x-1/2 w-[150%] h-96 bg-radial-gradient" />
      </header>

      {/* Impact Statistics Section */}
      <section className="py-24 px-8 bg-white text-blue-900">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-bold mb-6">
              Empowering Neurodiverse Learners
            </h2>
            <p className="text-xl text-neutral-400 max-w-3xl mx-auto">
              Supporting the 20% of global population with language-based
              learning differences through adaptive AI
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            <div className="bg-white/10 p-8 rounded-2xl backdrop-blur-lg">
              <div className="text-5xl font-bold mb-4 text-blue-300">700M+</div>
              <h3 className="text-xl font-semibold mb-3">
                Global Dyslexic Population
              </h3>
              <p className="text-neutral-400">
                Estimated people benefiting from neuro-inclusive learning tools
              </p>
            </div>

            <div className="bg-white/10 p-8 rounded-2xl backdrop-blur-lg">
              <div className="text-5xl font-bold mb-4 text-purple-300">68%</div>
              <h3 className="text-xl font-semibold mb-3">
                Faster Comprehension
              </h3>
              <p className="text-neutral-400">
                Average improvement using multi-sensory learning approaches
              </p>
            </div>

            <div className="bg-white/10 p-8 rounded-2xl backdrop-blur-lg">
              <div className="text-5xl font-bold mb-4 text-green-300">4.2x</div>
              <h3 className="text-xl font-semibold mb-3">Retention Increase</h3>
              <p className="text-neutral-400">
                Long-term knowledge retention with adaptive reinforcement
              </p>
            </div>
          </div>
        </div>
      </section>
      {/* Confusion Analytics Section */}
      <section className="py-24 px-8 bg-white">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <h2 className="text-4xl font-bold text-blue-900 mb-8">
              Cognitive Strain Detection
            </h2>
            <div className="space-y-6">
              <div className="p-8 bg-gray-50 rounded-xl border-l-4 border-blue-400">
                <h3 className="text-2xl font-semibold mb-4 flex items-center gap-4">
                  <span className="w-9 h-9 bg-blue-500 text-white rounded-lg flex items-center justify-center">
                    👁️
                  </span>
                  Biometric Indicators
                </h3>
                <ul className="space-y-3">
                  {[
                    "Blinking anomalies",
                    "Rapid eye movement tracking",
                    "Micro-expression recognition",
                  ].map((item) => (
                    <li key={item} className="flex gap-3">
                      <span>•</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-8 bg-gray-50 rounded-xl border-l-4 border-emerald-500">
                <h3 className="text-2xl font-semibold mb-4 flex items-center gap-4">
                  <span className="w-9 h-9 bg-emerald-500 text-white rounded-lg flex items-center justify-center">
                    📊
                  </span>
                  AI Processing Workflow
                </h3>
                <div className="space-y-6">
                  <div>
                    <h4 className="font-semibold mb-2">Multimodal Fusion</h4>
                    <p className="text-gray-600">
                      Combining eye tracking, facial coding, and speech patterns
                    </p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">Confusion Graph</h4>
                    <p className="text-gray-600">
                      Temporal mapping of cognitive strain events
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-bl from-indigo-50 to-gray-50 rounded-3xl p-12 shadow-2xl shadow-blue-900/10">
            <div className="space-y-12">
              <div className="text-center">
                <div className="w-20 h-20 bg-blue-500 rounded-full mb-6 flex items-center justify-center text-3xl text-white">
                  1
                </div>
                <h3 className="font-semibold mb-2">Real-Time Detection</h3>
                <p className="text-gray-600">High Accuracy</p>
              </div>
              <div className="h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full my-8" />
              <div className="text-center">
                <div className="w-20 h-20 bg-purple-500 rounded-full mb-6 flex items-center justify-center text-3xl text-white">
                  2
                </div>
                <h3 className="font-semibold mb-2">Pattern Analysis</h3>
                <p className="text-gray-600">Using ML Models</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Adaptive Learning Pipeline */}
      <section className="py-24 px-8 bg-gradient-to-br from-gray-50 to-indigo-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-blue-900 text-center mb-16">
            Adaptive Learning Engine
          </h2>
          <div className="grid md:grid-cols-2 gap-12 mb-16">
            <div className="bg-white p-10 rounded-3xl shadow-xl">
              <div className="w-16 h-16 bg-blue-500 rounded-2xl mb-8 flex items-center justify-center text-2xl text-white">
                🎯
              </div>
              <h3 className="text-2xl font-semibold mb-4">
                Topic Segmentation
              </h3>
              <p className="text-gray-600">
                BERT-based NLP models with 93% topic recognition accuracy
              </p>
              <div className="bg-gray-100 rounded-xl p-4 mt-6">
                <div className="w-3/4 h-1 bg-blue-500 rounded-full" />
                <div className="flex justify-between mt-2 text-gray-600 text-sm">
                  <span>Current Topic</span>
                  <span>78% Match</span>
                </div>
              </div>
            </div>

            <div className="bg-white p-10 rounded-3xl shadow-xl">
              <div className="w-16 h-16 bg-purple-500 rounded-2xl mb-8 flex items-center justify-center text-2xl text-white">
                📝
              </div>
              <h3 className="text-2xl font-semibold mb-4">
                Dynamic Note Generation
              </h3>
              <p className="text-gray-600">
                Context-aware summarization with confusion highlights
              </p>
              <div className="bg-gray-100 rounded-xl p-6 mt-6 relative">
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-4/5 bg-purple-500 rounded-full" />
                <p className="italic text-gray-700 m-0">
                  &quot;Identified struggle with quadratic factoring at 12:45 -
                  Suggested visual breakdown&quot;
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <footer className="bg-gray-800 flex flex-col p-12 items-center justify-center text-white">
        <span className="block bg-gradient-to-r from-white to-indigo-100 bg-clip-text text-transparent text-3xl font-bold">
          NeuroAdapt AI
        </span>
        <span className="block bg-gradient-to-r from-white to-indigo-100 bg-clip-text text-transparent text-xl font-bold">
          Catering the needs of the neurodiverse
        </span>
      </footer>
    </div>
  );
}
