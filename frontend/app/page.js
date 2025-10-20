'use client';

import { useState, useEffect } from 'react';
import LeftStoryNav from '../components/LeftStoryNav';
import CreateStoryModal from '../components/CreateStoryModal';
import CreateChapterModal from '../components/CreateChapterModal';
import StoryDetailView from '../components/StoryDetailView';
import StudyDeck from '../components/StudyDeck';

export default function Home() {
  const [stories, setStories] = useState([]);
  const [selectedStory, setSelectedStory] = useState(null);
  const [selectedStudiable, setSelectedStudiable] = useState(null);
  const [showCreateStoryModal, setShowCreateStoryModal] = useState(false);
  const [showCreateChapterModal, setShowCreateChapterModal] = useState(false);

  // Fetch stories on mount
  useEffect(() => {
    fetchStories();
  }, []);

  const fetchStories = async () => {
    try {
      const res = await fetch('/api/stories');
      const data = await res.json();
      setStories(data);
    } catch (error) {
      console.error('Error fetching stories:', error);
    }
  };

  const handleStoryCreated = (newStory) => {
    setStories([...stories, newStory]);
    setSelectedStory(newStory);
    setShowCreateStoryModal(false);
  };

  const handleStorySelected = (story) => {
    setSelectedStory(story);
    setSelectedStudiable(null); // Clear any selected studiable
  };

  const handleStudiableSelected = (studiable) => {
    setSelectedStudiable(studiable);
  };

  const handleBackToStory = () => {
    setSelectedStudiable(null);
  };

  const handleCreateChapter = () => {
    setShowCreateChapterModal(true);
  };

  const handleChapterCreated = () => {
    setShowCreateChapterModal(false);
    // Refresh will happen in StoryDetailView
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Left Navigation */}
      <LeftStoryNav
        stories={stories}
        selectedStory={selectedStory}
        onStorySelect={handleStorySelected}
        onCreateStory={() => setShowCreateStoryModal(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 overflow-auto">
        {selectedStudiable ? (
          // Study Deck View
          <StudyDeck
            studiable={selectedStudiable}
            onBack={handleBackToStory}
          />
        ) : selectedStory ? (
          // Story Detail View
          <StoryDetailView
            story={selectedStory}
            onStudiableSelect={handleStudiableSelected}
            onCreateChapter={handleCreateChapter}
          />
        ) : (
          // Welcome View
          <div className="flex items-center justify-center h-full">
            <div className="text-center glass-card p-12 rounded-2xl">
              <h1 className="text-4xl font-bold text-white mb-4">
                Welcome to Aprendia
              </h1>
              <p className="text-white/80 mb-8">
                Create a new story to start learning
              </p>
              <button
                onClick={() => setShowCreateStoryModal(true)}
                className="px-6 py-3 glass-button-primary text-white rounded-lg"
              >
                Create Your First Story
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Modals */}
      {showCreateStoryModal && (
        <CreateStoryModal
          onClose={() => setShowCreateStoryModal(false)}
          onCreated={handleStoryCreated}
        />
      )}

      {showCreateChapterModal && selectedStory && (
        <CreateChapterModal
          story={selectedStory}
          onClose={() => setShowCreateChapterModal(false)}
          onCreated={handleChapterCreated}
        />
      )}
    </div>
  );
}
