import logging
from pathlib import Path
from apng import APNG


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def ensure_directory_exists(directory: Path) -> None:
    """Ensure a directory exists, creating it if necessary."""
    directory.mkdir(parents=True, exist_ok=True)


def extract_frames(apng_path: Path, output_folder: Path) -> None:
    """
    Extract frames from an APNG file and save them as PNGs.

    Args:
        apng_path (Path): Path to the input APNG file.
        output_folder (Path): Path to the folder where extracted frames will be saved.
    """
    ensure_directory_exists(output_folder)

    try:
        apng = APNG.open(str(apng_path))
        for i, (png, control) in enumerate(apng.frames):
            output_png_path = output_folder / f"frame_{i:03}.png"
            with open(output_png_path, "wb") as f:
                f.write(png.to_bytes())
        logging.info(f"Extracted frames from '{apng_path.name}' into '{output_folder}'")
    except Exception as e:
        logging.error(f"Failed to process '{apng_path.name}': {e}")


def process_apng_files(input_directory: Path, output_directory: Path) -> None:
    """
    Process all APNG files in the input directory.

    Args:
        input_directory (Path): Path to the directory containing APNG files.
        output_directory (Path): Path to the directory where output will be saved.
    """
    ensure_directory_exists(output_directory)

    for file in input_directory.iterdir():
        if file.suffix.lower() == ".apng":
            folder_name = file.stem
            folder_path = output_directory / folder_name
            extract_frames(file, folder_path)


def main():
    """Main entry point for the script."""
    input_dir = Path("./data/input")
    output_dir = Path("./data/output")

    process_apng_files(input_dir, output_dir)


if __name__ == "__main__":
    setup_logging()
    main()
