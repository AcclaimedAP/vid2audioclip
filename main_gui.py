import os

if __name__ == "__main__":
    # Ensure temp directory exists
    os.makedirs(os.path.join(os.getcwd(), 'temp'), exist_ok=True)
    from src.gui import main
    main() 