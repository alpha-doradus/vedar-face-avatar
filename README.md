# Face Avatar
Face tracking y gestos de avatar.

## Instrucciones de uso
1. Ejecutar el script:
```
python3 avatarDetection.py
```
2. La cámara empezará a detectar la cara, sonrisa, palma de la mano y puño
3. Para cada gesto el avatar cambiará de estado:
  - Si no detecta la cara, empezará un contador hasta llegar a modo durmiendo
  - Si detecta sonrisa, el avatar pondrá el pulgar arriba
  - Si detecta puño, el avatar pondrá el pulgar abajo
  - Si detecta palma de la mano, el avatar alzará la mano

## Tech stack
- Python
- OpenCV
