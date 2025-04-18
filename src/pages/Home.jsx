import Navbar from "../components/Navbar";
import SportSection from "../components/SportSection";
import Chatbot from "../components/Chatbot";

export default function Home() {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
   
      <Navbar />

      <div className="flex flex-1 min-h-0">
        
        <div className="hidden lg:block lg:w-2/3 overflow-y-auto">
          <SportSection />
        </div>
        
        
        <div className="hidden lg:block fixed right-0 top-16 bottom-0 w-1/3 bg-white border-l border-gray-200">
          <Chatbot />
        </div>
        
       
        <div className="w-full lg:hidden overflow-y-auto">
          <SportSection />
        </div>
      </div>

      
      <div className="lg:hidden">
        <Chatbot />
      </div>
    </div>
  );
}