# # chatbot.py
# import pathway as pw
# import cohere
# from datetime import datetime
# import threading
# import numpy as np
# from typing import List, Dict
# from config import Config
# import gradio as gr

# class CricketChatbot:
#     def __init__(self):
#         self.co = cohere.Client(Config.COHERE_API_KEY)
#         self.conversations: List[Dict] = []
#         self.last_update = None
#         self.lock = threading.Lock()  # For thread-safe operations
#         self.setup_data_pipeline()
#         self.start_pathway_thread()

#     def setup_data_pipeline(self):
#         """Set up Pathway data processing pipeline"""
#         from scraper import create_cricket_stream
        
#         self.match_stream = create_cricket_stream()
        
#         # Enrich with context for chatbot
#         self.enriched_data = self.match_stream.select(
#             *pw.this,
#             context=pw.apply(
#                 lambda r: (
#                     f"Series: {r.series}\nTeams: {r.team1} vs {r.team2}\n"
#                     f"Scores: {r.score1} vs {r.score2}\n"
#                     f"Overs: {r.over1} vs {r.over2}\nStatus: {r.status}\n"
#                     f"Updated: {datetime.fromisoformat(r.timestamp).strftime('%H:%M:%S')}"
#                 ),
#                 pw.this
#             )
#         )
        
#         pw.io.subscribe(self.enriched_data, self.on_match_update)

#     def start_pathway_thread(self):
#         """Run Pathway in background thread"""
#         def pathway_runner():
#             try:
#                 pw.run(monitoring_level=pw.MonitoringLevel.NONE)
#             except Exception as e:
#                 print(f"Pathway runtime error: {str(e)}")
#                 # Implement restart logic if needed
        
#         thread = threading.Thread(target=pathway_runner, daemon=True)
#         thread.start()

#     def on_match_update(self, match):
#         """Process new match data and update embeddings"""
#         with self.lock:
#             self.last_update = datetime.fromisoformat(match.timestamp)
            
#             qa_pairs = [
#                 ("Who is playing?", f"{match.team1} vs {match.team2}"),
#                 ("What's the score?", f"{match.score1} vs {match.score2}"),
#                 ("Overs played?", f"{match.over1} vs {match.over2}"),
#                 ("Match status?", match.status),
#                 ("Which series?", match.series)
#             ]
            
#             new_conversations = []
#             for question, answer in qa_pairs:
#                 new_conversations.append({
#                     "context": match.context,
#                     "question": question,
#                     "answer": answer,
#                     "timestamp": match.timestamp
#                 })
            
#             self.update_embeddings(new_conversations)

#     def update_embeddings(self, conversations: List[Dict]):
#         """Generate and store embeddings for new data"""
#         contexts = [conv["context"] for conv in conversations]
        
#         try:
#             # Get embeddings from Cohere
#             response = self.co.embed(
#                 texts=contexts,
#                 model=Config.EMBEDDING_MODEL,
#                 input_type="search_document"
#             )
            
#             # Add embeddings to conversations
#             for conv, embedding in zip(conversations, response.embeddings):
#                 conv["embedding"] = np.array(embedding)  # Store as numpy array for efficient similarity calc
#                 self.conversations.append(conv)
                
#             # Keep only the most recent conversations (optional)
#             self.conversations = sorted(
#                 self.conversations,
#                 key=lambda x: x["timestamp"],
#                 reverse=True
#             )[:1000]  # Keep last 1000 conversations
                
#         except Exception as e:
#             print(f"Embedding update failed: {str(e)}")

#     def generate_response(self, query: str) -> str:
#         """Generate response using Cohere API and match data"""
#         with self.lock:  # Ensure thread-safe access to conversations
#             if not self.conversations:
#                 return "No match data available yet. Please try again soon."
            
#             try:
#                 # Get query embedding
#                 embed_response = self.co.embed(
#                     texts=[query],
#                     model=Config.EMBEDDING_MODEL,
#                     input_type="search_query"
#                 )
#                 query_embed = np.array(embed_response.embeddings[0])
                
