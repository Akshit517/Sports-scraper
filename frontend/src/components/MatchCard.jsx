
import { useNavigate } from 'react-router-dom'
export default function MatchCard({ match }) {

 const navigate = useNavigate()

  const handleShowCommentary = () => {
    navigate(`/commentary/${match.matchcode}`)
  }
    return (
      <div className="bg-white rounded-lg shadow-md overflow-hidden w-64 flex-shrink-0">
        <div className="relative h-32">
          <img 
            src="\cricket.jpg"
            alt={match.teams}
            className="w-full h-full object-cover"
          />
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2">
            <span className="text-xs text-white">{match.tournament}</span>
          </div>
        </div>
        <div className="p-3">
          <h3 className="font-semibold text-gray-800">{match.teams}</h3>
          <div className="flex justify-between items-center mt-2">
            <span className="text-sm text-gray-600">{match.score}</span>
            <button className="text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600" onClick={handleShowCommentary}>
              <svg className="inline mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"/>
              </svg>
              Commentary
            </button>
          </div>
        </div>
      </div>
    );
  }
