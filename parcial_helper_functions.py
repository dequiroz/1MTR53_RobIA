import numpy as np

# Mapa de prueba del mundo, presentando los movimientos validos donde:
# 'B' representa hacia atras,
# 'L' representa hacia izquierda,
# 'F' representa hacia frente,
# 'R' representa hacia derecha.
test_world = [['B','B','L','L','B'],
              ['B','B','F','F','B'],
              ['B','B','F','F','B'],
              ['B','B','R','R','B']]

def show(p):
    """        
    Muestra una distribución de probabilidad bidimensional en formato legible.
    
    Args:
        p (list): Matriz 2D de probabilidades.
    """
    rows = ['[' + ','.join(map(lambda x: '{0:.4f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')

def uniform_distribution_2D(world):
  """
  Genera una distribución uniforme en una matriz 2D del mismo tamaño que el mundo.

  Args:
    world (list): Matriz 2D representando el entorno.
   
  Returns:
    list: Distribución uniforme de probabilidades en cada celda.
  """
  value = 1/np.size(world)
  return [[value for _ in row] for row in world]

class bcolors:
    """
    Clase para definir colores en la terminal para resaltar texto.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def validar_respuesta(caso, p, esperado, message=''):
  """
  Valida la respuesta generada comparándola con una respuesta esperada.

  Args:
    caso (int): Número del caso de prueba.
    p (list): Distribución de probabilidad obtenida.
    esperado (list): Distribución de probabilidad esperada.
    message (str): Mensaje opcional con detalles de la prueba.
  """
  try:
    p = [[round(val,4) for val in row] for row in p]
    assert p==esperado
    print(f'Caso {caso}: {bcolors.OKGREEN}Exitoso{bcolors.ENDC} ({message})')
    show(p)
  except AssertionError:
    print(f'Caso {caso}: {bcolors.FAIL}Error{bcolors.ENDC} ({message})')
    print(f'{bcolors.UNDERLINE}Se obtuvo el resultado{bcolors.ENDC}')
    show(p)
    print(f'{bcolors.UNDERLINE}se esperaba obtener{bcolors.ENDC}')
    show(esperado)
    print('')

def validar_pregunta1(sense):
  """
  Ejecuta pruebas unitarias para la función 'sense', verificando el ajuste de probabilidades 
  según las mediciones y la fiabilidad del sensor.

  Args:
    sense (function): Función de detección que ajusta probabilidades.
  """
  print(f'{bcolors.UNDERLINE}\nProbando función sense desarrollada{bcolors.ENDC}')
  p = uniform_distribution_2D(test_world)
  # Se define el vector de mediciones y movimientos
  measurements = ['B','L','F','R','B','L','F','R']
  # Se definen los resultados esperados para cada caso de prueba
  esperados = [
               [[0.0648, 0.0648, 0.0278, 0.0278, 0.0648], [0.0648, 0.0648, 0.0278, 0.0278, 0.0648], [0.0648, 0.0648, 0.0278, 0.0278, 0.0648], [0.0648, 0.0648, 0.0278, 0.0278, 0.0648]],
               [[0.0441, 0.0441, 0.1029, 0.1029, 0.0441], [0.0441, 0.0441, 0.0441, 0.0441, 0.0441], [0.0441, 0.0441, 0.0441, 0.0441, 0.0441], [0.0441, 0.0441, 0.0441, 0.0441, 0.0441]],
               [[0.0395, 0.0395, 0.0395, 0.0395, 0.0395], [0.0395, 0.0395, 0.0921, 0.0921, 0.0395], [0.0395, 0.0395, 0.0921, 0.0921, 0.0395], [0.0395, 0.0395, 0.0395, 0.0395, 0.0395]],
               [[0.0441, 0.0441, 0.0441, 0.0441, 0.0441], [0.0441, 0.0441, 0.0441, 0.0441, 0.0441], [0.0441, 0.0441, 0.0441, 0.0441, 0.0441], [0.0441, 0.0441, 0.1029, 0.1029, 0.0441]],
               [[0.0714, 0.0714, 0.0179, 0.0179, 0.0714], [0.0714, 0.0714, 0.0179, 0.0179, 0.0714], [0.0714, 0.0714, 0.0179, 0.0179, 0.0714], [0.0714, 0.0714, 0.0179, 0.0179, 0.0714]],
               [[0.0385, 0.0385, 0.1538, 0.1538, 0.0385], [0.0385, 0.0385, 0.0385, 0.0385, 0.0385], [0.0385, 0.0385, 0.0385, 0.0385, 0.0385], [0.0385, 0.0385, 0.0385, 0.0385, 0.0385]],
               [[0.0312, 0.0312, 0.0312, 0.0312, 0.0312], [0.0312, 0.0312, 0.125, 0.125, 0.0312], [0.0312, 0.0312, 0.125, 0.125, 0.0312], [0.0312, 0.0312, 0.0312, 0.0312, 0.0312]],
               [[0.0385, 0.0385, 0.0385, 0.0385, 0.0385], [0.0385, 0.0385, 0.0385, 0.0385, 0.0385], [0.0385, 0.0385, 0.0385, 0.0385, 0.0385], [0.0385, 0.0385, 0.1538, 0.1538, 0.0385]]]

  for i, (measurement, esperado) in enumerate(zip(measurements, esperados)):
    sensor_right = 0.7 if i<4 else 0.8
    sensor_wrong = 1 - sensor_right
    test = sense(p, test_world, measurement, sensor_right, sensor_wrong)
    validar_respuesta(i+1, test, esperado, message=f'Sense: {measurement} | sensor_right: {sensor_right}')

def validar_pregunta2(move):
  """
  Ejecuta pruebas unitarias para la función 'move', verificando los cambios en 
  la distribución de probabilidad según los movimientos en el entorno.

  Args:
    move (function): Función de movimiento que ajusta probabilidades.
  """
  print(f'{bcolors.UNDERLINE}\nProbando función move desarrollada{bcolors.ENDC}')
  # Se define el vector de mediciones y movimientos
  #  [0,0] - stay
  #  [0,1] - right
  #  [0,-1] - left
  #  [1,0] - down
  #  [-1,0] - up
  motions_cases = [[[0,1]],
                   [[0,-1]],
                   [[1,0]],
                   [[-1,0]],
                   [[0,0],[0,1],[0,1],[0,1],[0,1]],
                   [[0,0],[0,1],[-1,0],[0,1],[0,1]],
                   [[0,0],[0,1],[1,0],[0,1],[0,1]],
                   [[0,0],[0,1],[1,0],[0,1],[1,0]],
                   [[0,0],[0,1],[1,0],[0,1],[0,1]],
                   [[0,0],[0,1],[1,0],[0,1],[1,0]]]
  # Se definen los resultados esperados para cada caso de prueba
  esperados = [
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.2, 0.8, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.8, 0.2, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.2, 0.0, 0.0], [0.0, 0.0, 0.8, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.0, 0.0, 0.8, 0.0, 0.0], [0.0, 0.0, 0.2, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.4096, 0.4096, 0.0016, 0.0256, 0.1536], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.4096, 0.0, 0.0064, 0.0768, 0.3072], [0.1024, 0.0, 0.0016, 0.0192, 0.0768], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.1024, 0.0, 0.0016, 0.0192, 0.0768], [0.4096, 0.0, 0.0064, 0.0768, 0.3072], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0016, 0.0128, 0.0256], [0.0, 0.0, 0.0128, 0.1024, 0.2048], [0.0, 0.0, 0.0256, 0.2048, 0.4096]],
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.1029, 0.0, 0.0081, 0.0567, 0.1323], [0.2401, 0.0, 0.0189, 0.1323, 0.3087], [0.0, 0.0, 0.0, 0.0, 0.0]],
               [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0081, 0.0378, 0.0441], [0.0, 0.0, 0.0378, 0.1764, 0.2058], [0.0, 0.0, 0.0441, 0.2058, 0.2401]]]
  for i, (motions, esperado) in enumerate(zip(motions_cases, esperados)):
    p = [[0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]]
    for motion in motions:
      p_move = 0.8 if i<8 else 0.7
      p_stay = 1-p_move
      p = move(p, motion, p_move, p_stay)
    validar_respuesta(i+1, p, esperado, message=f'input={motions} | p_move={p_move}')

def validar_pregunta3(localize):
  """
  Ejecuta pruebas unitarias para la función 'localize', evaluando la precisión en
  la localización basada en secuencias de mediciones y movimientos.

  Args:
    localize (function): Función de localización.
  """
  print(f'{bcolors.UNDERLINE}\nProbando función move desarrollada{bcolors.ENDC}')
  mediciones_casos = [['B','B','F','F','B'],
                      ['B','B','B','L','L'],
                      ['B','B','B','F','F'],
                      ['B','B','B','F','R'],
                      ['B','B','F','F','B'],
                      ['B','B','B','L','L'],
                      ['B','B','B','F','F'],
                      ['B','B','B','F','R']]

  movimientos_casos = [[[0,0],[0,1],[0,1],[0,1],[0,1]],
                       [[0,0],[0,1],[-1,0],[0,1],[0,1]],
                       [[0,0],[0,1],[1,0],[0,1],[0,1]],
                       [[0,0],[0,1],[1,0],[0,1],[1,0]],
                       [[0,0],[0,1],[0,1],[0,1],[0,1]],
                       [[0,0],[0,1],[-1,0],[0,1],[0,1]],
                       [[0,0],[0,1],[1,0],[0,1],[0,1]],
                       [[0,0],[0,1],[1,0],[0,1],[1,0]]]

  esperados = [[[0.0192, 0.0240, 0.0193, 0.0237, 0.0402], [0.0364, 0.0240, 0.0286, 0.0784, 0.2061], [0.0364, 0.0240, 0.0286, 0.0784, 0.2061], [0.0192, 0.0240, 0.0193, 0.0237, 0.0402]],
               [[0.0163, 0.0437, 0.1713, 0.2338, 0.0189], [0.0163, 0.0437, 0.0597, 0.0429, 0.0093], [0.0163, 0.0437, 0.0597, 0.0429, 0.0093], [0.0163, 0.0437, 0.0597, 0.0429, 0.0093]],
               [[0.0124, 0.0333, 0.0455, 0.0327, 0.0071], [0.0124, 0.0333, 0.1306, 0.1782, 0.0144], [0.0124, 0.0333, 0.1306, 0.1782, 0.0144], [0.0124, 0.0333, 0.0455, 0.0327, 0.0071]],
               [[0.0386, 0.0608, 0.0506, 0.0089, 0.0104], [0.0386, 0.0608, 0.0641, 0.0112, 0.0104], [0.0386, 0.0608, 0.1181, 0.0207, 0.0104], [0.0386, 0.0608, 0.2442, 0.0428, 0.0104]],
               [[0.0092, 0.0195, 0.0087, 0.009, 0.0198], [0.0191, 0.0195, 0.0268, 0.0795, 0.2888], [0.0191, 0.0195, 0.0268, 0.0795, 0.2888], [0.0092, 0.0195, 0.0087, 0.009, 0.0198]],
               [[0.0128, 0.032, 0.2682, 0.3525, 0.0066], [0.0128, 0.032, 0.0394, 0.022, 0.0031], [0.0128, 0.032, 0.0394, 0.022, 0.0031], [0.0128, 0.032, 0.0394, 0.022, 0.0031]],
               [[0.0082, 0.0205, 0.0252, 0.0141, 0.002], [0.0082, 0.0205, 0.1716, 0.2256, 0.0042], [0.0082, 0.0205, 0.1716, 0.2256, 0.0042], [0.0082, 0.0205, 0.0252, 0.0141, 0.002]],
               [[0.0292, 0.0461, 0.033, 0.0018, 0.0071], [0.0292, 0.0461, 0.0626, 0.0034, 0.0071], [0.0292, 0.0461, 0.1318, 0.0071, 0.0071], [0.0292, 0.0461, 0.4087, 0.0221, 0.0071]]]

  #Ejecutar código usando las funciones
  for i, (mediciones, movimientos, esperado) in enumerate(zip(mediciones_casos, movimientos_casos, esperados)):
    if i<4:
      sensor_right = 0.7
      p_move = 0.8
    else:
      sensor_right = 0.8
      p_move = 0.7
    p = localize(test_world, mediciones, movimientos, sensor_right, p_move)
    validar_respuesta(i+1, p, esperado, message=f'input=> mediciones:{mediciones} | movimientos:{movimientos} | sensor_right:{sensor_right} | p_move:{p_move}')
