import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

export default function CommentaryPage() {
  const { matchcode } = useParams(); // ✅ Extracts the match code from URL
  const [commentary, setCommentary] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:4001/api/commentary/${matchcode}`)
      .then((res) => {setCommentary(res.data.commentary)
        console.log(res.data)})
      .catch((err) => console.error("Error fetching commentary:", err));

    console.log(commentary)
  }, [matchcode]);

  return (
    <div>
      <h2>Commentary for Match: {matchcode}</h2>
      {Array.isArray(commentary) ? (
        commentary.map((item, index) => (
          <div key={index}>
            <strong>{item.ball}:</strong> {item.commentary}
          </div>
        ))
      ) : (
        <p>Loading or no commentary found.</p>
      )}
    </div>
  );
}
