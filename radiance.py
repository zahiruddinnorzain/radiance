import os
print('Radiance v1.0')

os.system('uvicorn main:app --reload --host 0.0.0.0 --port 8000')