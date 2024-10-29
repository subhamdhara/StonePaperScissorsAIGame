import random

class RPSBot:
    def __init__(self):
        self.history = []        
        self.transition_matrix = {
            '1': {'1': 0, '2': 0, '3': 0},
            '2': {'1': 0, '2': 0, '3': 0},
            '3': {'1': 0, '2': 0, '3': 0}
        }

    def update_matrix(self, player_move):
        if len(self.history) > 0:
            last_move = self.history[-1]
            self.transition_matrix[last_move][player_move] += 1


    def predict_move(self):
        if len(self.history) < 2:
            return random.choice(['1', '2', '3'])
        last_move = self.history[-1]
        next_move_counts = self.transition_matrix[last_move]
        predicted_move = max(next_move_counts, key=next_move_counts.get)
        
        total = sum(next_move_counts.values())
        if total == 0:
            return random.choice(['1', '2', '3'])
        
        return {'1': '2', '2': '3', '3': '1'}[predicted_move]

    def play(self):
        bot_move = self.predict_move()
        return bot_move
    def update(self, player_move):
        self.update_matrix(player_move)
        self.history.append(player_move)

def main():
    bot = RPSBot()
    moves = ['1', '2', '3']
    
    while True:
        player_move = input("Your move: ").lower()
        if player_move == 'exit':
            print("Thanks for playing!")
            break
        if player_move not in moves:
            print("Invalid move. Please try again.")
            continue
        
        bot_move = bot.play()
        bot.update(player_move)
        print(f"Bot move: {bot_move}")
        
        if player_move == bot_move:
            print("It's a tie!")
        elif (player_move == '1' and bot_move == '3') or \
             (player_move == '2' and bot_move == '1') or \
             (player_move == '3' and bot_move == '2'):
            print("You win!")
        else:
            print("Bot wins!")

if __name__ == "__main__":
    main()
