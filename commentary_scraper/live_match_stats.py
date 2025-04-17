import requests
from bs4 import BeautifulSoup


class LiveMatchStats:

    def __init__(self):
        self.url = "https://www.cricbuzz.com/cricket-match/live-scores"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.soup = None
    
    def get_Stats(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status() 
            self.soup = BeautifulSoup(response.text, 'lxml')

            # Find all tournament sections
            tournaments = self.soup.find_all('div', class_="cb-col cb-col-100 cb-plyr-tbody cb-rank-hdr cb-lv-main")

            if not tournaments:
                print("No matches found - the page structure may have changed")
            else:
                print("Recent Cricket Matches:")
                match_counter = 1

                for tournament in tournaments:
                    try:
                        # Get tournament name
                        tour_name = tournament.find('h2', class_="cb-lv-grn-strip").get_text(strip=True) if tournament.find('h2', class_="cb-lv-grn-strip") else "N/A"
                        print(f"\nTournament: {tour_name}")
                        print("-" * 50)

                        # Find all matches in this tournament
                        matches = tournament.find_all('div', class_="cb-mtch-lst cb-col cb-col-100 cb-tms-itm")

                        for match in matches:
                            try:
                                # Get teams
                                teams = match.find('h3', class_="cb-lv-scr-mtch-hdr").get_text(" ", strip=True) if match.find('h3', class_="cb-lv-scr-mtch-hdr") else "N/A"

                                # Get score
                                score = match.find('div', class_="cb-scr-wll-chvrn").get_text(" ", strip=True) if match.find('div', class_="cb-scr-wll-chvrn") else "N/A"

                                # Get match status (like "Live", "Completed", etc.)
                                status = match.find('div', class_="cb-text-live").get_text(strip=True) if match.find('div', class_="cb-text-live") else (
                                    match.find('div', class_="cb-text-complete").get_text(strip=True) if match.find('div', class_="cb-text-complete") else "N/A"
                                )
                                href = match.find('a', class_='cb-lv-scrs-well')['href']
                                print(f"{match_counter}. {teams}")
                                print(f"   Score: {score}")
                                print(f"   Status: {status}")
                                print(f"   Link: {href}")
                                print("-" * 40)
                                match_counter += 1

                            except Exception as e:
                                print(f"Error processing match: {str(e)}")
                                continue

                    except Exception as e:
                        print(f"Error processing tournament: {str(e)}")
                        continue

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    


        

        
        