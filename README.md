# Book parser from tululu.org

Parser for downloading pictures and books from the site https://tululu.org/ .

## How to install

- Сlone this repository:
```bash
git@github.com:MaxHC-vlop/online_library_parsing.git
```

 - You must have python3.9 (or higher) installed to run the parser .

 - Create a virtual environment on directory project:
 ```bash
python3 -m venv env
 ```
- Start the virtual environment:
```bash
. env/bin/activate
```
- Then use pip to install dependencies:
```bash
pip install -r requirements.txt
```

## Arguments

- `--start_page` - what book ID to start with (default value 1)
- `--end_page` - what book ID to end with (default value 2)

### Example
- Downloads the first 8 books :
```bash
python3 main.py 1 11
```

## Run
```bash
python3 main.py
```
- You will see directory structure:
```
.
├── main.py
│   README.md
│   requirements.txt
│
├── books
│   └── Административные рынки СССР и России.txt
└── images
    └── imagesnopic.gif
```