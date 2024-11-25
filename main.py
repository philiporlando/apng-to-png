import os
from apng import APNG


def extract_pngs_from_apng(input_directory: str, output_directory: str):
    os.makedirs(output_directory, exist_ok=True)

    for file in os.listdir(input_directory):
        if file.lower().endswith(".apng"):
            apng_path = os.path.join(input_directory, file)
            folder_name = os.path.splitext(file)[0]
            folder_path = os.path.join(output_directory, folder_name)

            os.makedirs(folder_path, exist_ok=True)

            try:
                apng = APNG.open(apng_path)
                for i, (png, control) in enumerate(apng.frames):
                    output_png_path = os.path.join(folder_path, f"frame_{i:03}.png")
                    with open(output_png_path, "wb") as f:
                        f.write(png.to_bytes())
                print(f"Extracted frames from '{file}' into '{folder_path}'")
            except Exception as e:
                print(f"Failed to process '{file}': {e}")


def main():
    input_dir = "./data/input"
    output_dir = "./data/output"

    extract_pngs_from_apng(input_dir, output_dir)


if __name__ == "__main__":
    main()
