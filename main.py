import os
import shutil
import subprocess

# --- Настройки ---
# Абсолютный путь или относительный путь к первому репозиторию
SOURCE_REPO = "../study-notebooks/notebooks"   # путь к папке notebooks из study-notebooks
TARGET_DIR = "notebooks"                       # локальная папка в my-notebooks
GIT_BRANCH = "main"

def sync_files():
    """Копирует все файлы из SOURCE_REPO в TARGET_DIR"""
    if not os.path.exists(SOURCE_REPO):
        raise Exception(f"Источник {SOURCE_REPO} не найден!")

    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # удаляем старые файлы
    for root, dirs, files in os.walk(TARGET_DIR):
        for f in files:
            os.remove(os.path.join(root, f))

    # копируем новые
    for root, dirs, files in os.walk(SOURCE_REPO):
        rel_path = os.path.relpath(root, SOURCE_REPO)
        target_subdir = os.path.join(TARGET_DIR, rel_path)
        os.makedirs(target_subdir, exist_ok=True)
        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(target_subdir, f)
            shutil.copy2(src_file, dst_file)

    print(f"Все файлы скопированы из {SOURCE_REPO} в {TARGET_DIR}")

def git_push():
    """Делает git add/commit/push"""
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Синхронизация ноутбуков"], check=False)
    subprocess.run(["git", "push", "origin", GIT_BRANCH], check=True)
    print("Изменения запушены в my-notebooks!")

def main():
    print("=== Синхронизация ноутбуков из study-notebooks в my-notebooks ===")
    sync_files()
    git_push()

if __name__ == "__main__":
    main()
