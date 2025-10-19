import { useState } from 'react';

export default function CreateStoryModal({ onClose, onCreated }) {
  const [title, setTitle] = useState('');
  const [src, setSrc] = useState('en-US');
  const [tgt, setTgt] = useState('es-ES');

  const createStory = async () => {
    const res = await fetch('/api/stories', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, source_locale: src, target_locale: tgt })
    });
    const data = await res.json();
    onCreated(data);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg w-96">
        <h2 className="text-xl mb-4">New Story</h2>
        <input className="border p-2 w-full mb-2" placeholder="Story title" value={title} onChange={e => setTitle(e.target.value)} />
        <input className="border p-2 w-full mb-2" placeholder="Source locale" value={src} onChange={e => setSrc(e.target.value)} />
        <input className="border p-2 w-full mb-4" placeholder="Target locale" value={tgt} onChange={e => setTgt(e.target.value)} />
        <div className="flex justify-end gap-2">
          <button className="px-4 py-2 bg-gray-200 rounded" onClick={onClose}>Cancel</button>
          <button className="px-4 py-2 bg-blue-500 text-white rounded" onClick={createStory}>Create</button>
        </div>
      </div>
    </div>
  );
}