import React from 'react';

const Logo = () => {
  return (
    <div className="flex items-center space-x-2">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-8 w-8 text-primary"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <path d="M12 18h.01" />
        <path d="M12 15h.01" />
        <path d="M12 12h.01" />
      </svg>
      <span className="text-2xl font-bold text-gray-800">AdvocAI</span>
    </div>
  );
};

export default Logo;
