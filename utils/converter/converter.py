from pydub import AudioSegment
from bs4 import BeautifulSoup
from PIL import Image
import win32com.client as win32
import html2text
import subprocess
import os

from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')

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
        logger.info(f"HWP to HTML 변환에 성공했습니다. {html_path}")
    except FileNotFoundError as fe:
        raise FileNotFoundError(f"hwp5html 실행 파일을 찾을 수 없습니다. pyhwp가 정상적으로 설치되었는지 확인하세요. {str(fe)}")
    
    # html 로드 및 bmp등의 이미지 jpg 변환
    xhtml_path = os.path.join(output_dir, 'index.xhtml')
    with open(xhtml_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "xml")

    for img_tag in soup.find_all("img"):
        img_src = img_tag["src"]
        img_path = os.path.join(output_dir, img_src)

        if os.path.exists(img_path):
            img = Image.open(img_path)
            new_img_path = os.path.splitext(img_path)[0] + ".jpg"

            img.convert("RGB").save(new_img_path, "JPEG")
            img_tag["src"] = os.path.join('bindata', os.path.basename(new_img_path))
    
    with open(xhtml_path, "w+", encoding="utf-8") as file:
        file.write(str(soup))
        file.seek(0)
        html_content = file.read()

    logger.info(f'html 파일을 성공적으로 로드했습니다.')
        

    # html to markdown
    md_converter = html2text.HTML2Text()
    md_converter.ignore_links = False   
    md_content = md_converter.handle(html_content)

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
    logger.info(f"Markdown 파일이 생성되었습니다: {md_path}")


def hwp_to_pdf(hwp_path:str):
    filename = os.path.basename(os.path.splitext(hwp_path)[0])
    output_dir = os.path.abspath(f'assets/output/{filename}')
    pdf_path = os.path.join(output_dir, f'{filename}.pdf') 

    try:
        hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
        logger.info('Hancom Office activate')

        hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")

        hwp.Open(hwp_path)
        logger.info(f'hwp 파일을 성공적으로 로드했습니다.')

        hwp.SaveAs(pdf_path, "PDF")
        logger.info(f"HWP to PDF 변환에 성공했습니다. {pdf_path}")
    except Exception as e:
        logger.error(f'hwp2pdf failed {str(e)}')
    finally:
        hwp.Quit()


def mp4_to_wav(mp4_path: str):
    filename = os.path.basename(os.path.splitext(mp4_path)[0])
    output_dir = os.path.abspath(f'assets/output/{filename}')
    audio_path = os.path.join(output_dir, f'{filename}.wav')

    logger.info(f"파일 오픈: {mp4_path}")
    audio = AudioSegment.from_file(mp4_path, format='mp4')

    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    
    audio.export(audio_path, format="wav")
    logger.info(f"변환 완료: {audio_path}")