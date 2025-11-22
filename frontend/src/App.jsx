import React, { useRef, useState, useEffect } from 'react';
import Header from './components/Header';
import PromptInput from './components/PromptInput';
import PodcastPlayer from './components/PodcastPlayer';
import About from './components/About';
import { generatePodcastSequence, confirmTopicReceived } from './services/api';

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

  const [podcastData, setPodcastData] = useState(null);
  const [podcastSequence, setPodcastSequence] = useState([]);
  const [currentTopicIndex, setCurrentTopicIndex] = useState(0);
  const [currentSequenceId, setCurrentSequenceId] = useState(null);
  const [error, setError] = useState(null);

  const handleHome = () => {
    setIsGenerating(false);
    setIsPlaying(false);
    setPodcastSequence([]);
    setCurrentTopicIndex(0);
    setCurrentSequenceId(null);
    // Scroll to top smoothly
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleGenerate = async (topics, sponsors = []) => {
    if (!topics || topics.length === 0) {
      alert('Please enter at least one topic');
      return;
    }

    console.log('🎙️  Starting podcast generation for topics:', topics);
    setIsGenerating(true);
    setError(null);
    setPodcastData(null);
    setPodcastSequence([]);
    setCurrentTopicIndex(0);
    setIsPlaying(false);

    try {
      console.log('📡 Calling backend API for sequence...');
      
      // Handle topic completion callback
      const handleTopicComplete = async (topicData, index, seqId) => {
        console.log(`✅ Topic ${index + 1} generated:`, topicData);
        
        // Store sequence ID
        if (seqId && !currentSequenceId) {
          setCurrentSequenceId(seqId);
        }
        
        // Add to sequence
        setPodcastSequence(prev => {
          const newSeq = [...prev];
          newSeq[index] = topicData;
          return newSeq;
        });
        
        // Set as current data and show player
        setPodcastData(topicData);
        setCurrentTopicIndex(index);
        setIsGenerating(index < topics.length - 1); // Still generating if more topics
        setIsPlaying(true);
        
        // Scroll to player after generation
        setTimeout(() => {
          playerRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
      };
      
      // Generate sequence using the API function
      const { results, sequence_id } = await generatePodcastSequence(
        topics, 
        sponsors, 
        handleTopicComplete
      );
      
      setCurrentSequenceId(sequence_id);
      
      console.log('✅ All topics generated successfully!', results);
      setIsGenerating(false);
      
    } catch (err) {
      console.error('❌ Error generating podcast:', err);
      const errorMessage = err.message || 'Failed to generate podcast. Make sure the backend is running on http://localhost:5001';
      setError(errorMessage);
      setIsGenerating(false);
      setIsPlaying(false);
      alert(`Error: ${errorMessage}`);
    }
  };

  return (
    <div className="app-container">
      <Header theme={theme} toggleTheme={toggleTheme} onHomeClick={handleHome} />
      <main>
        <PromptInput onGenerate={handleGenerate} isGenerating={isGenerating} isPlaying={isPlaying} />
        {error && (
          <div className="w-full max-w-[800px] mx-auto p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg mb-4">
            {error}
          </div>
        )}
        <div ref={playerRef} className="w-full flex justify-center">
          <PodcastPlayer 
            isGenerating={isGenerating} 
            isPlaying={isPlaying} 
            podcastData={podcastData}
          />
        </div>
        <About />
      </main>
    </div>
  );
}

export default App;
