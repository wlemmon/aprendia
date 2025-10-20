'use client';

import { useState } from 'react';

export default function CreateChapterModal({ story, onClose, onCreated }) {
  const [formData, setFormData] = useState({
    language_level: story.metadata?.language_level || 'A1',
    age_level: story.metadata?.age_level || 'college',
    topic: story.metadata?.topic || 'travel',
    conversation_type: 'dialogue',
    min_sentence_length: 5,
    max_sentence_length: 15,
  });
  const [isCreating, setIsCreating] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name.includes('sentence_length') ? parseInt(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsCreating(true);

    try {
      const res = await fetch(`/api/stories/${story.id}/studiables`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'chapter',
          ...formData,
        }),
      });

      if (!res.ok) throw new Error('Failed to create chapter');

      onCreated();
    } catch (error) {
      console.error('Error creating chapter:', error);
      alert('Failed to create chapter. Please try again.');
      setIsCreating(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass-modal rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Create Next Chapter</h2>
          <p className="text-gray-600 mb-4">for "{story.title}"</p>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Language Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Language Level (CEFR)
              </label>
              <select
                name="language_level"
                value={formData.language_level}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="A1">A1 - Beginner</option>
                <option value="A2">A2 - Elementary</option>
                <option value="B1">B1 - Intermediate</option>
                <option value="B2">B2 - Upper Intermediate</option>
              </select>
            </div>

            {/* Age Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Age Level
              </label>
              <select
                name="age_level"
                value={formData.age_level}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="toddler">Toddler (2-3)</option>
                <option value="pre_school">Pre-school (4-5)</option>
                <option value="middle_school">Middle School (11-14)</option>
                <option value="high_school">High School (15-18)</option>
                <option value="college">College (18+)</option>
              </select>
            </div>

            {/* Topic */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Topic
              </label>
              <select
                name="topic"
                value={formData.topic}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="travel">Travel</option>
                <option value="parenting">Parenting</option>
              </select>
            </div>

            {/* Conversation Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Story Format
              </label>
              <select
                name="conversation_type"
                value={formData.conversation_type}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="internal_dialogue">Internal Dialogue</option>
                <option value="first_person">1st Person</option>
                <option value="third_person">3rd Person Narrator</option>
                <option value="dialogue">Dialogue Between Two People</option>
              </select>
            </div>

            {/* Sentence Length */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Min Sentence Length
                </label>
                <input
                  type="number"
                  name="min_sentence_length"
                  value={formData.min_sentence_length}
                  onChange={handleChange}
                  min="3"
                  max="7"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Max Sentence Length
                </label>
                <input
                  type="number"
                  name="max_sentence_length"
                  value={formData.max_sentence_length}
                  onChange={handleChange}
                  min="5"
                  max="20"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Buttons */}
            <div className="flex justify-end gap-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                disabled={isCreating}
                className="px-4 py-2 glass-button text-gray-700 rounded-lg disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isCreating}
                className="px-4 py-2 glass-button-primary text-white rounded-lg disabled:opacity-50"
              >
                {isCreating ? 'Creating...' : 'Create Chapter'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
