import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaPlay } from 'react-icons/fa';

// Format transcript: make sponsor mentions bold and remove unnecessary tags
const formatTranscript = (text) => {
    if (!text) return '';
    
    // Remove *sponsor* markers and make sponsor names bold
    // Pattern: *sponsor*SponsorName*sponsor* → <strong>SponsorName</strong>
    let formatted = text.replace(/\*sponsor\*([^*]+)\*sponsor\*/g, '<strong>$1</strong>');
    
    // Remove any remaining *sponsor* tags that weren't properly paired
    formatted = formatted.replace(/\*sponsor\*/g, '');
    
    // Split by lines to process each dialogue
    const lines = formatted.split('\n');
    const processedLines = lines.map((line, index) => {
        // Skip empty lines
        if (!line.trim()) return null;
        
        // Check if it's a dialogue line (Alex: or Maya:)
        if (line.match(/^(Alex|Maya):/)) {
            return (
                <div key={index} className="mb-2">
                    <span className="font-semibold text-text">
                        {line.split(':')[0]}:
                    </span>
                    <span 
                        className="ml-2"
                        dangerouslySetInnerHTML={{ __html: line.split(':').slice(1).join(':').trim() }}
                    />
                </div>
            );
        }
        
        // Regular line
        return (
            <div key={index} dangerouslySetInnerHTML={{ __html: line }} />
        );
    }).filter(Boolean);
    
    return <>{processedLines}</>;
};

const PodcastPlayer = ({ isGenerating, isPlaying, podcastData }) => {
    const [isAudioPlaying, setIsAudioPlaying] = useState(false);
    const [currentAudioIndex, setCurrentAudioIndex] = useState(0);
    const audioRefs = useRef([]);
    const currentIndexRef = useRef(0);
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';
    
    // Use real podcast data if available, otherwise use placeholder
    const transcript = podcastData?.conversation || 
        "Welcome to this podcast about the fascinating world of AI and machine learning. Today we'll explore how neural networks are revolutionizing the way we interact with technology.";
    
    const topic = podcastData?.topic || '';
    const sponsor = podcastData?.sponsor || '';
    const audioFiles = podcastData?.audio_files || [];
    
    // Handle audio playback
    useEffect(() => {
        if (audioFiles.length > 0 && isAudioPlaying) {
            // Reset index when starting playback
            currentIndexRef.current = 0;
            setCurrentAudioIndex(0);
            playAudioSequence(0);
        }
        
        return () => {
            // Cleanup: stop all audio when component unmounts
            audioRefs.current.forEach(audio => {
                if (audio) {
                    audio.pause();
                    audio.currentTime = 0;
                }
            });
        };
    }, [audioFiles, isAudioPlaying]);
    
    const playAudioSequence = (index) => {
        // Use the passed index parameter instead of state
        const currentIdx = index;
        
        if (currentIdx >= audioFiles.length) {
            setIsAudioPlaying(false);
            setCurrentAudioIndex(0);
            currentIndexRef.current = 0;
            return;
        }
        
        const audioUrl = `${API_BASE_URL}${audioFiles[currentIdx]}`;
        const audio = new Audio(audioUrl);
        audioRefs.current[currentIdx] = audio;
        
        // Update state for UI display
        setCurrentAudioIndex(currentIdx);
        currentIndexRef.current = currentIdx;
        
        audio.onended = () => {
            const nextIndex = currentIdx + 1;
            if (nextIndex < audioFiles.length) {
                // Play next audio after a small delay
                setTimeout(() => {
                    playAudioSequence(nextIndex);
                }, 200);
            } else {
                // All audio files played
                setIsAudioPlaying(false);
                setCurrentAudioIndex(0);
                currentIndexRef.current = 0;
            }
        };
        
        audio.onerror = () => {
            console.error(`Failed to load audio: ${audioUrl}`);
            // Try next audio on error
            const nextIndex = currentIdx + 1;
            if (nextIndex < audioFiles.length) {
                setTimeout(() => {
                    playAudioSequence(nextIndex);
                }, 200);
            } else {
                setIsAudioPlaying(false);
                setCurrentAudioIndex(0);
                currentIndexRef.current = 0;
            }
        };
        
        audio.play().catch(err => {
            console.error('Error playing audio:', err);
            setIsAudioPlaying(false);
        });
    };
    
    const handlePlayPause = () => {
        if (audioFiles.length === 0) {
            alert('No audio files available. Make sure ElevenLabs API key is configured.');
            return;
        }
        
        if (isAudioPlaying) {
            // Pause current audio
            audioRefs.current.forEach(audio => {
                if (audio) {
                    audio.pause();
                }
            });
            setIsAudioPlaying(false);
        } else {
            // Start playing from beginning
            currentIndexRef.current = 0;
            setCurrentAudioIndex(0);
            setIsAudioPlaying(true);
        }
    };

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
            <div className="w-full flex items-end h-[200px] justify-center gap-[4px]">
                {[...Array(250)].map((_, i) => {
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
                <div className="mb-md">
                    {topic && (
                        <h2 className="text-text font-bold text-2xl mb-sm">{topic}</h2>
                    )}
                    {sponsor && (
                        <p className="text-text-muted text-sm">Sponsored by: <span className="font-bold text-primary">{sponsor}</span></p>
                    )}
                </div>
                <h3 className="text-text font-bold text-xl mb-md">Transcript</h3>
                <div className="text-text-muted text-base leading-relaxed whitespace-pre-wrap font-mono">
                    {formatTranscript(transcript)}
                </div>
            </motion.div>

            {/* Playback Controls */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.8 }}
                className="flex gap-md items-center flex-col"
            >
                {audioFiles.length > 0 ? (
                    <>
                        <button 
                            onClick={handlePlayPause}
                            className="w-[60px] h-[60px] rounded-full bg-primary text-white border-none text-3xl flex items-center justify-center shadow-lg hover:scale-110 transition-transform cursor-pointer"
                        >
                            {isAudioPlaying ? '⏸' : <FaPlay />}
                        </button>
                        <p className="text-text-muted text-sm mt-2">
                            {isAudioPlaying 
                                ? `Playing dialogue ${currentAudioIndex + 1} of ${audioFiles.length}`
                                : `${audioFiles.length} audio file${audioFiles.length !== 1 ? 's' : ''} ready`
                            }
                        </p>
                    </>
                ) : (
                    <p className="text-text-muted text-sm">
                        Audio generation not available (ElevenLabs not configured)
                    </p>
                )}
            </motion.div>
        </motion.div>
    );
};

export default PodcastPlayer;
