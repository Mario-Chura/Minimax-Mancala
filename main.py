#En estas líneas, el código importa algunos módulos necesarios, incluido Tuple de 
#typing para trabajar con tipos de tupla y copy para realizar copias profundas de objetos
from typing import Tuple
import copy


#Funcion se encarga de imprimir el trablero en consola del juego
def print_board(board: dict, player_1: str = "P 1", player_2: str = "P 2") -> None:
    """A function to display the board

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
    """
    print(
        f"""
   {''.join(f'{(len(board["top"]) - num):3}' for num in range(len(board['top'])))}
+---+{'--+'*len(board['top'])}---+
|{player_1}|{'|'.join(f'{item:2}' for item in reversed(board['top']))}|   | <- PLAYER 1
|{board["top_score"]:3}+{'--+'*len(board['top'])}{board["bottom_score"]:3}|
|   |{'|'.join(f'{item:2}' for item in board['bottom'])}|{player_2}| PLAYER 2 ->
+---+{'--+'*len(board['bottom'])}---+
   {''.join(f'{(num+1):3}' for num in range(len(board['bottom'])))}
"""
    )
    return

#recibe el diccionario board el indice de la casilla a mover y el turno
#del jugador, devuelve un nuevo estado del tablero y un valor booleano 
#que indica si el jugador puede hacer otro movimiento
def move_piece(board: dict, tile: int, turn: str) -> Tuple[dict, bool]:
    """A function to preform the moves of the user

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        tile (int): the index of the list
        turn (str): 'top' or 'bottom'

    Returns:
        Tuple[dict, bool]:
            board (dict): Schema
            {
                "top"          : [4, 4, 4, 4, 4, 4],
                "bottom"       : [4, 4, 4, 4, 4, 4],
                "top_score"    : 0,
                "bottom_score" : 0
            }
            go_again (bool): indicats if the user is able ot make another turn
    """
    pieces = board[turn][tile]
    board[turn][tile] = 0
    location = turn
    go_again = False

    #Moviéndose en el sentido contrario a las agujas del reloj, el jugador 
    #deposita una de las piedras en cada bolsillo hasta que se agotan.
    while pieces > 0:
        go_again = False
        pieces -= 1
        tile += 1

        if tile < len(board[location]):
            board[location][tile] += 1
            continue

        #Si te topas con tu propia Mancala (tienda), deposita una pieza en ella.
        # Si te topas con el Mancala de tu oponente, sáltalo y continúa moviéndote al siguiente bolsillo.
        #Si la última pieza que sueltas está en tu propia Mancala, tomas otro turno.
        if location == turn:
            board[f"{turn}_score"] += 1
            go_again = True
        else:
            pieces += 1

        location = "bottom" if location == "top" else "top"
        tile = -1

    # Si la última pieza que sueltas está en un bolsillo vacío de tu costado,
    # capturas esa pieza y cualquier pieza en el bolsillo justo enfrente.
    # A MENOS QUE no haya nada directamente en el bolsillo al lado
    # Siempre coloca todas las piezas capturadas en tu Mancala (tienda).

    inverse_location = "bottom" if location == "top" else "top"
    if (
        (location == turn)
        and (board[location][tile] == 1)
        and (board[inverse_location][len(board[inverse_location]) - 1 - tile] != 0)
    ):
        board[f"{turn}_score"] += (
            1 + board[inverse_location][len(board[inverse_location]) - 1 - tile]
        )
        board[location][tile] = 0
        board[inverse_location][len(board[inverse_location]) - 1 - tile] = 0

    #El juego termina cuando los seis bolsillos de un lado del tablero de Mancala están vacíos.
    #El jugador que todavía tiene piezas en su lado del tablero cuando termina el juego captura todas esas piezas.

    if (not any(board["top"])) or (not any(board["bottom"])):
        board["top_score"] += sum(board["top"])
        board["bottom_score"] += sum(board["bottom"])

        board["top"] = [0] * len(board["top"])
        board["bottom"] = [0] * len(board["bottom"])

        go_again = False

    return board, go_again

#La función tiene como objetivo verificar si el movimiento en 
#el índice especificado (tile) es válido para el jugador cuyo 
#turno está representado por turn.
def is_viable_move(board: dict, tile: int, turn: str) -> bool:
    """A validation function to determin if a move is viable

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        tile (int): the index of the list
        turn (str): 'top' or 'bottom'

    Returns:
        bool: if the space is a valid space to choose
    """
    if tile >= len(board[turn]) or tile < 0:
        return False
    return bool(board[turn][tile])

