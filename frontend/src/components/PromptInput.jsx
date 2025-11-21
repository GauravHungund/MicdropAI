import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const PromptInput = ({ onGenerate, isGenerating, isPlaying }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    console.log('Generating podcast for:', prompt);
    if (onGenerate) onGenerate();
    // TODO: Connect to backend
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
            {"MicDrop Ai".split("").map((char, index) => (
              <motion.span
                key={index}
                className="inline-block"
                variants={{
                  initial: { x: 0, y: 0, rotate: 0, opacity: 1 },
                  hover: {
                    x: [0, (Math.random() - 0.5) * 1000, (Math.random() - 0.5) * 1000], // Scatter horizontally, then maintain
                    y: [0, 0, 1000], // Stay up, then fall
                    rotate: [0, (Math.random() - 0.5) * 180, (Math.random() - 0.5) * 360], // Rotate during scatter and fall
                    opacity: [1, 1, 0], // Fade out during fall
                    transition: {
                      duration: 3,
                      times: [0, 0.3, 1], // 30% scatter, 70% fall
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
          className="w-full max-w-[800px] flex flex-col gap-md mb-xl"
          onSubmit={handleSubmit}
        >
          <div className="relative w-full flex gap-sm items-center bg-white border border-gray-200 rounded-full p-2 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <input
              type="text"
              className="flex-1 p-sm bg-transparent border-none text-text font-sans text-lg focus:outline-none ml-sm"
              placeholder="Describe your podcast topic..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <button type="submit" className="px-lg py-sm bg-black text-white rounded-full font-medium hover:bg-gray-800 transition-colors">
              Generate Podcast
            </button>
          </div>
        </motion.form>
      </motion.section>
    </AnimatePresence>
  );
};

export default PromptInput;
