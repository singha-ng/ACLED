# ACLED-MM

## Clone this dash app on your local computer

1. Create a virtual Python environment
   (`cd` command ဖြင့် ကိုယ်ထားချင်တဲ့ နေရာထိသွားပါ။ )

```bash
python3 -m venv .venv
```

This will create a new python environment in .venv folder.

2. Activate that environment

In Unix/Linux

```bash
source .venv/bin/activate
```

In Window (I'm not sure)

```
source .venv\Scripts\activate.bat
```

If it is not working, googling about `create and activate python virtual environment in window`.

3. Clone that GitHub repository.

```bash
git clone https://github.com/angel4demons/acled-mm.git
```

If `git` is not installed in Windows, install it. Follow [this link](https://gitforwindows.org/)

4. Go to that folder and install required Python libraries

```bash
 cd acled-mm/
 pip install -r requirements.txt
```

5. Done. To run the app

```bash
python3 src/app.py
```

To open this inside VSCode

```bash
code .
```
