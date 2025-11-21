import React from 'react';

const Header = ({ theme, toggleTheme }) => {
    return (
        <header className="w-full flex justify-between items-center px-lg py-md bg-transparent absolute top-0 z-50">
            <div className="flex items-center gap-sm font-display text-2xl font-bold text-text">
                <span className="text-2xl">🎙️</span>
            </div>
            <nav className="flex items-center">
                <button className="bg-transparent border-none text-text-muted text-base ml-md transition-colors hover:text-text font-light">History</button>
                <button className="bg-transparent border-none text-text-muted text-base ml-md transition-colors hover:text-text font-light">Settings</button>
                <button
                    onClick={toggleTheme}
                    className="bg-transparent border-none text-2xl ml-md cursor-pointer transition-transform hover:scale-110 active:scale-95"
                    aria-label="Toggle Theme"
                >
                    {theme === 'light' ? '🌙' : '☀️'}
                </button>
            </nav>
        </header>
    );
};

export default Header;