#implementa el algoritmo minimax, Toma el estado actual dell tablero(`board`)
#el lado controlado por la inteligencia artificial (`ai_side`) el turno actual (turn)
# y la profundidad maxima para la bsuqueda. Devuelve una tupla con la puntuación y el
# el movimiento recomendado para el juego AIZ
def minimax_mancala(
    board: dict, ai_side: str, turn: str, depth: int
) -> Tuple[int, int]:
    """A function to calculate the minimax algorithm for a given board

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        ai_side (str): 'top' or 'bottom'
        turn (str): 'top' or 'bottom'
        depth (int): How deep that you want the AI to look ahead, *WARNING* larger depths require more CPU power

    Returns:
        Tuple[int, int]:
            score (int): the likely hood of the move being the best move
                - this is used in recursion for finding the best move
            move (int) : the recommended minimax move
                - this is used in decision making for executing the best move
    """
    AI = ai_side
    PLAYER = "bottom" if AI == "top" else "top"

    #inicialza la varible, Esta variable se utiliza para almacenar el mejor mov encontrado
    best_move = -1

    # Si el juego termina o se alcanza la profundidad máxima.
    # El delta de AI - PLAYER es lo que creo que dará el mejor resultado, 
    # ya que hará que el algoritmo se esfuerce por conseguir un gran número de victorias.
    if (not any(board["top"])) or (not any(board["bottom"])) or depth <= 0:
        return board[f"{AI}_score"] - board[f"{PLAYER}_score"], best_move

    # Encontrar el movimiento que le dará más puntos a la IA
    if AI == turn:
        #inicia coon un valor negativo, esto para realizar seguimiento de la
        #mejor puntuacion encontrada hasta ahora d ela busqueda
        best_score = float("-inf")

        #Se crea la lista con los moviminetos validos para el lado controaldo por la IA(AI)
        possible_moves = [
            move for move in range(len(board[AI])) if is_viable_move(board, move, AI)
        ]

        #Iteramos a través de los movimientos válidos.
        for move in possible_moves:
            #realizar una copia profunda para no sobrescribir movimientos accidentalmente haciendo referencia a la misma lista
            board_copy = copy.deepcopy(board)
            board_copy, go_again = move_piece(board_copy, move, turn)

            # mancala es uno de esos juegos en los que puedes realizar dos movimientos.
            if go_again:
                points, _ = minimax_mancala(board_copy, AI, AI, depth)
            else:
                points, _ = minimax_mancala(board_copy, AI, PLAYER, depth - 1)

            # La parte MAX de minimax. Encontrar la salida MAX para la IA
            if points > best_score:
                best_move = move
                best_score = points

    # Encontrar el movimiento que le dará menos puntos al JUGADOR
    elif PLAYER == turn:
        best_score = float("inf")
        possible_moves = [
            move
            for move in range(len(board[PLAYER]))
            if is_viable_move(board, move, PLAYER)
        ]

        for move in possible_moves:
           #realizar una copia profunda para no sobrescribir movimientos accidentalmente haciendo referencia a la misma lista
            board_copy = copy.deepcopy(board)
            board_copy, go_again = move_piece(board_copy, move, turn)

            if go_again:
                points, _ = minimax_mancala(board_copy, AI, PLAYER, depth)
            else:
                points, _ = minimax_mancala(board_copy, AI, AI, depth - 1)

            #La parte MIN de minimax. Encontrar la salida MIN para el JUGADOR
            if points < best_score:
                best_move = move
                best_score = points

    return best_score, best_move

#get_player_type es una función que solicita al usuario que elija 
#el tipo de jugador (jugador 1 o jugador 2) y devuelve una cadena que 
#representa el lado del jugador.
def get_player_type() -> str:
    """Una función para obtener el tipo de jugadores (los de arriba van primero)
    Returns:
        str: 'top' or 'bottom'
    """
    while True:

        player_input = input(
            "Please Enter Which Player You Want To Be :\n1. Player 1\n2. Player 2\n:"
        )
        #Aqui se verifica si ususario ingreso quit y llamara a quit()
        if "quit" in player_input.lower():
            quit()
        elif "1" in player_input:
            return "top"
        elif "2" in player_input:
            return "bottom"
        #Asegúrese de ingresar una de las dos opciones enumeradas
        print("Please Make Sure You Are Entering One Of The Two Options Listed.")

