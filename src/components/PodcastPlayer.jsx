import React from 'react';

const PodcastPlayer = () => {
    return (
        <div className="w-full max-w-[800px] bg-surface border border-border rounded-lg p-lg mt-lg shadow-lg">
            <div className="flex flex-col items-center justify-center h-[200px] text-text-muted gap-md">
                <div className="flex gap-[4px] items-center h-[40px]">
                    <span className="block w-[6px] bg-primary rounded-[4px] animate-wave h-[20px] [animation-delay:0.1s]"></span>
                    <span className="block w-[6px] bg-primary rounded-[4px] animate-wave h-[40px] [animation-delay:0.2s]"></span>
                    <span className="block w-[6px] bg-primary rounded-[4px] animate-wave h-[30px] [animation-delay:0.3s]"></span>
                    <span className="block w-[6px] bg-primary rounded-[4px] animate-wave h-[40px] [animation-delay:0.4s]"></span>
                    <span className="block w-[6px] bg-primary rounded-[4px] animate-wave h-[20px] [animation-delay:0.5s]"></span>
                </div>
                <p>Your generated podcast will appear here</p>
            </div>

            {/* Hidden for now, will be toggled when podcast is ready */}
            <div className="flex flex-col gap-md" style={{ display: 'none' }}>
                <div className="flex justify-between items-center">
                    <h3 className="font-bold">The History of Nike Air Jordan</h3>
                    <span className="bg-secondary text-white px-2 py-[2px] rounded-sm text-xs font-bold uppercase">Ad: Nike Store</span>
                </div>
                <div className="w-full h-[6px] bg-[#333] rounded-[3px] overflow-hidden">
                    <div className="h-full bg-primary" style={{ width: '30%' }}></div>
                </div>
                <div className="flex justify-center gap-md items-center">
                    <button className="text-2xl">⏮</button>
                    <button className="w-[50px] h-[50px] rounded-full bg-white text-black border-none text-2xl flex items-center justify-center shadow-[0_0_15px_rgba(255,255,255,0.3)]">▶</button>
                    <button className="text-2xl">⏭</button>
                </div>
            </div>
        </div>
    );
};

export default PodcastPlayer;

