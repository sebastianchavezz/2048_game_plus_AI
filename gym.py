from game import Game
from agent import Agent, Move


def update_game(game: Game, action: Move):
    if action == Move.TOP:
        game.top()
    elif action == Move.LEFT:
        game.left()
    elif action == Move.BOT:
        game.bottom()
    elif action == Move.RIGHT:
        game.right()


def train():
    # Parameters
    eps = 0.5
    eps_decay = 0.99
    min_eps = 0.01
    learning_rate = 0.1
    discount_rate = 0.9
    num_episodes = 1000

    max_tile = 0
    game = Game()
    agent = Agent(game.board, eps, eps_decay, min_eps)

    for episode in range(1, num_episodes + 1):
        # Initialize the state
        current_state = agent.get_state()

        # Initialize episode-specific variables
        total_reward = 0
        num_moves = 0

        # Run the episode until the game is over
        while not game.game_over:
            # Choose action based on epsilon-greedy strategy
            action = agent.get_action(current_state)

            # Update the game state based on the chosen action
            update_game(game, action)

            # Get the reward for the current state-action pair
            reward = agent.get_reward(game.board, game.score, game.game_over)

            # Update Q-values based on the observed reward and the next state
            next_state = agent.get_state()
            agent.updateQValue(current_state, action, reward, next_state, learning_rate, discount_rate)

            # Update episode-specific variables
            total_reward += reward
            num_moves += 1

            # Update the current state for the next iteration
            current_state = next_state

        # Decay epsilon after each episode
        eps = max(min_eps, eps * eps_decay)
        max_tile = max(max_tile, max(map(max, game.board)))
        # Log episode results
        print(f"Episode {episode}: Total Reward = {total_reward}, Num Moves = {num_moves}, Max Tile = {max(map(max, game.board))}")
        
        # Reset the game for the next episode
        game.reset()

        #update epsilon 
        agent.update_epsilon()

        print("Before reset: ",agent.big_scores_counters)
        #reset the agenttablemax_tile
        agent.reset(game.board)
        print("after reset: ",agent.big_scores_counters)
        

    # Save the learned Q-table after training
    agent.save_q_table("q_table.pkl")
    print(f"Max tile: {max_tile}")

if __name__ == "__main__":
    train()
