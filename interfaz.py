import time # Agregar pequeñas pausas en la ejecución del programa
import tkinter as tk # Importamos biblioteca tkinter
from tkinter import font # Manipulacion de fuentes
from main import minimax_mancala  # Importa la función minimax_mancala del main


# Clase principal que representa la interfaz del juego de Mancala.
class MancalaTkinterUI(tk.Tk):
    def __init__(
        self,
        reference_size: int = 10,
    ):
        super().__init__()

        # Inicialización de variables y configuración de la interfaz.
        self.reference_size = reference_size
        self.jugador = "--"
        self.ai = "--"

        # Representación del tablero de Mancala.
        self.board = {
            "top": [4, 4, 4, 4, 4, 4],
            "bottom": [4, 4, 4, 4, 4, 4],
            "top_score": 0,
            "bottom_score": 0,
        }

        # Configuración de etiquetas de la interfaz.
        self.etiqueta_jugador_1 = "{jugador}\n{points:0>2}\n"
        self.etiqueta_jugador_2 = "\n{points:0>2}\n{jugador}"
        self.etiqueta_turno = "--"
        self.etiqueta_de_valor_de_oportunidad = "--"
        self.etiqueta_piezas_retenidas_num = "0"
        self.IA_dificultad = 1

        # Mapeo de confianza en la victoria basado en la puntuación.
        self.confianza_de_victoria = {
            -6: "Eres muy pro..",
            -1: "Aun tengo esperanzas",
            3: "Lo pones dificil",
            6: "¡Mejor no juegues!",
            100: "¡Ya fuiste!",
        }

        # Configuración de la ventana principal.
        self.title("Juego : Mancala")
        self.font_large = font.Font(size=self.reference_size * 2)
        self.font_med = font.Font(size=self.reference_size)
        self.font_small = font.Font(size=self.reference_size // 2)

        # Creación de marcos en la interfaz.

        #Titulo
        self.frame_titulo = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            background="#3176E8",
            relief=tk.RAISED,
        )

        #Titulo1
        self.frame_titulo1 = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            background="#3176E8",
            relief=tk.RAISED,
        )

        #Titulo2
        self.frame_titulo2 = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            background="#3176E8",
            relief=tk.RAISED,
        )

        #Superior
        self.frame_seleccion_botones = tk.Frame(
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            background="#3176E8",
            relief=tk.RAISED,
        )
        #Medio
        self.frame_estadisticas_juego = tk.Frame(
            background="#1ABBD9",
            master=self,
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            
            relief=tk.RAISED,
        )
        #Tablero
        self.frame_tablero_mancala = tk.Frame(
            master=self,
            padx=self.reference_size,
            pady=self.reference_size,
            background="#3176E8",
            relief=tk.RAISED,
        )




        # Colocación de marcos en la ventana principal.
        self.frame_titulo.grid(column=0, row=0, sticky="nsew")
        self.frame_seleccion_botones.grid(column=0, row=1, sticky="nsew")
        self.frame_titulo1.grid(column=0, row=2, sticky="nsew")
        self.frame_estadisticas_juego.grid(column=0, row=3, sticky="nsew")
        self.frame_titulo2.grid(column=0, row=4, sticky="nsew")
        self.frame_tablero_mancala.grid(column=0, row=5, sticky="nsew")

        #Fuentes
        font_underline = font.Font(family="Helvetica", size=18, underline=True)
        font_bold_italic = font.Font(family="Helvetica", size=12, weight="bold", slant="italic")
        font_bold_italic1 = font.Font(family="Helvetica", size=20, weight="bold", slant="italic")
        verdana_font = font.Font(family="Verdana", size=20, weight="bold")

        # Configuración de botones en el marco "frame_seleccion_botones".
        

        self.boton_jugador1 = tk.Button(
            master=self.frame_seleccion_botones,
            text="Jugador 1",
            background="#AD29CF",
            padx=self.reference_size // 2,  #Relleno horizontal
            pady=self.reference_size // 2,  #Relleno vertical
            font=font_bold_italic, # Fuente
            command=lambda: self.choose_jugador(jugador_type=1),
            borderwidth=10,  # ancho de borde
            relief=tk.RIDGE,  # redondeado
        )

        self.boton_jugador2 = tk.Button(
            master=self.frame_seleccion_botones,
            text="Jugador 2",
            background="#E3830B",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_bold_italic,
            command=lambda: self.choose_jugador(jugador_type=2),
            borderwidth=10,  # ancho de borde
            relief=tk.RIDGE,  # redondeado
        )

        self.boton_salir = tk.Button(
            master=self.frame_seleccion_botones,
            text="Salir",
            background="#1FD180",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_bold_italic,
            borderwidth=10,  # ancho de borde
            relief=tk.RIDGE,  # redondeado
            command=lambda: quit(),
        )

        self.boton_titulo = tk.Label(
            master=self.frame_titulo,
            text="Mancala",
            background="#1FD180",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_underline,
            

        )

        self.boton_titulo1 = tk.Label(
            master=self.frame_titulo1,
            text="Informacion del Juego",
            background="#1FD180",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_bold_italic,

        )

        self.boton_titulo2 = tk.Label(
            master=self.frame_titulo2,
            text="Ajuste de Dificultad de la IA",
            background="#1FD180",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_bold_italic,

        )

        # Colocación de titulo
        
        self.frame_titulo.grid_rowconfigure(0, weight=1)
        self.frame_titulo.grid_columnconfigure(0, weight=1)
        self.boton_titulo.grid(column=0, row=0, sticky="nsew")

        # Colocación de titulo1
        
        self.frame_titulo1.grid_rowconfigure(0, weight=1)
        self.frame_titulo1.grid_columnconfigure(0, weight=1)
        self.boton_titulo1.grid(column=0, row=2, sticky="nsew")

        # Colocación de titulo2
        
        self.frame_titulo2.grid_rowconfigure(0, weight=1)
        self.frame_titulo2.grid_columnconfigure(0, weight=1)
        self.boton_titulo2.grid(column=0, row=2, sticky="nsew")



        # Configuración de la fila 0 para que se expanda
        self.frame_seleccion_botones.grid_rowconfigure(0, weight=1)

        # Configuración de las columnas para centrar los botones
        self.frame_seleccion_botones.grid_columnconfigure(0, weight=1)
        self.frame_seleccion_botones.grid_columnconfigure(1, weight=1)
        self.frame_seleccion_botones.grid_columnconfigure(2, weight=1)

        # Colocación de botones en la interfaz.
        self.boton_jugador1.grid(column=0, row=1, sticky="nsew")
        self.boton_jugador2.grid(column=1, row=1, sticky="nsew")
        self.boton_salir.grid(column=2, row=1, sticky="nse")

        



        # Configuración de etiquetas y controles en el marco "frame_estadisticas_juego".

        self.etiqueta_turno_actual = tk.Label(
            master=self.frame_estadisticas_juego,
            background="#1ABBD9",
            text="Turno actual",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_bold_italic,
        )
        self.etiqueta_oportunidad_ganar = tk.Label(
            master=self.frame_estadisticas_juego,
            text="Predicción de Triunfo de la IA",
            background="#1ABBD9",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_bold_italic,
        )
        self.etiqueta_posecion_piezas = tk.Label(
            master=self.frame_estadisticas_juego,
            background="#1ABBD9",
            text="Fichas en Posesión",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=font_bold_italic,
        )



        # Otras etiquetas y controles en el marco "frame_estadisticas_juego".
        self.etiqueta_valor_turno_actual = tk.Label(
            background="#1ABBD9",
            master=self.frame_estadisticas_juego,
            text="--",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.etiqueta_valor_oportunidad_ganar = tk.Label(
            background="#1ABBD9",
            master=self.frame_estadisticas_juego,
            text="--",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.etiqueta_valor_posecion_piezas = tk.Label(
            background="#1ABBD9",
            master=self.frame_estadisticas_juego,
            text="0",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=self.font_med,
        )
        self.escala_dificultad = tk.Scale(
            background="#A364D6",
            master=self.frame_titulo2,
            orient="horizontal",
            from_=1,
            to=5,
            tickinterval=1,
            font=self.font_med,
            command=self.adjust_IA_dificultad,
        )

        # Separadores ":" entre etiquetas y valores.
        self.div_etiquetas = []
        for index in range(3):
            colon_divider_label = tk.Label(
                master=self.frame_estadisticas_juego,
                text=":",
                background="#1ABBD9",
                padx=self.reference_size // 2,
                pady=self.reference_size // 2,
                font=self.font_med,
            )
            colon_divider_label.grid(column=1, row=0 + index)
            self.div_etiquetas.append(colon_divider_label)

        # Colocación de etiquetas y controles en el marco "frame_estadisticas_juego".
        
        self.etiqueta_turno_actual.grid(column=0, row=0, sticky="nsw")
        self.etiqueta_oportunidad_ganar.grid(column=0, row=1, sticky="nsw")
        self.etiqueta_posecion_piezas.grid(column=0, row=2, sticky="nsw")

        self.etiqueta_valor_turno_actual.grid(column=2, row=0, sticky="nsw")
        self.etiqueta_valor_oportunidad_ganar.grid(column=2, row=1, sticky="nsw")
        self.etiqueta_valor_posecion_piezas.grid(column=2, row=2, sticky="nsw")

        #self.etiqueta_dificultad.grid(column=0, row=3, sticky="nsw")
        self.escala_dificultad.grid(column=0, row=4, columnspan=3, sticky="nsew")

        # Configuración de la representación visual del tablero de Mancala en "frame_tablero_mancala".
        self.etiqueta_jugador1_base = tk.Label(
            master=self.frame_tablero_mancala,
            text="J:1\n00\n",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=verdana_font,
            background="#AD29CF",
            width=self.reference_size // 4,
        )
        self.etiqueta_jugador2_base = tk.Label(
            master=self.frame_tablero_mancala,
            text="\n00\nJ:2",
            padx=self.reference_size // 2,
            pady=self.reference_size // 2,
            font=verdana_font,
            background="#E3830B",
            width=self.reference_size // 4,
        )
        #Tablero mancala
        #Almacena objetos de boton hoyos
        self.mancala_button_list = []
        for row in range(2):
            for column in range(6):

                def choose_move_closure(location: str, tile: int):
                    return lambda: self.choose_move(location=location, tile=tile)
                #Creacion de cada hoyo
                mancala_button = tk.Button(
                    master=self.frame_tablero_mancala,
                    text="4",
                    padx=self.reference_size // 2,
                    pady=self.reference_size // 2,
                    font=verdana_font,
                    background="#1AD9CD",
                    #Funcion cuando se hace click
                    command=choose_move_closure(
                        location="top" if row == 0 else "bottom",
                        tile=5 - column if row == 0 else column,
                    ),
                    width=self.reference_size // 8,
                )

                mancala_button.grid(column=1 + column, row=row, sticky="nsew")

                self.mancala_button_list.append(mancala_button)

        self.etiqueta_jugador1_base.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.etiqueta_jugador2_base.grid(column=7, row=0, rowspan=2, sticky="nsew")

    def sync_backend_front_end(self):
        """Actualiza la interfaz con los valores actuales del juego."""
        self.etiqueta_valor_turno_actual.config(text=self.etiqueta_turno)
        self.etiqueta_valor_oportunidad_ganar.config(text=self.etiqueta_de_valor_de_oportunidad)
        self.etiqueta_valor_posecion_piezas.config(text=self.etiqueta_piezas_retenidas_num)
        #Actualiza el puntaje J!
        self.etiqueta_jugador1_base.config(
            text=self.etiqueta_jugador_1.format(
                jugador="Tu" if self.jugador == "top" else "AI",
                points=self.board["top_score"],
            )
        )
        #Actualiza puntoaje J2
        self.etiqueta_jugador2_base.config(
            text=self.etiqueta_jugador_2.format(
                jugador="Tu" if self.jugador == "bottom" else "AI",
                points=self.board["bottom_score"],
            )
        )
        #Actualiza texto de los hoyos
        for index, tile in enumerate(reversed(self.board["top"])):
            self.mancala_button_list[index].config(text=tile)

        for index, tile in enumerate(self.board["bottom"]):
            self.mancala_button_list[index + 6].config(text=tile)

    def adjust_IA_dificultad(self, value: int):
        """Permite ajustar la dificultad de la IA."""
        self.IA_dificultad = value

    def choose_jugador(self, jugador_type: int):
        """Permite al jugador elegir su rol en el juego."""
        if jugador_type == 1:
            self.jugador = "top"
            self.ai = "bottom"
            self.etiqueta_turno = "Tu"

        if jugador_type == 2:
            self.jugador = "bottom"
            self.ai = "top"
            self.etiqueta_turno = "AI"

        # Reinicia el tablero y sincroniza la interfaz.
        self.board = {
            "top": [4, 4, 4, 4, 4, 4],
            "bottom": [4, 4, 4, 4, 4, 4],
            "top_score": 0,
            "bottom_score": 0,
        }

        self.sync_backend_front_end()

        # Si el jugador va segundo, la IA hace su primer movimiento.
        if jugador_type == 2:
            best_score, move = minimax_mancala( self.board, self.ai, self.ai, int(self.IA_dificultad))
            self.move_pieces(self.ai, move)

    def choose_move(self, location: str, tile: int):
        """Permite al jugador seleccionar un movimiento."""
        #Verifica si es turno del juegador
        #Verifica si escogo mis fichas
        #Verifica si hay fichas
        if (
            not ("tu" in self.etiqueta_turno.lower())
            or (self.jugador != location)
            or (self.board[location][tile] == 0)
        ):
            return

        self.move_pieces(location, tile)

    def move_pieces(self, turn: str, tile: int):
        """Realiza el movimiento de las piezas en el juego."""
        pieces = self.board[turn][tile]
        self.board[turn][tile] = 0
        location = turn
        go_again = False

        # 2. Movimiento de las piezas.
        while pieces > 0:
            self.etiqueta_piezas_retenidas_num = pieces
            #Actualiza la interfaz 
            self.sync_backend_front_end()
            self.update()
            time.sleep(0.2)

            go_again = False
            #Repartimos en los hoyos
            pieces -= 1
            #Indice del nuevo hoyo
            tile += 1
            #Coloca piesas repartidas
            if tile < len(self.board[location]):
                self.board[location][tile] += 1
                continue

            # 3. Si la última pieza cae en tu propia Mancala, toma otro turno.
            # Si cae en la Mancala del oponente, omítela y continúa al siguiente hoyo.
            if location == turn:
                self.board[f"{turn}_score"] += 1
                go_again = True
            else:
                pieces += 1
            #Actualizacion de jugador
            location = "bottom" if location == "top" else "top"
            #Asegura que el siguiente ciclo de bucle empiese desde el primer
            #hoyo a quien le toque el turno
            tile = -1

        #Actualiza interfaz
        self.etiqueta_piezas_retenidas_num = 0
        self.sync_backend_front_end()
        time.sleep(0.2)

        # 5. Captura de piezas en el lado opuesto si corresponde.
        inverse_location = "bottom" if location == "top" else "top"
        #
        if (
            (location == turn)
            and (self.board[location][tile] == 1)
            and (
                self.board[inverse_location][
                    len(self.board[inverse_location]) - 1 - tile
                ]
                != 0
            )
        ):
            self.board[f"{turn}_score"] += (
                1
                + self.board[inverse_location][
                    len(self.board[inverse_location]) - 1 - tile
                ]
            )
            self.board[location][tile] = 0
            self.board[inverse_location][
                len(self.board[inverse_location]) - 1 - tile
            ] = 0

        # 7. El juego termina cuando todos los hoyos de un lado están vacíos.
        # 8. El jugador con piezas restantes en su lado las captura todas.
        if (not any(self.board["top"])) or (not any(self.board["bottom"])):
            self.board["top_score"] += sum(self.board["top"])
            self.board["bottom_score"] += sum(self.board["bottom"])

            self.board["top"] = [0] * len(self.board["top"])
            self.board["bottom"] = [0] * len(self.board["bottom"])
            self.etiqueta_turno = "Fin del Juego"
            self.sync_backend_front_end()
            go_again = False
            return

        if not go_again:
            self.etiqueta_turno = (
                "Tu" if self.etiqueta_turno == "AI" else "AI"
            )
        #Actualiza la interfaz
        self.sync_backend_front_end()

        if self.etiqueta_turno == "AI":
            best_score, move = minimax_mancala(
                self.board, self.ai, self.ai, int(self.IA_dificultad)
            )
            for score, confidence in self.confianza_de_victoria.items():
                if score < best_score:
                    continue
                self.etiqueta_de_valor_de_oportunidad = confidence
                break
            self.move_pieces(self.ai, move)

    

# Función principal para iniciar la interfaz del juego.
def main():
    mancala = MancalaTkinterUI(14)
    mancala.mainloop()

if __name__ == "__main__":
    main()
