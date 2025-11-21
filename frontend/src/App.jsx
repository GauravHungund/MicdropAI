import React, { useRef, useState, useEffect } from 'react';
import Header from './components/Header';
import PromptInput from './components/PromptInput';
import PodcastPlayer from './components/PodcastPlayer';

function App() {
  const playerRef = useRef(null);
  const [theme, setTheme] = useState('light');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

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

  const handleHome = () => {
    setIsGenerating(false);
    setIsPlaying(false);
    // Scroll to top smoothly
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleGenerate = () => {
    setIsGenerating(true);

    // Simulate podcast generation (2 seconds)
    setTimeout(() => {
      setIsGenerating(false);
      setIsPlaying(true);

      // Scroll to player after generation
      setTimeout(() => {
        playerRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 100);
    }, 2000);
  };

  return (
    <div className="app-container">
      <Header theme={theme} toggleTheme={toggleTheme} onHomeClick={handleHome} />
      <main>
        <PromptInput onGenerate={handleGenerate} isGenerating={isGenerating} isPlaying={isPlaying} />
        <div ref={playerRef} className="w-full flex justify-center">
          <PodcastPlayer isGenerating={isGenerating} isPlaying={isPlaying} />
        </div>
      </main>
    </div>
  );
}

export default App;
