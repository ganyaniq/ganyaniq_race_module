from bs4 import BeautifulSoup

def parse_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    all_data = []
    for table in tables:
        headers = []
        header_row = table.find('tr')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        rows = table.find_all('tr')[1:]  # Başlık satırı atlandı
        table_data = []
        for row in rows:
            cols = row.find_all(['td', 'th'])
            row_data = {}
            for idx, col in enumerate(cols):
                key = headers[idx] if idx < len(headers) else f'col_{idx}'
                row_data[key] = col.get_text(strip=True)
            table_data.append(row_data)
        all_data.append(table_data)
    return all_data
