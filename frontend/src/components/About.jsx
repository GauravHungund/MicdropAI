import React from 'react';
import { motion } from 'framer-motion';

const About = () => {
    return (
        <section id="about" className="w-full min-h-screen flex flex-col items-center justify-center py-xl px-lg bg-background">
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ duration: 0.8 }}
                className="max-w-[800px] text-center"
            >
                <h2 className="text-7xl font-black text-text mb-xl">About Us</h2>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="space-y-md"
                >
                    <p className="text-text-muted text-lg leading-relaxed mt-lg">
                        EchoDuo is an autonomous, multi-agent AI podcast system that doesn’t just generate content — it thinks, acts, evolves, and publishes on its own.

                        Unlike traditional AI tools that require constant human prompts and editing, EchoDuo operates as a coordinated network of intelligent agents:

                        One agent identifies what information is needed

                        Another agent retrieves real-world data from the internet

                        Another agent writes a human-like conversation

                        A memory system ensures evolution over time

                        A voice engine turns text into real audio

                        A publishing system stores and organizes every episode

                        Every episode is a natural conversation between two distinct personas, Alex (curious & empathetic) and Maya (analytical & grounded), designed to reflect how real people explore complex topics together.

                        EchoDuo also integrates sponsors seamlessly and organically, embedding them as lived experiences or practical tools — never as disruptive ads.

                        At its core, EchoDuo is a demonstration of what happens when AI stops being a tool and starts becoming a living, learning system.
                    </p>


                </motion.div>
            </motion.div>
        </section>
    );
};

export default About;
