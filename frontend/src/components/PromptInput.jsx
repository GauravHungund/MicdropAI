import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRocket } from 'react-icons/fa';

const PromptInput = ({ onGenerate, isGenerating, isPlaying }) => {
  const [sponsorsPrompt, setSponsorsPrompt] = useState('');
  const [myTopicsPrompt, setMyTopicsPrompt] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate input - at least one field must have content
    if (!sponsorsPrompt.trim() && !myTopicsPrompt.trim()) {
      alert('Please enter at least a topic or sponsor information');
      return;
    }
    
    if (isGenerating) {
      console.log('⏳ Already generating, please wait...');
      return;
    }
    
    // Parse topics and sponsors as arrays (split by newlines or commas)
    const parseList = (text) => {
      return text
        .split(/[,\n]/)
        .map(item => item.trim())
        .filter(item => item.length > 0);
    };
    
    const topics = parseList(myTopicsPrompt);
    const sponsors = parseList(sponsorsPrompt);
    
    // Validate we have at least one topic
    if (topics.length === 0 && sponsors.length === 0) {
      alert('Please enter at least one topic or sponsor');
      return;
    }
    
    // If no topics but sponsors, use sponsors as topics
    const finalTopics = topics.length > 0 ? topics : sponsors;
    const finalSponsors = topics.length > 0 ? sponsors : [];
    
    console.log('📝 Form submitted - Topics:', finalTopics, 'Sponsors:', finalSponsors);
    
    if (onGenerate) {
      try {
        // Pass arrays to the parent component's handler
        await onGenerate(finalTopics, finalSponsors);
        // Clear the inputs after successful submission
        setMyTopicsPrompt('');
        setSponsorsPrompt('');
      } catch (error) {
        console.error('❌ Error in handleSubmit:', error);
        // Error handling is done in App.jsx
      }
    } else {
      console.error('❌ onGenerate handler not provided');
      alert('Error: Generate handler not available');
    }
  };

  // Don't render if generating or playing
  if (isGenerating || isPlaying) return null;

  return (
    <AnimatePresence>
      <motion.section
        initial={{ opacity: 1 }}
        exit={{ opacity: 0, y: -50 }}
        transition={{ duration: 0.5 }}
        className="flex flex-col items-center justify-center w-full min-h-[80vh] relative"
      >
        <div className="flex-1 flex flex-col items-center justify-center mb-xl">
          <motion.h1
            className="text-9xl font-black text-text mb-xl tracking-tight cursor-default relative z-10"
            initial="initial"
            whileHover="hover"
          >
            {"MicDrop AI".split("").map((char, index) => (
              <motion.span
                key={index}
                className="inline-block"
                variants={{
                  initial: { x: 0, y: 0, rotate: 0, opacity: 1 },
                  hover: {
                    x: [0, (Math.random() - 0.5) * 1000, (Math.random() - 0.5) * 1000],
                    y: [0, 0, 1000],
                    rotate: [0, (Math.random() - 0.5) * 180, (Math.random() - 0.5) * 360],
                    opacity: [1, 1, 0],
                    transition: {
                      duration: 3,
                      times: [0, 0.3, 1],
                      ease: [0.6, 0, 0.2, 1],
                    },
                  },
                }}
              >
                {char === ' ' ? '\u00A0' : char}
              </motion.span>
            ))}
          </motion.h1>
          <motion.p
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="text-text-muted text-md font-light max-w-[500px] text-center mt-lg"
          >
            Turn any topic into an engaging audio experience with seamless ad integration
          </motion.p>
        </div>

        <motion.form
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="w-full max-w-[800px] mb-xl"
          onSubmit={handleSubmit}
        >
          <div className="relative w-full bg-white border border-gray-200 rounded-3xl p-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
            {/* Two Column Layout */}
            <div className="flex gap-0">
              {/* Sponsors Column */}
              <div className="flex-1 flex flex-col">
                <h3 className="text-sm font-semibold text-gray-700 mb-sm">Sponsors</h3>
                <textarea
                  className="w-full h-[120px] p-sm bg-transparent border-none text-text font-sans text-base focus:outline-none resize-none"
                  placeholder="Enter sponsors (one per line or comma-separated)..."
                  value={sponsorsPrompt}
                  onChange={(e) => setSponsorsPrompt(e.target.value)}
                />
              </div>

              {/* Vertical Divider */}
              <div className="w-[1px] bg-gray-300 mx-md"></div>

              {/* My Topics Column */}
              <div className="flex-1 flex flex-col">
                <h3 className="text-sm font-semibold text-gray-700 mb-sm">My Topics</h3>
                <textarea
                  className="w-full h-[120px] p-sm bg-transparent border-none text-text font-sans text-base focus:outline-none resize-none"
                  placeholder="Enter topics (one per line or comma-separated)..."
                  value={myTopicsPrompt}
                  onChange={(e) => setMyTopicsPrompt(e.target.value)}
                />
              </div>
            </div>

            {/* Centered Submit Button */}
            <div className="flex justify-center mt-md">
              <button
                type="submit"
                className="px-xl py-md bg-black text-white rounded-full font-medium hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-sm"
              >
                <FaRocket className="text-base" />
                <span>Generate Podcast</span>
              </button>
            </div>
          </div>
        </motion.form>
      </motion.section>
    </AnimatePresence>
  );
};

export default PromptInput;