#                 # Calculate cosine similarities
#                 similarities = []
#                 for conv in self.conversations:
#                     similarity = np.dot(query_embed, conv["embedding"]) / (
#                         np.linalg.norm(query_embed) * np.linalg.norm(conv["embedding"])
#                     )
#                     similarities.append((similarity, conv))
                
#                 # Get top 3 most relevant
#                 top_matches = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]
#                 context = "\n\n".join([match[1]["context"] for match in top_matches])
                
#                 # Generate response
#                 response = self.co.chat(
#                     message=query,
#                     model=Config.CHAT_MODEL,
#                     temperature=Config.CHAT_TEMPERATURE,
#                     preamble=f"Current cricket match information:\n{context}"
#                 )
#                 return response.text
                
#             except Exception as e:
#                 return f"Sorry, I couldn't process your request. Error: {str(e)}"

# def create_chat_interface():
#     """Create Gradio chat interface"""
#     chatbot = CricketChatbot()
    
#     with gr.Blocks(theme=gr.themes.Soft(), title="Live Cricket Chatbot") as demo:
#         gr.Markdown("""
#         # 🏏 Live Cricket Chatbot
#         *Real-time match information from ESPN Cricinfo*
#         """)
        
#         with gr.Row():
#             with gr.Column(scale=2):
#                 chat_interface = gr.Chatbot(height=500)
#             with gr.Column(scale=1):
#                 update_status = gr.Textbox(
#                     label="Last Update",
#                     value="No data yet",
#                     interactive=False
#                 )
#                 gr.Examples(
#                     examples=[
#                         "Who is playing right now?",
#                         "What's the latest score?",
#                         "Which matches are happening today?",
#                         "Give me a summary of current matches"
#                     ],
#                     inputs=chat_interface
#                 )
        
#         with gr.Row():
#             user_query = gr.Textbox(
#                 placeholder="Ask about live matches...",
#                 label="Your Question"
#             )
#             submit_btn = gr.Button("Ask", variant="primary")
        
#         clear_btn = gr.Button("Clear Chat")
        
#         def respond(message, chat_history):
#             response = chatbot.generate_response(message)
#             update_time = (
#                 chatbot.last_update.strftime("%H:%M:%S") 
#                 if chatbot.last_update 
#                 else "N/A"
#             )
#             chat_history.append((message, response))
#             return "", chat_history, update_time
        
#         user_query.submit(respond, [user_query, chat_interface], [user_query, chat_interface, update_status])
#         submit_btn.click(respond, [user_query, chat_interface], [user_query, chat_interface, update_status])
#         clear_btn.click(lambda: ([], "No data yet"), outputs=[chat_interface, update_status])
    
#     return demo

# if __name__ == "__main__":
#     interface = create_chat_interface()
#     interface.launch(
#         server_name="0.0.0.0",
#         server_port=7860,
#         share=False
#     )




# import gradio as gr
# from scraper import Scraper
# import re
# import json
# import os
# from typing import Dict, List, Union

# def extract_player_name(query: str) -> Union[str, None]:
#     """Extracts player name from query using NLP patterns."""
#     patterns = [
#         r"statistics of (.+)",
#         r"stats of (.+)",
#         r"how is (.+) performing",
#         r"details about (.+)",
#         r"tell me about (.+)",
#         r"show (.+) stats"
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, query, re.IGNORECASE)
#         if match:
#             return match.group(1).strip()
#     return None

# def read_player_stats() -> List[Dict]:
#     """Reads the stats from the JSON file created by scraper."""
#     try:
#         with open("player_stats.json", "r") as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# def format_stats_response(stats: List[Dict]) -> str:
#     """Formats the scraped stats into a readable string."""
#     if not stats:
#         return "No statistics found for this player."
    
#     response = "**Player Statistics:**\n\n"
    
#     for format_data in stats:
#         if "Format" in format_data:
#             response += f"🏏 **{format_data['Format']}**\n"
#             for key, value in format_data.items():
#                 if key != "Format":
#                     response += f"- {key}: {value}\n"
#             response += "\n"
    
