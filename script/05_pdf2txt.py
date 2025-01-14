import os
from PyPDF2 import PdfReader
import logging
from pathlib import Path


def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def convert_pdf_to_txt(pdf_path, output_dir):
    """
    将单个PDF文件转换为TXT文件

    Args:
        pdf_path: PDF文件的路径
        output_dir: 输出TXT文件的目录
    """
    try:
        # 创建与PDF文件同名的TXT文件路径
        txt_filename = Path(pdf_path).stem + '.txt'
        txt_path = os.path.join(output_dir, txt_filename)

        # 读取PDF文件
        reader = PdfReader(pdf_path)
        text_content = []

        # 提取每一页的文本
        for page in reader.pages:
            text_content.append(page.extract_text())

        # 将文本写入TXT文件
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write('\n'.join(text_content))

        logging.info(f"成功转换: {pdf_path} -> {txt_path}")

    except Exception as e:
        logging.error(f"转换失败 {pdf_path}: {str(e)}")


def process_directory(input_dir, output_dir):
    """
    处理指定目录下的所有PDF文件

    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 递归遍历目录
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                convert_pdf_to_txt(pdf_path, output_dir)


def main():
    # 设置日志
    setup_logging()

    # 设置输入和输出目录
    input_dir = "/mnt/samba/tools/documents"  # 这里替换为你的PDF文件目录
    output_dir = "/mnt/samba/tools/documents_txt"  # 输出TXT文件的目录

    logging.info(f"开始处理目录: {input_dir}")
    process_directory(input_dir, output_dir)
    logging.info("转换完成")


if __name__ == "__main__":
    main()