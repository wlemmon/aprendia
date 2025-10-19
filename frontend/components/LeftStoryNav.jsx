'use client';

export default function LeftStoryNav({ stories, selectedStory, onStorySelect, onCreateStory }) {
  return (
    <aside className="w-64 bg-gray-100 border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Aprendia</h2>
        <button
          onClick={onCreateStory}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition font-medium"
        >
          + New Story
        </button>
      </div>
      
      <div className="flex-1 overflow-auto p-4">
        <h3 className="text-sm font-semibold text-gray-600 mb-2 uppercase">Your Stories</h3>
        {stories.length === 0 ? (
          <p className="text-sm text-gray-500 italic">No stories yet</p>
        ) : (
          <ul className="space-y-1">
            {stories.map((story) => (
              <li key={story.id}>
                <button
                  onClick={() => onStorySelect(story)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition ${
                    selectedStory?.id === story.id
                      ? 'bg-blue-100 text-blue-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-200'
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
