import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc

plt.rcParams['axes.grid'] = True

class Robot_2D_animacion():
  '''
  Clase para animar el movimiento de un manipulador robótico 2D en tiempo real.
    
  Atributos:
    fig: Objeto de la figura para la animación.
    ax: arreglo de subfiguras para graficar diferentes componentes de la animación.
    tt: Serie de datos de tiempo.
    qq: Serie de datos de ángulo de las articulaciones.
    ee: Serie de datos de error.
    xx: Serie de datos de posición del efector final.
  '''
  # Inicializa la figura y los subplots para la animación.
  fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 6), tight_layout=True)
  ax[0][0].set_aspect('equal')
  plt.close()

  # Crea gráficos para los componentes de la animación.
  line, = ax[0,0].plot([], [], 'o-', color='purple', lw=2) # Línea del eslabón
  joint, = ax[0,0].plot([], [], 'o', color='y', markersize=5) # Posición de la articulación
  trayectory, = ax[0,0].plot([], [], ':', color='r',markersize=1) # Trayectoria del efector final

  articulaciones = ax[1,0].plot([],[], [], [], [2.5], [0], lw=1) # Posiciones de las articulaciones
  posicion_x, = ax[0,1].plot([], [], lw=1) # Posición X del efector final
  posicion_y, = ax[0,1].plot([], [], lw=1) # Posición Y del efector final
  posicion_x_sp, = ax[0,1].plot([], [], 'g--', lw=1) # Posición X deseada
  posicion_y_sp, = ax[0,1].plot([], [], 'g--', lw=1) # Posición Y deseada
  error_x, = ax[1,1].plot([], [], lw=1) # Error en X
  error_y, = ax[1,1].plot([], [], lw=1) # Error en Y
  error_sp, = ax[1,1].plot([], [], 'g--', lw=1) # Error deseado (cero)

  # Pre-inicialización para las series datos a emplear
  tt = []
  qq = []
  ee = []
  xx = []

  @classmethod
  def reset_plot(cls):
    '''
    Reinicia los datos almacenados para la animación limpiando las listas de 
    tiempo, ángulo de las articulaciones, error y posición del efector final. 
    También establece un valor de error alto arbitrario.
    '''
    cls.tt.clear()
    cls.qq.clear()
    cls.ee.clear()
    cls.xx.clear()
    cls.e = 10000 # Arbitrary high error value
    
  @classmethod
  def configure_plot(cls, pos_deseada, time_end=2.5, epsilon=1e-1, max_iter=100):
    '''
    Configuración de los gráficos, incluyendo los límites para los ejes, leyendas y títulos
        
    Parámetros:
      pos_deseada (array-like): Posición deseada del efector final.
      time_end (float): El tiempo final para la simulación.
      epsilon (float): Tolerancia para el error, utilizado para determinar la convergencia.
      max_iter (int): Número máximo de iteraciones para la simulación.
    '''
    cls.reset_plot()
    cls.pos_deseada = pos_deseada
    cls.epsilon = epsilon
    cls.max_iter = max_iter
    cls.time_end = time_end

    # Establecer límites de los ejes y titulo para cada subgráfica
    cls.ax[0,0].set_title('Simulación del manipulador')
    cls.ax[0,0].set_xlim((-15, 15))
    cls.ax[0,0].set_ylim((-15, 15))
    cls.ax[0,0].grid(False)

    cls.ax[0,1].set_title('Posición del efector final')
    cls.ax[0,1].set_ylim((1.5 * min(pos_deseada), 1.5 * max(pos_deseada)))
    cls.ax[0,1].legend(['Coordenada X', 'Coordenada Y'])
    cls.ax[0,1].set_xlabel('Time')
    cls.ax[0,1].set_ylabel('Posición')

    cls.ax[1,0].set_title('Posición de las articulaciones')
    cls.ax[1,0].set_ylim(( -180, 180))
    cls.ax[1,0].legend(['q1', 'q2'])
    cls.ax[1,0].set_xlabel('Time')
    cls.ax[1,0].set_ylabel('Posición (°)')

    cls.ax[1,1].set_title('Errores')
    cls.ax[1,1].set_ylim(( -20, 20))
    cls.ax[1,1].legend(['Error en X', 'Error en Y'])
    cls.ax[1,1].set_xlabel('Time')
    cls.ax[1,1].set_ylabel('Posición')

  @classmethod
  def update_plot(cls, t, q, e, x1, y1, x2, y2):
    '''
    Actualiza el gráfico con los nuevos datos en cada frame de la animación.
        
    Parámetros:
      t (float): Tiempo actual.
      q (array-like): Ángulos actuales de las articulaciones.
      e (array-like): Valores actuales de error.
      x1 (float): Coordenada X actual de la primera articulación.
      y1 (float): Coordenada Y actual de la primera articulación.
      x2 (float): Coordenada X actual del efector final.
      y2 (float): Coordenada Y actual del efector final.
    '''
    cls.tt.append(t)
    cls.qq.append(np.rad2deg(q))
    cls.ee.append(e)
    cls.xx.append([x2, y2])
    cls.e = e

    # Direct array updates for efficiency
    q_array = np.array(cls.qq)
    x_array = np.array(cls.xx)
    e_array = np.array(cls.ee)

    cls.articulaciones[0].set_data(cls.tt, q_array[:,0])
    cls.articulaciones[1].set_data(cls.tt, q_array[:,1])

    cls.posicion_x.set_data(cls.tt, x_array[:,0])
    cls.posicion_y.set_data(cls.tt, x_array[:,1])

    cls.error_x.set_data(cls.tt, e_array[:,0])
    cls.error_y.set_data(cls.tt, e_array[:,1])

    cls.line.set_data([0, x1, x2], [0, y1, y2])
    cls.joint.set_data([0, x1], [0, y1])
    cls.trayectory.set_data(x_array.T)

    # auto escala las gráficas cuando el tiempo es 0 o supera time_end (2.5)
    if t==0 or t>cls.time_end:
      t_end = max(t,cls.time_end)
      cls.posicion_x_sp.set_data([0,t_end], [cls.pos_deseada[0],cls.pos_deseada[0]])
      cls.posicion_y_sp.set_data([0,t_end], [cls.pos_deseada[1],cls.pos_deseada[1]])
      cls.error_sp.set_data([0,t_end], [0,0])
      # recompute the ax.dataLim
      cls.ax[0,1].relim()
      cls.ax[1,0].relim()
      cls.ax[1,1].relim()
      # update ax.viewLim using the new dataLim
      cls.ax[0,1].autoscale_view()
      cls.ax[1,0].autoscale_view()
      cls.ax[1,1].autoscale_view()

  @staticmethod
  def gen():
    '''
    Genera frames para la animación mientras el error esté por encima del umbral
    especificado y no se haya alcanzado el número máximo de iteraciones.
    
    Yields:
      int: El número de la iteración actual.
    '''
    i = 0
    while np.linalg.norm(Robot_2D_animacion.e) > Robot_2D_animacion.epsilon and i < Robot_2D_animacion.max_iter:
        i += 1
        yield i
    if i == Robot_2D_animacion.max_iter:
      print('Se alcanzó el número máximo de iteraciones')
    else:
      print(f'Simulación terminó en {i} iteraciones con un error máximo de {np.linalg.norm(Robot_2D_animacion.e):.2f}')
      print(f'Robot alcanza ubicación {np.around(Robot_2D_animacion.xx[-1],2)} en {Robot_2D_animacion.tt[-1]:.2f} segundos')

  @classmethod
  def init(cls):
    '''
    Inicializa la animación estableciendo los datos de la línea como vacíos.
        
    Returns:
      tuple: Una tupla que contiene el objeto de línea inicializado.
    '''
    cls.line.set_data([], [])
    return (cls.line,)

  @classmethod
  def run_animation(cls, animate):
    """
    Ejecuta la animación utilizando FuncAnimation de matplotlib.
        
    Parámetros:
      animate (function): La función de animación que se llamará para cada fotograma.
    
    Returns:
      anim: El objeto de animación creado por FuncAnimation.
    """
    anim = animation.FuncAnimation(cls.fig, animate, init_func=cls.init,
                                   frames=cls.gen, interval=100, blit=True, repeat=False,
                                   cache_frame_data=False)

    # Nota: la siguiente parte es necesaria para ejecutar el código en colab
    rc('animation', html='jshtml')
    return anim
