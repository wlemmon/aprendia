import './globals.css';

export const metadata = {
  title: 'Aprendia - Language Learning',
  description: 'Fast and efficient language learning through stories',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
