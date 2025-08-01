# Access OLE Image Exporter

This Python script extracts OLE-embedded images from a MySQL database table (migrated from Microsoft Access), converts them to valid BMP format, and saves them as compressed JPG files.

## Features

- Connects to a MySQL database
- Extracts and decodes OLE-wrapped image BLOBs
- Converts to `.jpg` using Pillow
- Automatically compresses images larger than 300 KB
- Saves all images in the same folder as the script
- Names each image file based on a field from the database

## Requirements

- Python 3.8+
- Pillow
- mysql-connector-python

Install dependencies:

```bash
pip install pillow mysql-connector-python
```

## Usage

1. Edit the database connection in the script:
```python
conn = mysql.connector.connect(
    host='your_host',
    user='your_user',
    password='your_password',
    database='your_database'
)
```

2. Adjust the SQL query to match your database and table structure:
```python
cursor.execute("SELECT name_field AS 'ID', Image_field AS 'image' FROM your_schema.your_table WHERE Image_field IS NOT NULL")
```

3. Run the script:
```bash
python export_access_ole_images.py
```

4. JPG images will be saved next to the script.

---

Made with ❤️ by Felix
