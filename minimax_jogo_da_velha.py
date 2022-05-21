class game:
    def __init__(self):
        self.board = ["-", "-", "-", 
                      "-", "-", "-",
                      "-", "-", "-"]
    
    def print(self):
        for i in range (9):
            print("|" + self.board[i],end='')
            if(i == 2 or i == 5 or i == 8):
                print("|")
        print()

    def valid_play(self, move):
        if(self.board[move] == '-'):
            return True
        return False

    def valid_input(self):
        while(True):
            move = int(input("Escolha a posição entre 1 e 9: "))
            if(self.valid_play(move - 1)):
                self.board[move - 1] = "X"
                break
            else:
                print("Jogada inválida!\n")

    def min_max(self, is_max):
        victory = self.win(self.board)

        if(victory != -2):
            return victory

        if(is_max):
            best = -9999

            for i in range(9):
                if(self.board[i] == '-'):
                    self.board[i] = 'O'

                    best = max(best, self.min_max(False))

                    self.board[i] = '-'
            return best
        
        else:
            best = 9999

            for i in range(9):
                if(self.board[i] == '-'):
                    self.board[i] = 'X'

                    best = min(best, self.min_max(True))

                    self.board[i] = '-'
            return best

    def best_play(self):
        best = -9999
        pos = -1

        for i in range(9):
            if(self.board[i] == '-'):
                self.board[i] = 'O'

                mm_value = self.min_max(False)

                self.board[i] = '-'

                if(mm_value > best):
                    best = mm_value
                    pos = i
        return pos

    def play(self):
        while(True):
            self.print()

            self.valid_input()

            if(self.win(self.board) == 1):
                print("\nHumano Venceu!")
                self.print()
                break

            ia_play = self.best_play()
            self.board[ia_play] = 'O'

            if(self.win(self.board) == 2):
                print("\nIA Venceu!")
                self.print()
                break

            if(self.win(self.board) == 0):
                print("\nEmpate!")
                self.print()
                break

    def win(self, board):

        if((board[0] == 'X' and board[1] == 'X' and board[2] == 'X') or
           (board[3] == 'X' and board[4] == 'X' and board[5] == 'X') or
           (board[6] == 'X' and board[7] == 'X' and board[8] == 'X') or
           (board[0] == 'X' and board[3] == 'X' and board[6] == 'X') or
           (board[1] == 'X' and board[4] == 'X' and board[7] == 'X') or
           (board[2] == 'X' and board[5] == 'X' and board[8] == 'X') or
           (board[0] == 'X' and board[4] == 'X' and board[8] == 'X') or
           (board[2] == 'X' and board[4] == 'X' and board[6] == 'X')):
            return 1
    
        if((board[0] == 'O' and board[1] == 'O' and board[2] == 'O') or
           (board[3] == 'O' and board[4] == 'O' and board[5] == 'O') or
           (board[6] == 'O' and board[7] == 'O' and board[8] == 'O') or
           (board[0] == 'O' and board[3] == 'O' and board[6] == 'O') or
           (board[1] == 'O' and board[4] == 'O' and board[7] == 'O') or
           (board[2] == 'O' and board[5] == 'O' and board[8] == 'O') or
           (board[0] == 'O' and board[4] == 'O' and board[8] == 'O') or
           (board[2] == 'O' and board[4] == 'O' and board[6] == 'O')):
            return 2

        game = True
        for i in range(9):
            if(board[i] == '-'):
                game = False
        if(game):
            return 0

        return -2

def main():

    tic_tac_toe = game()
    tic_tac_toe.play()

if __name__ == "__main__":
    main()
