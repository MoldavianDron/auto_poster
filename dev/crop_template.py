import cv2
import numpy as np
from PIL import Image
import subprocess
import io

# Get screenshot from device via adb
def get_screenshot():
    result = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    img = Image.open(io.BytesIO(result.stdout))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def crop_template_from_screenshot(save_path="./new_template.png"):
    img = get_screenshot()
    clone = img.copy()
    roi = cv2.selectROI("Select template ROI and press ENTER or SPACE", img, fromCenter=False, showCrosshair=True)
    x, y, w, h = roi

    if w == 0 or h == 0:
        print("❌ No region selected, exiting.")
        cv2.destroyAllWindows()
        return

    cropped = clone[y:y+h, x:x+w]
    cv2.imwrite(save_path, cropped)
    print(f"✅ Template saved to: {save_path}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    crop_template_from_screenshot()
