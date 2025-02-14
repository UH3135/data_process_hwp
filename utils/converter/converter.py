from bs4 import BeautifulSoup
from PIL import Image
import html2text
import subprocess
import os


def get_hwp_filenames(directory):
    if not os.path.exists(directory):
        print(f"Error:'{directory}'가 존재하지 않습니다.")
        return []

    hwp_files = []
    for root, _, files in os.walk(directory):
        hwp_files.extend([os.path.join(root, f) for f in files if f.lower().endswith(".hwp")])

    if not hwp_files:
        print(f"해당 {directory}에 HWP 파일이 없습니다.")
        return []

    print(f"{len(hwp_files)}개의 HWP 파일을 찾았습니다.")

    return hwp_files


def hwp_to_md(hwp_path: str):
    filename = os.path.basename(os.path.splitext(hwp_path)[0])

    output_dir = os.path.abspath(f'assets/output/{filename}')
    md_path = os.path.join(output_dir, f'{filename}.md')    
    html_path = os.path.join(output_dir, 'index.xhtml')

    os.makedirs(output_dir, exist_ok=True)

    # HWP to HTML 변환
    try:
        command = f"hwp5html --output {output_dir} {hwp_path}"
        subprocess.run(command, shell=True, check=True)
        print(f"HWP to HTML 변환에 성공했습니다. {output_dir}")
    except FileNotFoundError as fe:
        raise FileNotFoundError(f"hwp5html 실행 파일을 찾을 수 없습니다. pyhwp가 정상적으로 설치되었는지 확인하세요. {str(fe)}")
    
    
    html_content = load_html_content(output_dir)

    print(f'html 파일을 성공적으로 로드했습니다.')
        

    # html to markdown
    md_converter = html2text.HTML2Text()
    md_converter.ignore_links = False   
    md_content = md_converter.handle(html_content)

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
    print(f"Markdown 파일이 생성되었습니다: {md_path}")


def load_html_content(file_dir: str):
    xhtml_path = os.path.join(file_dir, 'index.xhtml')
    with open(xhtml_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "xml")

    for img_tag in soup.find_all("img"):
        img_src = img_tag["src"]
        img_path = os.path.join(file_dir, img_src)

        if os.path.exists(img_path):
            img = Image.open(img_path)
            new_img_path = os.path.splitext(img_path)[0] + ".jpg"

            img.convert("RGB").save(new_img_path, "JPEG")
            img_tag["src"] = os.path.join('bindata', os.path.basename(new_img_path))
    
    with open(xhtml_path, "w+", encoding="utf-8") as file:
        file.write(str(soup))
        file.seek(0)
        html_content = file.read()
    return html_content


def convert_all_hwp2md():
    data_path = os.path.abspath('assets/')
    for file_path in get_hwp_filenames(data_path):
        hwp_to_md(file_path)