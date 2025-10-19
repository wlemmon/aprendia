'use client';

import { useState, useEffect } from 'react';

export default function StoryDetailView({ story, onStudiableSelect, onCreateChapter }) {
  const [studiables, setStudiables] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchStudiables();
    // Poll for updates every 3 seconds to check if chapters/quizzes are done processing
    const interval = setInterval(fetchStudiables, 3000);
    return () => clearInterval(interval);
  }, [story.id]);

  const fetchStudiables = async () => {
    try {
      const res = await fetch(`/api/stories/${story.id}/studiables`);
      const data = await res.json();
      setStudiables(data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching studiables:', error);
      setIsLoading(false);
    }
  };

  const handleCreateQuiz = async (chapterId) => {
    try {
      const res = await fetch(`/api/stories/${story.id}/studiables`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'quiz',
          parent_studiable_id: chapterId,
        }),
      });

      if (!res.ok) throw new Error('Failed to create quiz');
      
      // Refresh studiables
      fetchStudiables();
    } catch (error) {
      console.error('Error creating quiz:', error);
      alert('Failed to create quiz. Please try again.');
    }
  };

  const chapters = studiables.filter((s) => s.metadata?.type === 'chapter');
  const quizzes = studiables.filter((s) => s.metadata?.type === 'quiz');

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">{story.title}</h1>
      <p className="text-gray-600 mb-8">
        {story.source_locale} → {story.target_locale}
      </p>

      {/* Chapters Section */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Chapters</h2>
        <div className="flex gap-4 overflow-x-auto pb-4">
          {chapters.map((chapter) => (
            <div
              key={chapter.id}
              className="flex-shrink-0 w-64 bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden"
            >
              <div className="p-4">
                <h3 className="font-semibold text-gray-800 mb-2">{chapter.title}</h3>
                {chapter.sentences && chapter.sentences.length > 0 ? (
                  <>
                    <p className="text-sm text-gray-600 mb-4">
                      {chapter.sentences.length} sentences
                    </p>
                    <button
                      onClick={() => onStudiableSelect(chapter)}
                      className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition mb-2"
                    >
                      Study Chapter
                    </button>
                    <button
                      onClick={() => handleCreateQuiz(chapter.id)}
                      className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition text-sm"
                    >
                      Create Quiz
                    </button>
                  </>
                ) : (
                  <div className="text-sm text-gray-500 italic">
                    Creating chapter...
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {/* Create Chapter Button */}
          <button
            onClick={onCreateChapter}
            className="flex-shrink-0 w-64 h-48 bg-gray-100 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition flex items-center justify-center"
          >
            <div className="text-center">
              <div className="text-4xl text-gray-400 mb-2">+</div>
              <div className="text-gray-600 font-medium">Create Chapter</div>
            </div>
          </button>
        </div>
      </div>

      {/* Quizzes Section */}
      {quizzes.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Quizzes</h2>
          <div className="flex gap-4 overflow-x-auto pb-4">
            {quizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="flex-shrink-0 w-64 bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden"
              >
                <div className="p-4">
                  <h3 className="font-semibold text-gray-800 mb-2">{quiz.title}</h3>
                  {quiz.sentences && quiz.sentences.length > 0 ? (
                    <>
                      <p className="text-sm text-gray-600 mb-4">
                        {quiz.sentences.length} questions
                      </p>
                      <button
                        onClick={() => onStudiableSelect(quiz)}
                        className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition"
                      >
                        Start Quiz
                      </button>
                    </>
                  ) : (
                    <div className="text-sm text-gray-500 italic">
                      Creating quiz...
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
