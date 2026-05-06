TITLE: RedCross Machine Solve
CATEGORY: HackTheBox
IMAGE: ./assets/htb.jpg
---
### Initial Access
Here is how I bypassed the initial filters using a custom script.
```python
import requests
print("Pwned")---

### Final Steps to Run:
1. Make sure you have your dependencies installed:
   `pip3 install markdown`
2. Place your uploaded images (`image_9290d4.png`, `image_928dd2.png`, `image_928d8c.png`) and a picture of yourself named `profile.jpg` into the `public/assets/` folder.
3. Run the script from the root of your project:
   `python3 build.py`
4. Open `public/index.html` in your browser.