#     return response

# def handle_player_query(query: str) -> str:
#     """Main function to process player stats requests."""
#     player_name = extract_player_name(query)
#     if not player_name:
#         return "Please specify a player name. Example: 'Give me statistics of Virat Kohli'"
    
#     # Run the scraper (it will save data to player_stats.json)
#     scraper = Scraper(player_name)
#     scraper.start()  # This creates/overwrites player_stats.json
    
#     # Read the freshly scraped data
#     stats = read_player_stats()
    
#     if not stats:
#         return f"Could not retrieve statistics for {player_name}. The player may not exist or there was a scraping error."
    
#     return format_stats_response(stats)

# # Gradio Interface
# iface = gr.Interface(
#     fn=handle_player_query,
#     inputs=gr.Textbox(
#         label="Ask about any cricket player",
#         placeholder="E.g., 'Give me statistics of Virat Kohli'"
#     ),
#     outputs=gr.Textbox(label="Player Statistics", lines=20),
#     title="🏏 Cricket Player Stats Bot",
#     examples=[
#         ["Show Virat Kohli stats"],
#         ["How is Babar Azam performing?"],
#         ["Statistics of Jasprit Bumrah"]
#     ],
#     allow_flagging="never"
# )

# if __name__ == "__main__":
#     iface.launch()





# import gradio as gr
# from scraper import Scraper
# import re
# import json
# import os
# import time
# from typing import Optional

# class CricketChatbot:
#     def __init__(self):
#         self.last_player = None
#         self.last_stats = None

#     def extract_player_name(self, query: str) -> Optional[str]:
#         """Improved player name extraction with more patterns"""
#         patterns = [
#             r"(?:stats|statistics|details|info|information) (?:of|for|about) (.+)",
#             r"how (?:is|are) (.+) performing",
#             r"show (?:me )?(?:the )?(?:stats|statistics) (?:of|for) (.+)",
#             r"(.+) (?:stats|statistics|record|performance)"
#         ]
        
#         query = query.lower().strip()
#         for pattern in patterns:
#             match = re.search(pattern, query, re.IGNORECASE)
#             if match:
#                 name = match.group(1).strip()
#                 # Clean common trailing phrases
#                 name = re.sub(r"'s$| stats$| statistics$", "", name)
#                 return name.title()  # Proper capitalization
#         return None

#     def load_stats(self) -> Optional[dict]:
#         """Wait for and load the stats file with timeout"""
#         timeout = 10  # seconds
#         start_time = time.time()
        
#         while not os.path.exists("player_stats.json") and (time.time() - start_time) < timeout:
#             time.sleep(0.5)
            
#         if os.path.exists("player_stats.json"):
#             try:
#                 with open("player_stats.json", "r") as f:
#                     return json.load(f)
#             except (json.JSONDecodeError, IOError):
#                 pass
#         return None

#     def format_stats(self, stats: list) -> str:
#         """Better formatted output with error handling"""
#         if not stats or not isinstance(stats, list):
#             return "No valid statistics found for this player."
        
#         response = "**Player Statistics**\n\n"
#         format_names = {
#             "Tests": "🏏 Test Matches",
#             "ODIs": "🏏 ODI Matches",
#             "T20s": "⚡ T20 Internationals",
#             "Overall": "📊 Overall Career",
#             "IPL": "💰 IPL Statistics"
#         }
        
#         for format_data in stats:
#             if not isinstance(format_data, dict):
#                 continue
                
#             format_type = format_data.get("Format", "Unknown")
#             response += f"### {format_names.get(format_type, format_type)}\n"
            
#             for key, value in format_data.items():
#                 if key != "Format":
#                     response += f"- {key.replace('_', ' ').title()}: {value}\n"
#             response += "\n"
        
#         return response if len(response) > 20 else "Statistics found but in unexpected format."

