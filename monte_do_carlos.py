import random
import math

class Node:

    def __init__(self, parent, move, player, visits = 0, wins = 0):
        self.visits = visits
        self.wins = wins
        self.children = []
        self.player = player
        self.parent = parent
        self.move = move
        self.best_ucb = -1;
        self.best_move = -1;

    def add(self, node):
        self.children.append(node)

    def update(self, player):
        self.visits += 1
        if (self.player == player):
            self.wins += 1

    def ucb(self):
        c = 2
        if (self.visits == 0):
            return math.inf
        return self.wins / self.visits + math.sqrt( c * ( math.log( self.parent.visits ) / self.visits ) )



class Game:

    def __init__(self):
        self.matrix = [ [ 0 for _ in range(7) ] for _ in range(6) ]
        self.available_plays = [ 5 for _ in range(7) ]
        self.player = 1
        self.victory = 0
        self.placed_pieces = 0

    def play(self, col):
        self.matrix[self.available_plays[col]][col] = self.player
        self.placed_pieces += 1
        match_has_ended = self.verify(col)
        self.available_plays[col] -= 1
        self.player = -self.player
        return match_has_ended
    
    def verify(self, col):
        if (self.placed_pieces >= 42): return True
        row = self.available_plays[col]
        counter = [ 0 for _ in range(4) ]
        for i in range(-3, 4, 1):
            if (col + i >= 0 and col + i < 7):
                counter[0] = (counter[0] + 1) if (self.matrix[row][col + i] == self.player) else 0
            if (row + i >= 0 and row + i < 6):
                counter[1] = (counter[1] + 1) if (self.matrix[row + i][col] == self.player) else 0
            if (row + i >= 0 and row + i < 6 and col + i >= 0 and col + i < 7):
                counter[2] = (counter[2] + 1) if (self.matrix[row + i][col + i] == self.player) else 0
            if (row - i >= 0 and row - i < 6 and col + i >= 0 and col + i < 7):
                counter[3] = (counter[3] + 1) if (self.matrix[row - i][col + i] == self.player) else 0
            for j in range(4):
                if (counter[j] == 4):
                    self.victory = self.player
                    return True
        return False

    def copy(self, match):
        self.available_plays = match.available_plays[:]
        self.matrix = [row[:] for row in match.matrix]
        self.player = match.player
        self.victory = match.victory
        self.placed_pieces = match.placed_pieces

    def selection(self, root):
        node = root
        new_match = Game()
        new_match.copy(self)
        while(len(node.children) > 0):
            best = max(node.children, key = lambda child: child.ucb()) 
            new_match.play(best.move)
            node = best
        return (node, new_match)

    def expansion(self, parent):
        if (self.victory != 0 or self.placed_pieces >= 42):
            return parent
        for i in range(7):
            if (self.available_plays[i] >= 0):
                child = Node(parent, i, -parent.player)
                parent.add(child)
        return random.choice(parent.children)

    def simulation(self):
        moves = []
        for i in range(7):
            if (self.available_plays[i] >= 0):
                moves.append(i)
        
        while (True):
            move = random.choice(moves)
            if (self.play(move)):
                break
            if (self.available_plays[move] < 0):
                moves.remove(move)

    def backpropagation(self, child, victory):
        while(child != None):
            child.update(victory)
            child = child.parent

    def __str__(self):
        board = "\n "
        for i in range(6):
            for j in range(7):
                board += "X" if (self.matrix[i][j] == 1) else ("O" if (self.matrix[i][j] == -1) else "-")
            board += "\n "
        return board



def monte(cur_match, iterations):
    root = Node(None, -1, cur_match.player)
     
    for i in range(iterations):
        (leaf, match) = cur_match.selection(root)
        simulated_node = match.expansion(leaf)
        if (not (match.victory != 0 or match.placed_pieces >= 42) and not match.play(simulated_node.move)): 
            match.simulation() 
        match.backpropagation(simulated_node, -match.victory)

    best_node = None
    max_visits = -1
    for i in range(len(root.children)):
        #print(root.children[i].wins, root.children[i].visits)
        if (root.children[i].visits > max_visits):
            max_visits = root.children[i].visits
            best_node = root.children[i]
    
    return best_node.move



match = Game()

while (match.victory == 0 and match.placed_pieces < 42):
    print(match)
    if match.player == 1:
        move = monte(match,100000)
        match.play(move)
    else:
        #move = monte(match,10000)
        #match.play(move)
        match.play(int(input("Choose Column (" + ("X" if (match.player == 1) else "O") + "): "))-1)



print(match)

if (match.victory != 0):
    print("The victor is player " + ("1!" if (match.victory == 1) else "2!"))
else:
    print("It was a draw!")





# player == 1 verifica se o jogador é o jogador 1, e o player == -1 verifica se o jogador é o jogador 2.
# victory == 0 verifica se o jogo ainda não foi ganho, e victory == 1 verifica se o jogador 1 venceu, e victory == -1 verifica se o jogador 2 venceu.
# matrix == 0 verifica se a posição da matriz está livre, matrix == 1 verifica se a posição da matriz tem uma peça do jogador 1, e matrix == -1 verifica se a posição da matriz tem uma peça do jogador 2.
# o jogador 1 (1) joga primeiro, e o jogador 2 (-1) joga a seguir do jogador 1 (1).
# a classe tem uma variavel com a matriz do jogo, uma variavel com todas as jogadas possiveis (representadas pela coluna e depois em cada coluna o indice da linha na qual se pode jogar), uma variável que nos diz quem é a jogar e uma variável que nos diz quem venceu, se já houver vencedor.
# a classe tem um método de inicialização de todas as variáveis referidas, um método de fazer jogadas em função da coluna dada, que depois usa as jogadas possíveis de modo a determinar onde a peça é posicionada, e também usa a variável que determina quem é a jogar para que a alteração da matriz possa ser feita corretamente e implicitamente, e finalmente também tem um método que é executado implicitamente no método de fazer jogadas, e este método serve para que seja feita verificação de vitória a partir da posição em que a última peça que foi jogada calhou, e este método usa a variável que determina quem é a jogar para que a vitória possa ser atribuida corretamente.
# os métodos referidos foram refiridos na ordem: "__init__(self)", "play(self, col)", "verify(self, col)".
# o método play retorna False e faz print de uma mensagem de erro se a jogada que se tentou fazer não for válida (como descrito no "if statement") e retorna True se o método for executado sem problemas.
# o método verify retorn True se uma vitória tiver sido alcançada e False caso contrário.
# o método verify é composto por duas variáveis que nos dizem informação da posição da peça que está a ser jogada (linha e coluna) e de uma matriz com um contador em cada uma das 4 posições, onde a posição 0 é referente à linha em questão, a posição 1 à coluna, a posição 2 à diagonal principal e a posição 3 à diagonal secundária, e é desta forma que verificamos para todas as direções, usando um loop que viaja por ambos os sentidos verificando a contagem de peças do jogador atual, somando 1 ao contador se encontrar e definindo o contador a 0 caso contrário, assim assegurando que só verifica para 4 peças adjacentes, e é no fim de cada uma das 7 iterações que confirma se a contagem já chegou a 4 em alguma das direções, tendo a garantia de que não há um erro de "out of bound" graças ao uso das várias condições visíveis ao longo do loop.

