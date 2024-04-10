from game import Game

def main():
    game = Game()

    while not game.game_over:
        # Ask for user input
        print("score: ", game.score) 
        user_input = input("Enter command (z/q/s/d): ")
        # Handle user input
        if user_input == 'z':
            game.top()
        elif user_input == 'q':
            game.left()
        elif user_input == 's':
            game.bottom()
        elif user_input == 'd':
            game.right()
        elif user_input.lower() == 'exit':
            game.game_over = True
        else:
            print("Invalid command")

        

    if game.won:
        print("YOU WON")
    else:
        print("GAME OVER LOSER!!")

if __name__ == "__main__":
    main()