#     def get_player_stats(self, query: str) -> str:
#         """Main function to handle queries"""
#         player_name = self.extract_player_name(query)
#         if not player_name:
#             return "Please ask about a player. Example: 'Show me Virat Kohli stats' or 'How is Babar Azam performing?'"
        
#         # Skip scraping if same player requested again
#         if player_name == self.last_player and self.last_stats:
#             return self.format_stats(self.last_stats)
        
#         # Run the scraper
#         try:
#             scraper = Scraper(player_name)
#             scraper.start()
            
#             # Load the results
#             stats = self.load_stats()
#             if stats is None:
#                 return f"Failed to retrieve data for {player_name}. The player may not exist or there was a website error."
            
#             self.last_player = player_name
#             self.last_stats = stats
#             return self.format_stats(stats)
            
#         except Exception as e:
#             return f"Error processing your request: {str(e)}"

# # Create interface
# chatbot = CricketChatbot()
# iface = gr.Interface(
#     fn=chatbot.get_player_stats,
#     inputs=gr.Textbox(
#         label="Ask about any cricket player",
#         placeholder="E.g., 'Virat Kohli stats' or 'How is Steve Smith performing?'"
#     ),
#     outputs=gr.Markdown(label="Player Statistics"),
#     title="🏏 Cricket Stats Bot",
#     examples=[
#         ["Show me Rohit Sharma ODI stats"],
#         ["How is Kane Williamson performing in Tests?"],
#         ["Pat Cummins bowling statistics"],
#         ["Rashid Khan T20 records"]
#     ],
#     allow_flagging="never",
#     theme="soft"
# )

# if __name__ == "__main__":
#     iface.launch(server_port=7860, share=False)




import gradio as gr
from scraper import Scraper
import re
import json
import os
import time
from typing import Optional
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class CricketChatbot:
    def __init__(self):
        self.last_player = None
        self.last_stats = None
        # Configure ChromeDriver path automatically
        self.chromedriver_path = ChromeDriverManager().install()

    def extract_player_name(self, query: str) -> Optional[str]:
        """Extract player name from query"""
        patterns = [
            r"(?:stats|statistics|details) (?:of|for|about) (.+)",
            r"how is (.+) performing",
            r"show (?:me )?(?:the )?stats (?:of|for) (.+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip().title()
        return None

    def load_stats(self) -> Optional[dict]:
        """Wait for stats file to be created"""
        timeout = 10
        start_time = time.time()
        while not os.path.exists("player_stats.json") and (time.time() - start_time) < timeout:
            time.sleep(0.5)
        if os.path.exists("player_stats.json"):
            try:
                with open("player_stats.json", "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return None

    def format_stats(self, stats: list) -> str:
        """Format the stats for display"""
        if not stats:
            return "No statistics found for this player."
        
        response = "**Player Statistics**\n\n"
        for format_data in stats:
            if "Format" in format_data:
                response += f"### {format_data['Format']}\n"
                for key, value in format_data.items():
                    if key != "Format":
                        response += f"- {key}: {value}\n"
                response += "\n"
        return response

    def get_player_stats(self, query: str) -> str:
        """Main function to handle queries"""
        player_name = self.extract_player_name(query)
        if not player_name:
            return "Please ask about a player. Example: 'Show me Virat Kohli stats'"
        
        try:
            # Pass the chromedriver path to Scraper
            scraper = Scraper(player_name)
            scraper.start()  # This will use the automatically managed ChromeDriver
            
            stats = self.load_stats()
            if stats is None:
                return f"Could not retrieve data for {player_name}"
            
            return self.format_stats(stats)
            
        except Exception as e:
            return f"Error: {str(e)}. Please ensure Chrome is installed."

# Create and launch interface
chatbot = CricketChatbot()
iface = gr.Interface(
    fn=chatbot.get_player_stats,
    inputs=gr.Textbox(label="Ask about a player"),
    outputs=gr.Markdown(),
    examples=[
        ["Show me Virat Kohli stats"],
        ["How is Babar Azam performing?"]
    ]
)

if __name__ == "__main__":
    iface.launch()