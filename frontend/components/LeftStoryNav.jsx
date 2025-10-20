'use client';

export default function LeftStoryNav({ stories, selectedStory, onStorySelect, onCreateStory }) {
  return (
    <aside className="w-64 glass flex flex-col">
      <div className="p-4 border-b border-white/20">
        <h2 className="text-xl font-bold text-white mb-4">Aprendia</h2>
        <button
          onClick={onCreateStory}
          className="w-full glass-button-primary text-white py-2 px-4 rounded-lg font-medium"
        >
          + New Story
        </button>
      </div>
      
      <div className="flex-1 overflow-auto p-4">
        <h3 className="text-sm font-semibold text-white/80 mb-2 uppercase">Your Stories</h3>
        {stories.length === 0 ? (
          <p className="text-sm text-white/60 italic">No stories yet</p>
        ) : (
          <ul className="space-y-1">
            {stories.map((story) => (
              <li key={story.id}>
                <button
                  onClick={() => onStorySelect(story)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition ${
                    selectedStory?.id === story.id
                      ? 'glass-button-primary text-white font-medium'
                      : 'text-white/90 hover:bg-white/10'
                  }`}
                >
                  {story.title}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </aside>
  );
}
