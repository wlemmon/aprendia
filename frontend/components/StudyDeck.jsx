'use client';

import { useState, useEffect, useRef } from 'react';

export default function StudyDeck({ studiable, onBack }) {
  const [sentences, setSentences] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showingFront, setShowingFront] = useState(true);
  const [showTargetText, setShowTargetText] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const audioRef = useRef(null);

  useEffect(() => {
    fetchStudiable();
  }, [studiable.id]);

  const fetchStudiable = async () => {
    try {
      const res = await fetch(`/api/studiables/${studiable.id}`);
      const data = await res.json();
      setSentences(data.sentences || []);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching studiable:', error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Auto-play audio when card changes or flips
    if (sentences.length > 0 && audioRef.current) {
      const currentSentence = sentences[currentIndex];
      const audioPath = showingFront ? currentSentence.target_audio : currentSentence.source_audio;
      if (audioPath) {
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
        audioRef.current.src = `${backendUrl}${audioPath}`;
        audioRef.current.play().catch(err => console.error('Audio play error:', err));
      }
    }
  }, [currentIndex, showingFront, sentences]);

  const handleFlip = () => {
    setShowingFront(false);
  };

  const handleSpacedRepetition = (difficulty) => {
    // For now, all buttons do the same thing: move card to back and advance
    const newSentences = [...sentences];
    const currentCard = newSentences.splice(currentIndex, 1)[0];
    newSentences.push(currentCard);
    
    setSentences(newSentences);
    setShowingFront(true);
    setShowTargetText(false);
    
    // If we were at the last card, stay at the same index (which is now the first card again)
    // Otherwise, we're already at the next card
    if (currentIndex >= newSentences.length) {
      setCurrentIndex(0);
    }
  };

  const playAudio = () => {
    if (audioRef.current) {
      audioRef.current.play().catch(err => console.error('Audio play error:', err));
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  if (sentences.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full">
        <div className="text-gray-600 mb-4">No sentences available yet</div>
        <button
          onClick={onBack}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
        >
          ← Back
        </button>
      </div>
    );
  }

  const currentSentence = sentences[currentIndex];
  const progress = `${currentIndex + 1} / ${sentences.length}`;

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="glass border-b border-white/20 px-6 py-4 flex items-center justify-between">
        <button
          onClick={onBack}
          className="px-4 py-2 glass-button text-white rounded-lg"
        >
          ← Back
        </button>
        <h2 className="text-xl font-semibold text-white">{studiable.title}</h2>
        <div className="text-white/80">{progress}</div>
      </div>

      {/* Flashcard */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="glass-card rounded-2xl w-full max-w-2xl min-h-[400px] flex flex-col">
          {showingFront ? (
            // Front of card
            <div className="flex-1 flex flex-col items-center justify-center p-8">
              <div className="mb-6">
                <button
                  onClick={playAudio}
                  className="text-6xl hover:scale-110 transition-transform"
                  title="Play audio"
                >
                  🔊
                </button>
              </div>
              
              {showTargetText ? (
                <p className="text-2xl text-white text-center mb-6">
                  {currentSentence.target_text}
                </p>
              ) : (
                <button
                  onClick={() => setShowTargetText(true)}
                  className="px-6 py-3 glass-button text-white rounded-lg mb-6"
                >
                  Show Text
                </button>
              )}
              
              <button
                onClick={handleFlip}
                className="mt-auto px-6 py-3 glass-button-primary text-white rounded-lg"
              >
                Flip to Back
              </button>
            </div>
          ) : (
            // Back of card
            <div className="flex-1 flex flex-col items-center justify-center p-8">
              <div className="mb-6">
                <button
                  onClick={playAudio}
                  className="text-6xl hover:scale-110 transition-transform"
                  title="Play audio"
                >
                  🔊
                </button>
              </div>
              
              <p className="text-2xl text-white text-center mb-8">
                {currentSentence.source_text}
              </p>
              
              {/* Spaced Repetition Buttons */}
              <div className="flex gap-3 mt-auto flex-wrap justify-center">
                <button
                  onClick={() => handleSpacedRepetition('again')}
                  className="px-6 py-3 glass-button text-white rounded-lg"
                  style={{
                    background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.6), rgba(220, 38, 38, 0.6))',
                  }}
                >
                  Again
                </button>
                <button
                  onClick={() => handleSpacedRepetition('hard')}
                  className="px-6 py-3 glass-button text-white rounded-lg"
                  style={{
                    background: 'linear-gradient(135deg, rgba(249, 115, 22, 0.6), rgba(234, 88, 12, 0.6))',
                  }}
                >
                  Hard
                </button>
                <button
                  onClick={() => handleSpacedRepetition('good')}
                  className="px-6 py-3 glass-button text-white rounded-lg"
                  style={{
                    background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.6), rgba(22, 163, 74, 0.6))',
                  }}
                >
                  Good
                </button>
                <button
                  onClick={() => handleSpacedRepetition('easy')}
                  className="px-6 py-3 glass-button-primary text-white rounded-lg"
                >
                  Easy
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Hidden audio element */}
      <audio ref={audioRef} />
    </div>
  );
}
