export default function LeftStoryNav({ stories, onCreate }) {
  return (
    <aside className="w-64 bg-gray-100 p-4 border-r overflow-auto">
      <button className="bg-blue-500 text-white w-full py-2 rounded mb-4" onClick={onCreate}>+ New Story</button>
      <ul>
        {stories.map(s => (
          <li key={s.id} className="py-1 text-blue-700 cursor-pointer hover:underline">{s.title}</li>
        ))}
      </ul>
    </aside>
  );
}