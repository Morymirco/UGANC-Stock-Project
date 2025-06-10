import cv2
from pyzbar.pyzbar import decode
import sqlite3

def scanner_code_barre():
    cap = cv2.VideoCapture(0)
    found = None
    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            code = barcode.data.decode('utf-8')
            print("Code-barre détecté :", code)
            found = code
            cap.release()
            cv2.destroyAllWindows()
            return found
        cv2.imshow('Scanner code-barre', frame)
        if cv2.waitKey(1) == 27:  # ESC pour quitter
            break
    cap.release()
    cv2.destroyAllWindows()
    return None

code_barre = scanner_code_barre()
if code_barre:
    conn = sqlite3.connect("stock_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Articles WHERE code_barre LIKE ?", (f"%{code_barre}%",))
    article = cursor.fetchone()
    print("Article trouvé :", article)
    conn.close()