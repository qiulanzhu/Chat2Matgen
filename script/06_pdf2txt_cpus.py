import os
from PyPDF2 import PdfReader
import logging
from pathlib import Path
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import time


def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def convert_pdf_to_txt(args):
    """
    将单个PDF文件转换为TXT文件

    Args:
        args: 包含pdf_path和output_dir的元组
    """
    pdf_path, output_dir = args
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

        return f"成功转换: {pdf_path} -> {txt_path}"

    except Exception as e:
        return f"转换失败 {pdf_path}: {str(e)}"


def get_pdf_files(input_dir):
    """获取所有PDF文件的路径"""
    pdf_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


def process_directory(input_dir, output_dir, num_workers=None):
    """
    并行处理指定目录下的所有PDF文件

    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
        num_workers: 并行工作进程数，默认为CPU核心数
    """
    # 如果未指定工作进程数，使用CPU核心数
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有PDF文件路径
    pdf_files = get_pdf_files(input_dir)
    total_files = len(pdf_files)

    if total_files == 0:
        logging.info("没有找到PDF文件")
        return

    logging.info(f"找到 {total_files} 个PDF文件，使用 {num_workers} 个工作进程处理")

    # 准备参数
    args_list = [(pdf_file, output_dir) for pdf_file in pdf_files]

    # 使用进程池并行处理
    start_time = time.time()
    completed = 0

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(convert_pdf_to_txt, args) for args in args_list]

        for future in as_completed(futures):
            completed += 1
            logging.info(f"进度: {completed}/{total_files} - {future.result()}")

    end_time = time.time()
    logging.info(f"所有文件处理完成，耗时: {end_time - start_time:.2f} 秒")


def main():
    # 设置日志
    setup_logging()

    # 设置输入和输出目录
    input_dir = "/mnt/samba/tools/documents"  # 这里替换为你的PDF文件目录
    output_dir = "/mnt/samba/tools/documents_txt"  # 输出TXT文件的目录

    # 使用12个工作进程（保留4个核心给系统）
    num_workers = 12

    logging.info(f"开始处理目录: {input_dir}")
    process_directory(input_dir, output_dir, num_workers)


if __name__ == "__main__":
    main()