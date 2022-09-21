# Book parser from tululu.org

Parser for downloading pictures and books from the site https://tululu.org/ . At the end, it saves a json file with information about books.

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

- `--start_page [num]` - first download page (default value 1)
- `--end_page [num]` - last download page (default value 702)
- `--dest_folder [folder]` - directory for storing uploaded files (default value `content`)
- `--skip_imgs` - do not download pictures
- `--skip_txt` - do not download books
- `--json_path [folder]` - json file storage directory (default value `.`)

### Example
- Loads the first 2 pages of the book and does not download pictures :
```bash
python3 parse_tululu_category.py --start_page 1 --end_page 2 --skip_imgs
```

## Run
```bash
python3 parse_tululu_category.py --start_page 1 --end_page 2 --skip_imgs
```
- You will see directory structure:
```
.
├── parse_tululu_category.py
│   README.md
│   requirements.txt
│   books_content.json
│
└── content
    └── books/
    │      Административные рынки СССР и России.txt
    │      ...
    │
    └── images/
           imagesnopic.gif
           ...
```