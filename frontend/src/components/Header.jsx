import React from 'react';
import { FaMicrophone, FaHome, FaInfoCircle, FaCog, FaMoon, FaSun } from 'react-icons/fa';

const Header = ({ theme, toggleTheme, onHomeClick }) => {
    const scrollToAbout = () => {
        const aboutSection = document.getElementById('about');
        if (aboutSection) {
            aboutSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    return (
        <header className="w-full flex justify-between items-center px-lg py-md bg-transparent absolute top-0 z-50">
            <div className="flex items-center gap-sm font-display text-2xl font-bold text-text">
                <FaMicrophone className="text-2xl text-primary" />
            </div>
            <nav className="flex items-center">
                <button
                    onClick={onHomeClick}
                    className="bg-transparent border-none text-text-muted text-base ml-md transition-colors hover:text-text font-light flex items-center gap-xs"
                >
                    <FaHome />
                    <span>Home</span>
                </button>
                <button
                    onClick={scrollToAbout}
                    className="bg-transparent border-none text-text-muted text-base ml-md transition-colors hover:text-text font-light flex items-center gap-xs"
                >
                    <FaInfoCircle />
                    <span>About</span>
                </button>
                <button className="bg-transparent border-none text-text-muted text-base ml-md transition-colors hover:text-text font-light flex items-center gap-xs">
                    <FaCog />
                    <span>Settings</span>
                </button>
                <button
                    onClick={toggleTheme}
                    className="bg-transparent border-none text-2xl ml-md cursor-pointer transition-transform hover:scale-110 active:scale-95 text-text-muted hover:text-text"
                    aria-label="Toggle Theme"
                >
                    {theme === 'light' ? <FaMoon /> : <FaSun />}
                </button>
            </nav>
        </header>
    );
};

export default Header;
