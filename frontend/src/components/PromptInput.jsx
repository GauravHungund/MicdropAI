import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRocket } from 'react-icons/fa';

const PromptInput = ({ onGenerate, isGenerating, isPlaying }) => {
  const [sponsorsPrompt, setSponsorsPrompt] = useState('');
  const [myTopicsPrompt, setMyTopicsPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!sponsorsPrompt.trim() && !myTopicsPrompt.trim()) return;
    console.log('Generating podcast - Sponsors:', sponsorsPrompt, 'My Topics:', myTopicsPrompt);
    if (onGenerate) onGenerate();
    // TODO: Connect to backend with both prompts
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
                  placeholder="Describe sponsor topics..."
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
                  placeholder="Describe your topics..."
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
