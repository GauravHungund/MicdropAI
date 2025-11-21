import React, { useRef, useState, useEffect } from 'react';
import Header from './components/Header';
import PromptInput from './components/PromptInput';
import PodcastPlayer from './components/PodcastPlayer';

function App() {
  const playerRef = useRef(null);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleGenerate = () => {
    // Small delay to allow for any immediate state updates or animations to start
    setTimeout(() => {
      playerRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
  };

  return (
    <div className="app-container">
      <Header theme={theme} toggleTheme={toggleTheme} />
      <main>
        <PromptInput onGenerate={handleGenerate} />
        <div ref={playerRef} className="w-full flex justify-center">
          <PodcastPlayer />
        </div>
      </main>
    </div>
  );
}

export default App;
