import { useState, useEffect } from 'react';
import LeftStoryNav from '../components/LeftStoryNav';
import CreateStoryModal from '../components/CreateStoryModal';
import StoryCard from '../components/StoryCard';

export default function Home() {
  const [stories, setStories] = useState([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetch('/api/stories').then(res => res.json()).then(setStories);
  }, []);

  return (
    <div className="flex h-screen">
      <LeftStoryNav stories={stories} onCreate={() => setShowModal(true)} />
      <main className="flex-1 p-6 overflow-auto">
        <h1 className="text-2xl font-semibold mb-4">Stories</h1>
        <div className="grid grid-cols-2 gap-4">
          {stories.map(s => <StoryCard key={s.id} story={s} />)}
        </div>
      </main>
      {showModal && <CreateStoryModal onClose={() => setShowModal(false)} onCreated={s => setStories([...stories, s])} />}
    </div>
  );
}