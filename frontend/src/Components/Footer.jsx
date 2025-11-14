import React from "react";

const Footer = () => {
  return (
    <footer className="bg-white border-t">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-800">AdvocAI</h4>
            <p className="text-gray-600">Navigate Legal Documents with AI</p>
          </div>
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-800">Links</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Home</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">About</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Contact</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-800">Legal</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Terms of Service</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Privacy Policy</a></li>
            </ul>
          </div>
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-800">Connect</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-gray-800">Twitter</a></li>
              <li><a href="#" className="text-gray-600 hover:text-gray-800">LinkedIn</a></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-200 pt-8 text-center">
          <p className="text-gray-600">&copy; {new Date().getFullYear()} AdvocAI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
