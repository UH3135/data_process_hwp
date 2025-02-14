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
