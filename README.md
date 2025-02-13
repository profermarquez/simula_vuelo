# Contexto

Este código en Python utiliza las bibliotecas pygame y numpy para crear una simulación aerodinámica sencilla de un avión moviéndose entre nubes, con efectos de sustentación, resistencia y ángulo de ataque que varían de forma aleatoria en cada ciclo de la simulación.
Luego aplicamos un algoritmos genéticos combinados con una matriz de covarianza para regular y optimizar el movimiento del avión. Este enfoque es similar al algoritmo de evolución estratégica conocido como CMA-ES (Covariance Matrix Adaptation Evolution Strategy).

# Creación y activacion del entorno virtual
/virtualenv env         /env/Scripts/activate.bat

# requerimientos
pip install pygame numpy cmaes

# Ejecución simulacion si cmaes y con cmaes
py simulacion_ala.py

py simulacion_ala_cmaes.py
