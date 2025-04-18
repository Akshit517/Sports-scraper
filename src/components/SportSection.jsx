import MatchCard from "./MatchCard"

const cricketMatches = [
  { id: 1, teams: "IND vs AUS", tournament: "ICC World Cup", score: "IND 289/5 (45.2)", sport: "cricket" },
  { id: 2, teams: "ENG vs NZ", tournament: "Test Series", score: "ENG 210/3 (62.1)", sport: "cricket" },
  { id: 3, teams: "SA vs PAK", tournament: "T20 League", score: "SA 165/4 (18.3)", sport: "cricket" },
  { id: 4, teams: "WI vs BAN", tournament: "ODI Series", score: "WI 190/2 (32.4)", sport: "cricket" },
]

const footballMatches = [
  { id: 1, teams: "MCI vs ARS", tournament: "Premier League", score: "2-1 (75')", sport: "football" },
  { id: 2, teams: "RM vs BAR", tournament: "La Liga", score: "1-1 (63')", sport: "football" },
  { id: 3, teams: "PSG vs LIV", tournament: "Champions League", score: "0-0 (22')", sport: "football" },
  { id: 3, teams: "PSG vs LIV", tournament: "Champions League", score: "0-0 (22')", sport: "football" },
  { id: 3, teams: "PSG vs LIV", tournament: "Champions League", score: "0-0 (22')", sport: "football" },
]


export default function SportSection() {
    return (
      <div className="space-y-8">
        <div>
          <h2 className="text-xl font-bold mb-4">Live Cricket</h2>
          <div className="relative">
            <div className="flex overflow-x-auto pb-4 gap-4 scrollbar-hide">
              {cricketMatches.map(match => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-bold mb-4">Live Cricket</h2>
          <div className="relative">
            <div className="flex overflow-x-auto pb-4 gap-4 scrollbar-hide">
              {cricketMatches.map(match => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </div>
        </div>
  
        <div>
          <h2 className="text-xl font-bold mb-4">Live Football</h2>
          <div className="relative">
            <div className="flex overflow-x-auto pb-4 gap-4 scrollbar-hide">
              {footballMatches.map(match => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }