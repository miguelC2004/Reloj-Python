import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pygame

# Inicialización de nuestro mezclador de audio y configuración del archivo de alarma wav que queremos reproducir cuando suene la alarma
pygame.mixer.init(42050, -16, 2, 2048)
sonido_alarma = pygame.mixer.Sound("Alarma.wav")
# Configuración de nuestros valores globales iniciales
inicio_impreso = False
detener_impreso = True
hecho = False
terminado = False
detener_hizo_clic = False

class AplicacionAlarma(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Título de la ventana establecido en 'Reloj despertador'
        self.title("Reloj despertador")
        # Evitar que el usuario pueda redimensionar la ventana
        self.resizable(width=False, height=False)
        # Configuración de todas las listas desplegables
        self.hr = tk.IntVar(self)
        self.min = tk.IntVar(self)
        self.ampm = tk.StringVar(self)
        # Configuración de los valores iniciales de cada lista desplegable
        self.hr.set('12')
        self.min.set("00")
        self.ampm.set("AM")
        # Creación de la lista de valores de la cual seleccionaremos en nuestra lista desplegable
        horas = []
        minutos = []
        ampmlista = ["AM", "PM"]
        # Las horas van de 1 a 12
        for x in range(1, 13):
            horas.append(x)
        # Los minutos van de 0 a 59
        for y in range(0, 60):
            minutos.append("%02d" % (y,))
        # Colocando todas nuestras listas en sus respectivas listas desplegables
        self.menuhoras = tk.OptionMenu(self, self.hr, *horas)
        self.menuminutos = tk.OptionMenu(self, self.min, *minutos)
        self.menuAMPM = tk.OptionMenu(self, self.ampm, *ampmlista)
        # Colocando nuestras listas desplegables en la página junto con una etiqueta
        self.menuhoras.pack(side="left")
        self.etiqueta = tk.Label(text=":").pack(side="left")
        self.menuminutos.pack(side="left")
        self.menuAMPM.pack(side="left")
        # Configuración de los botones en el lado derecho de la ventana. El texto se refiere a lo que dice el botón
        # Command se refiere a qué función se ejecutará cuando se haga clic en él
        # State se refiere a si se puede hacer clic en él o no en el estado actual.
        self.boton_alarma = tk.Button(self, text="Configurar alarma", command=self.iniciar_reloj)
        # Deshabilité ambos de estos botones ya que solo deberían poder ser presionados cuando sea apropiado y la alarma esté en funcionamiento
        self.boton_cancelar = tk.Button(self, text="Cancelar alarma", command=self.detener_reloj, state="disabled")
        self.boton_detener_alarma = tk.Button(self, text="Detener alarma", command=self.detener_audio, state="disabled")
        # Empaquetando todos los botones en la página
        self.boton_alarma.pack()
        self.boton_cancelar.pack()
        self.boton_detener_alarma.pack()

    def iniciar_reloj(self):

        global hecho, inicio_impreso, detener_impreso, detener_hizo_clic
        # "hecho" se refiere a si se ha alcanzado la hora o si el usuario ha cancelado. Es decir: bucle terminado.
        if not hecho:
            # El botón de cancelar ahora está activo para que el usuario pueda decidir en cualquier momento cancelar la alarma
            self.boton_cancelar.config(state="active")
            # El botón de alarma ahora está deshabilitado ya que actualmente ya se ha configurado una alarma
            self.boton_alarma.config(state="disabled")
            # En la primera ejecución del bucle, informamos al usuario que se ha configurado una alarma para la hora deseada
            if not inicio_impreso:
                # Imprimir esta notificación para el usuario en la terminal
                print("Alarma configurada para {}:{}{}".format(self.hr.get(), "%02d" % (self.min.get()), self.ampm.get()))
                # Ahora configuramos esto como verdadero, ya que lo hemos impreso, para que no lo imprima nuevamente en cada bucle para esta alarma configurada
                inicio_impreso = True
                # "detener_impreso" se configura en falso para que una vez que el usuario cancele el temporizador, se imprima un mensaje (como veremos más adelante en el código)
                detener_impreso = False
            # Estas siguientes dos instrucciones if convierten nuestras horas de nuestra lista desplegable en un formato de 24 horas, para que podamos usarlo a través de DateTime
            if self.ampm.get() == "AM":
                if self.hr.get() in range(1, 12):
                    valor_hora = self.hr.get()
                else:
                    valor_hora = self.hr.get() - 12
            if self.ampm.get() == "PM":
                if self.hr.get() in range(1, 12):
                    valor_hora = self.hr.get() + 12
                else:
                    valor_hora = self.hr.get()
            # Ahora llamamos a la función Alarma con la información que el usuario ha ingresado para verificar si hemos alcanzado la hora de la alarma
            self.Alarma("%02d" % (valor_hora,), "%02d" % (self.min.get()))
        # Si el usuario ha hecho clic en el botón de cancelar alarma, restablecemos todo
        if detener_hizo_clic:
            hecho = False
            inicio_impreso = False
            detener_hizo_clic = False

    def detener_reloj(self):
        global hecho, detener_hizo_clic
        # Informamos al usuario que se ha cancelado la alarma imprimiéndolo en la terminal
        print("Alarma configurada para {}:{}{} ha sido cancelada".format(self.hr.get(), "%02d" % (self.min.get()), self.ampm.get()))
        # El botón de cancelar ahora se ha hecho clic
        detener_hizo_clic = True
        # Ahora se ha terminado con la alarma/bucle actual
        hecho = True
        # Los botones se restablecen a su estado original
        self.boton_cancelar.config(state="disabled")
        self.boton_alarma.config(state="active")

    def detener_audio(self):
        # Usamos PyGame para detener el audio ya que se ha hecho clic en el botón
        pygame.mixer.Sound.stop(sonido_alarma)
        # El botón de detener alarma se deshabilita y el botón de alarma se activa, básicamente se restablece todo
        self.boton_detener_alarma.config(state="disabled")
        self.boton_alarma.config(state="active")

    def Alarma(self, mi_hora, mi_minuto):
        global hecho, inicio_impreso, terminado
        # Si todavía no hemos terminado, seguimos esta declaración
        if not hecho:
            # Convertimos la información en cadenas (para que coincida con DateTime)
            mi_hora, mi_minuto = str(mi_hora), str(mi_minuto)
            # A continuación, extraemos los datos de la hora actual de DateTime y tomamos la información que queremos (hora y minuto)
            a = str(datetime.now())
            b = a.split(" ")[1].split(":")
            hora = b[0]
            minuto = b[1]
            # Ahora, si la hora de la alarma coincide con la hora actual, seguimos esta declaración. ¡La alarma sonará!
            if hora == mi_hora and minuto == mi_minuto:
                # Usamos pygame para reproducir audio, loops = -1 se refiere a un bucle infinito
                pygame.mixer.Sound.play(sonido_alarma, loops=-1)
                print("¡La alarma está sonando!")
                # Ahora hemos terminado
                hecho = True
                # También terminado
                terminado = True
                # Ahora cambiamos de nuevo el estado del botón de cancelar a deshabilitado y el estado del botón de detener alarma a activo
                # Esto es para que el usuario pueda detener la alarma, ya que se repetirá infinitamente
                self.boton_cancelar.config(state="disabled")
                self.boton_detener_alarma.config(state="active")
            else:
                # Si todavía no es la hora establecida, volvemos a llamar recursivamente a la función iniciar_reloj
                self.after(1000, self.iniciar_reloj)
            hecho = False
        # Si hemos terminado, lo que hacemos cuando suena la alarma, restablecemos todo
        if terminado:
            inicio_impreso = False
            terminado = False

app = AplicacionAlarma()
app.mainloop()
