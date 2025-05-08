from logic import GradeCalc
from PyQt6.QtWidgets import QApplication
import sys

def main() -> None:
    """
    Creates the main window and runs the loop
    """
    app: QApplication = QApplication(sys.argv)

    try:
        window: GradeCalc = GradeCalc()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print('An unexpected error occurred: ' + str(e))

if __name__ == '__main__':
    main()