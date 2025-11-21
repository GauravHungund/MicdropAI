import React from 'react';
import { motion } from 'framer-motion';

const PodcastPlayer = ({ isGenerating, isPlaying }) => {
    // Dummy transcript data
    const transcript = "Welcome to this podcast about the fascinating world of AI and machine learning. Today we'll explore how neural networks are revolutionizing the way we interact with technology.";

    if (!isGenerating && !isPlaying) {
        return null; // Don't show anything initially
    }

    if (isGenerating) {
        // Loading state
        return (
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-[800px] flex flex-col items-center justify-center min-h-[300px] gap-md"
            >
                <div className="flex gap-[6px] items-end h-[60px]">
                    {[...Array(12)].map((_, i) => (
                        <motion.span
                            key={i}
                            className="block w-[8px] bg-primary rounded-[4px]"
                            animate={{
                                height: [20, 60, 20],
                            }}
                            transition={{
                                duration: 1,
                                repeat: Infinity,
                                delay: i * 0.1,
                                ease: "easeInOut",
                            }}
                        />
                    ))}
                </div>
                <p className="text-text-muted text-lg">Generating your podcast...</p>
            </motion.div>
        );
    }

    // Playing state
    return (
        <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-full flex flex-col items-center gap-xl p-xl"
        >
            {/* Waveform Animation - Full Width */}
            <div className="w-full flex items-end h-[150px] justify-center gap-[4px]">
                {[...Array(300)].map((_, i) => {
                    const min = 20;
                    const max = 120;
                    const randomHeight1 = Math.random() * (max - min) + min;
                    const randomHeight2 = Math.random() * (max - min) + min;

                    return (
                        <motion.span
                            key={i}
                            className="bg-black rounded-[6px] flex-1 max-w-[20px]"
                            animate={{
                                height: [randomHeight1, randomHeight2, randomHeight1],
                            }}
                            transition={{
                                duration: Math.random() * 1.2 + 1.5, // slower + random
                                repeat: Infinity,
                                delay: i * 0.015, // smooth wave ripple
                                ease: "easeInOut",
                            }}
                        />
                    );
                })}
            </div>

            {/* Transcript Display */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.8 }}
                className="w-full bg-surface border border-border rounded-lg p-lg shadow-lg"
            >
                <h3 className="text-text font-bold text-xl mb-md">Transcript</h3>
                <p className="text-text-muted text-base leading-relaxed">
                    {transcript}
                </p>
            </motion.div>

            {/* Playback Controls (Optional) */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.8 }}
                className="flex gap-md items-center"
            >
                <button className="w-[60px] h-[60px] rounded-full bg-primary text-white border-none text-3xl flex items-center justify-center shadow-lg hover:scale-110 transition-transform">
                    ▶
                </button>
            </motion.div>
        </motion.div>
    );
};

export default PodcastPlayer;
