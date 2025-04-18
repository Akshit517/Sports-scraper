import { useEffect, useState } from "react"
import MatchCard from "./MatchCard"

export default function SportSection() {
  const [matches, setMatches] = useState([])

  useEffect(() => {
    fetch("http://localhost:4001/api/live-stats/")
      .then(res => res.json())
      .then(data => setMatches(data))
      .catch(err => console.error("Error fetching matches:", err))
  }, [])

  // Group matches by tournament
  const groupedMatches = matches.reduce((acc, match) => {
    const tournament = match.tournament || "Unknown Tournament";
    if (!acc[tournament]) {
      acc[tournament] = [];
    }
    acc[tournament].push(match);
    return acc;
  }, {});

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-6">Live Cricket Matches</h2>

      {/* Render each tournament row */}
      {Object.keys(groupedMatches).map(tournament => (
        <div key={tournament} className="mb-8">
          <h3 className="text-xl font-semibold mb-4">{tournament}</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {/* Render matches for the current tournament */}
            {groupedMatches[tournament].map(match => (
              <MatchCard key={match.id} match={match} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
