import shutil
import time

source_path = r'C:\Users\SNOMRAWE\Documents\Custom Office Templates\A\Test.txt'
destination_path = r'C:\Users\SNOMRAWE\Documents\Custom Office Templates\B\Test.txt'

def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
        print(f"Copied {src} to {dst}")
    except Exception as e:
        print(f"Error copying file: {e}")

if __name__ == "__main__":
    while True:
        copy_file(source_path, destination_path)
        time.sleep(600)  # Wait 10 minutes (600 seconds)