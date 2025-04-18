import { useState, useEffect } from 'react';
import { 
  PaperAirplaneIcon, 
  MicrophoneIcon, 
  ChatBubbleOvalLeftIcon,
  XMarkIcon 
} from '@heroicons/react/24/solid';

import axios from 'axios';

export default function Chatbot() {
  const [isMobile, setIsMobile] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleResize = () => {
    
      setIsMobile(window.innerWidth < 700);
    };
    
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

 const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

 const handleSend = async () => {
  try {
    const response = await axios.post("http://localhost:4001/api/chatbot/", {
      message: message, // replace with your input variable
    }, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    console.log(response.data.reply);
    setResponse(response.data.reply);
  } catch (error) {
    console.error("Chat error:", error.response?.data || error.message);
  }
};
  if (isMobile) {
    return (
      <>
        
        {!isOpen && (
          <div className="fixed bottom-6 right-6 z-[1000]">
            <button
              onClick={() => setIsOpen(true)}
              className="bg-blue-600 text-white p-4 rounded-full shadow-xl hover:bg-blue-700 transition-all transform hover:scale-110"
              aria-label="Open chat"
            >
              <ChatBubbleOvalLeftIcon className="h-6 w-6" />
            </button>
          </div>
        )}


        {isOpen && (
          <div className="fixed inset-0 bg-[#343541] z-[1000] flex flex-col">

            <div className="flex justify-between items-center p-4 bg-[#202123] border-b border-gray-700">
              <h3 className="text-lg font-semibold text-white">Sports Assistant</h3>
              <button 
                onClick={() => setIsOpen(false)}
                className="p-2 text-gray-400 hover:text-white"
                aria-label="Close chat"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4">
              <div className="bg-[#40414f] rounded-lg p-3 mb-3 max-w-[80%] text-white">
                <p>Welcome! Ask me about live matches.</p>
              </div>
            </div>
            
            <div className="sticky bottom-0 p-4 bg-[#202123] border-t border-gray-700">
              <div className="flex gap-2">
                <button className="p-2 text-gray-400 hover:text-white">
                  <MicrophoneIcon className="h-5 w-5" />
                </button>
                <input 
                  type="text" 
                  placeholder="Type your question..." 
                  className="flex-1 p-2 rounded-lg bg-[#40414f] border border-gray-600 text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                <button className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  <PaperAirplaneIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        )}
      </>
    );
  }


  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col border-l border-dark-600 bg-dark-700 overflow-hidden">
     
      <div className="p-4 bg-dark-600 border-b border-dark-500">
        <h3 className="text-lg font-semibold text-white">Sports Assistant</h3>
      </div>
      

      <div className="flex-1 p-4 overflow-y-auto">
        <div className="bg-dark-600 rounded-lg p-3 mb-3 max-w-[80%] text-white">
          <p>Welcome! Ask me about live matches.</p>
          </div>
        <div className="bg-dark-600 rounded-lg p-3 mb-3 max-w-[80%] text-white">
          <p>{response}</p>
        </div>
      </div>
      

      <div className="sticky bottom-0 p-4 bg-dark-600 border-t border-dark-500">
        <div className="flex gap-2">
          <button className="p-2 text-dark-200 hover:text-white">
            <MicrophoneIcon className="h-5 w-5" />
          </button>
          <input 
            type="text" 
            placeholder="Type your question..." 
            className="flex-1 p-2 rounded-lg bg-dark-700 border border-dark-500 focus:outline-none focus:ring-1 focus:ring-dark-400 text-white"
            onChange={(e) => setMessage(e.target.value)}
          />
          <button className="p-2 bg-dark-400 text-white rounded-lg hover:bg-dark-300" onClick={handleSend}>
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
