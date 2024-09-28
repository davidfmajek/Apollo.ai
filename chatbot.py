import openai
import random

# Simulate feedback from the user
def get_user_feedback(song_recommendation):
    feedback = input(f"Do you like the recommendation: '{song_recommendation}'? (yes/no): ")
    return 1 if feedback.lower() == 'yes' else -1

# Function to call OpenAI to get song recommendations
def recommend_songs(song_title):
    # Query OpenAI to generate song recommendations based on the input song
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a music expert helping to recommend songs by genre based on a given song title."
            },
            {
                "role": "user",
                "content": f"Recommend some songs similar to {song_title}, including their artist."
            }
        ]
    )

    recommendations = response['choices'][0]['message']['content']
    return recommendations.strip()

# RL Agent class for song recommendations
class RLAgent:
    def __init__(self, song_history):
        self.song_history = song_history  # Stores the history of songs recommended and feedback
        self.q_table = {}  # Q-table to store expected rewards for song recommendations
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0  # Start with full exploration
        self.exploration_decay = 0.99  # Gradually reduce exploration

    def choose_song(self, current_song):
        if random.uniform(0, 1) < self.exploration_rate:
            # Explore: Get a new recommendation from OpenAI
            return recommend_songs(current_song)
        else:
            # Exploit: Choose the song with the highest reward in the Q-table
            return self.get_best_song(current_song)

    def get_best_song(self, current_song):
        # Get the song with the highest reward based on past feedback
        if current_song in self.q_table:
            return max(self.q_table[current_song], key=self.q_table[current_song].get)
        return recommend_songs(current_song)  # Fall back to exploring if no data available

    def learn(self, current_song, recommended_song, reward):
        # Update Q-table with new reward using Q-learning formula
        if current_song not in self.q_table:
            self.q_table[current_song] = {}

        if recommended_song not in self.q_table[current_song]:
            self.q_table[current_song][recommended_song] = 0  # Initialize if first time

        # Q-learning update rule
        best_future_reward = max(self.q_table[current_song].values(), default=0)
        self.q_table[current_song][recommended_song] += self.learning_rate * (reward + self.discount_factor * best_future_reward - self.q_table[current_song][recommended_song])

        # Decay exploration rate to favor exploitation over time
        self.exploration_rate *= self.exploration_decay

# Example usage
if __name__ == "__main__":
    openai.api_key = "your-api-key-here"  # Replace with your OpenAI API key

    # RL agent with empty song history
    agent = RLAgent(song_history={})

    # Start with a song title
    current_song = input("Enter a song title to start: ")

    for episode in range(10):  # Simulate 10 interactions with the user
        print(f"\n--- Interaction {episode+1} ---")
        
        # Agent chooses a song to recommend
        recommended_song = agent.choose_song(current_song)
        print(f"Recommended Song: {recommended_song}")

        # Get feedback from the user
        reward = get_user_feedback(recommended_song)

        # Agent learns from the feedback
        agent.learn(current_song, recommended_song, reward)

        # Update current song (could be the same, or user may input a new one)
        current_song = input("\nEnter a new song title to continue or press Enter to use the same: ") or current_song

    print("\nQ-table after training:")
    print(agent.q_table)
