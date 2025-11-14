import React from 'react';
import { Link } from 'react-router-dom';

const lawyers = [
  {
    id: 1,
    name: 'John Doe',
    specialty: 'Corporate Law',
    avatar: 'JD',
  },
  {
    id: 2,
    name: 'Jane Smith',
    specialty: 'Family Law',
    avatar: 'JS',
  },
  // Add more lawyers as needed
];

const Lawyers = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Our Lawyers</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {lawyers.map((lawyer) => (
            <Link to={`/lawyer-profile/${lawyer.id}`} key={lawyer.id}>
              <div className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center text-center hover:shadow-xl transition-shadow duration-300">
                <div className="w-24 h-24 bg-blue-500 text-white rounded-full flex items-center justify-center text-4xl font-bold mb-4">
                  {lawyer.avatar}
                </div>
                <h2 className="text-xl font-bold text-gray-800">{lawyer.name}</h2>
                <p className="text-gray-600">{lawyer.specialty}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Lawyers;
