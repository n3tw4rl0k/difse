# Docker Image File System Extractor - DIFSE
import os
import sys
import tarfile
import subprocess
import shutil
import logging
import argparse


__version__ = '1.0.0'
__program_name__ = "difse"


logging.basicConfig(level=logging.INFO)
logging.info("Running {}".format(__program_name__))


def pull_docker_image(img_name):
    try:
        logging.info("Pulling Docker image: {}".format(img_name))
        subprocess.run(['docker', 'pull', img_name], check=True)
    except subprocess.CalledProcessError:
        logging.error("Error pulling Docker image: {}".format(img_name))
        sys.exit(1)


def save_docker_image_to_tar(img_name, tar_archive_name):
    try:
        logging.info("Saving Docker image {} to {}".format(img_name, tar_archive_name))
        subprocess.run(['docker', 'save', img_name, '-o', tar_archive_name], check=True)
    except subprocess.CalledProcessError:
        logging.error("Error saving Docker image {} to {}".format(img_name, tar_archive_name))
        sys.exit(1)


def extract_all_tars_in_directory(directory, extraction_dir):
    try:
        if not os.path.exists(extraction_dir):
            os.makedirs(extraction_dir)
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.tar'):
                    tar_path = os.path.join(root, file)
                    with tarfile.open(tar_path, 'r') as tar_archive:
                        tar_archive.extractall(path=extraction_dir)
                    logging.info("Extracted {} to {}".format(tar_path, extraction_dir))
    except Exception as e:
        logging.error("Error extracting tar files: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pull a Docker image, save it to a tar file, extract its contents and cleanup.")
    parser.add_argument("image_name", help="The name of the Docker image to pull and process.")
    args = parser.parse_args()
    
    image_name = args.image_name
    tar_name = "saved_docker_image.tar"
    extraction_root = "main_extraction"
    final_extraction_name = "RootFSExtracted"
    final_extraction_dir = os.path.join(extraction_root, final_extraction_name)
    
    pull_docker_image(image_name)
    save_docker_image_to_tar(image_name, tar_name)
    
    if not os.path.exists(extraction_root):
        os.makedirs(extraction_root)
    
    with tarfile.open(tar_name, 'r') as tar:
        tar.extractall(path=extraction_root)
    logging.info("Extracted main tar {} to {}".format(tar_name, extraction_root))
    
    extract_all_tars_in_directory(extraction_root, final_extraction_dir)
    
    for item in os.listdir(extraction_root):
        item_path = os.path.join(extraction_root, item)
        if item != final_extraction_name:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    logging.info("Cleanup completed. Final extraction is available at {}".format(final_extraction_dir))
    
    try:
        os.remove(tar_name)
        logging.info("Deleted the initial tar file: {}".format(tar_name))
    except Exception as e:
        logging.error("Error deleting the tar file {}: {}".format(tar_name, e))