#get_player_move solicita al jugador que ingrese un movimiento válido 
#y devuelve el índice de la casilla elegida.
def get_player_move(board: dict, turn: str) -> int:
    #turn sera una cadena que indica de que lado del tablero es el turno
    #int es el mov valido del jugador
    """A function to get the players move

    Args:
        board (dict): Schema
        {
            "top"          : [4, 4, 4, 4, 4, 4],
            "bottom"       : [4, 4, 4, 4, 4, 4],
            "top_score"    : 0,
            "bottom_score" : 0
        }
        turn (str): 'top' or 'bottom'

    Returns:
        int: a valid move of the player
    """
    while True:
         #leera un dato ingresado por le usuario
        player_move = input("Please Select A Move.\n:")
        if "quit" in player_move.lower():
            quit()
        try:
            player_move = int(player_move) - 1
        except ValueError:
            # El bucle while continúa ejecutándose después de mostrar el mensaje de error.
            print("Please Make Sure To Enter A Valid Number.")
            continue

        if is_viable_move(board, player_move, turn):
            return player_move

        print("Sorry, That Is Not A Valid Move.")

#clear_screen se utiliza para borrar la pantalla y hacer que 
# la interfaz del juego sea más agradable visualmente.
def clear_screen() -> None:
    """
    *NOTE*
    some terminals may not work well with this code, please feel free to try out this instead...

    # IMPORT THIS AT THE TOP OF THE FILE
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    """
    #Limpiar la pantalla
    print("\033c", end="")

def main():
    # Default board, feel free to update if you know what you're doing and want a more interesting game.
    # The code should be set up mostly generic enough to handle different boards / piece amount
    board = {
        "top": [4, 4, 4, 4, 4, 4],
        "bottom": [4, 4, 4, 4, 4, 4],
        "top_score": 0,
        "bottom_score": 0,
    }

    # Mapping for how confident the algorithm is on winning the game (ballpark)
    total_pieces = sum(board["top"]) + sum(board["bottom"])
    winning_confidence_mapping = {
        -(total_pieces // 8): "Terrible",
        -(total_pieces // total_pieces): "Bad",
        total_pieces // 16: "Possible",
        total_pieces // 8: "Good",
        total_pieces + 1: "Certain",
    }

    # Displaying the board so the user know what they are selecting
    print_board(board)
    # Collecting what type the user is
    PLAYER = get_player_type()

    # Some final inits before starting the game
    PRINT_P1 = "YOU" if PLAYER == "top" else "CPU"
    PRINT_P2 = "CPU" if PLAYER == "top" else "YOU"
    AI = "bottom" if PLAYER == "top" else "top"
    MAX_DEPTH = 6

    # Top always goes first, feel free to change if you want to be a reble
    turn = "top"

    # visual for what the AI did
    ai_printed_moves = []

    # While the games not over!!!
    while not ((not any(board["top"])) or (not any(board["bottom"]))):
        # Players move
        if turn == PLAYER:
            # Getting the players move
            move = get_player_move(board, PLAYER)

            # Updating the board
            board, go_again = move_piece(board, move, PLAYER)

        # AI's move
        elif turn == AI:
            # Getting the AI's move with the Minimax function
            best_score, move = minimax_mancala(board, AI, turn, MAX_DEPTH)

            # Visual aid to show of confident the minimax algorithm is in winning
            winning_confidence = ""
            for score, confidence in winning_confidence_mapping.items():
                if score < best_score:
                    continue
                winning_confidence = confidence
                break
            ai_printed_moves.append(f"AI Moved : {move+1}\tChance of Winning : {winning_confidence}")

            # Updating the board
            board, go_again = move_piece(board, move, AI)

        # 4. If the last piece you drop is in your own Mancala, you take another turn.
        if not go_again:
            turn = "bottom" if turn == "top" else "top"

        # Shows the new baord
        clear_screen()
        if (turn == PLAYER) and ai_printed_moves:
            [print(move) for move in ai_printed_moves]
            ai_printed_moves = []
        print_board(board, PRINT_P1, PRINT_P2)

    # WIN / LOSS / DRAW
    if board[f"{PLAYER}_score"] > board[f"{AI}_score"]:
        print(
            f"Congrats! You won when the AI looks {MAX_DEPTH} moves ahead. For more of a challenge try increasing the MAX_DEPTH value."
        )
    elif board[f"{PLAYER}_score"] < board[f"{AI}_score"]:
        print(
            f"Nice try, but the machines win this time! For an easier game try decreasing the MAX_DEPTH value."
        )
    else:
        print(f"DRAW! Are you too looking {MAX_DEPTH} moves ahead?")

if __name__ == "__main__":
    main()