from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from gui import Ui_Dialog
import csv

class GradeCalc(QMainWindow, Ui_Dialog):
    """
    A class that handles all logic for the grade calculator app
    """
    def __init__(self) -> None:
        """
        Connects all the buttons and creates the input fields
        """
        super().__init__()
        self.setupUi(self)

        #Connect submit button
        self.submit_button.clicked.connect(self.calculate_grades)

        #Connect total students input change
        self.t_students.textChanged.connect(self.update_score_fields)

        # Store score input fields
        self.score_fields: list[QLineEdit] = [
            self.student1,
            self.student2,
            self.student3,
            self.student4
        ]

        # Initially hide all score fields
        self.update_score_fields()

    def update_score_fields(self) -> None:
        """
        Show/hide score fields based on number of students
        """
        try:
            num_students = int(self.t_students.text()) if self.t_students.text() else 0
            if num_students < 0:
                raise ValueError("Number of students cannot be negative")

            #Show only required fields
            for i, field in enumerate(self.score_fields):
                field.setVisible(i < num_students)
                field.setEnabled(i < num_students)
                # Update corresponding label
                label = getattr(self, f"label_{i + 1}" if i > 0 else "label")
                #Access to the attribute using string
                label.setVisible(i < num_students)

        except ValueError:
            #Hide all fields if invalid input
            for i, field in enumerate(self.score_fields):
                field.setVisible(False)
                label = getattr(self, f"label_{i + 1}" if i > 0 else "label")
                label.setVisible(False)

    def calculate_grade(self, score: float, best_score: int) -> str:
        """
        Calculate grade based on score and best score
        :param score: the average of all the scores
        :param best_score: the highest of all the scores
        """
        if score >= best_score - 10:
            return 'A'
        elif score >= best_score - 20:
            return 'B'
        elif score >= best_score - 30:
            return 'C'
        elif score >= best_score - 40:
            return 'D'
        return 'F'

    def calculate_grades(self) -> None:
        """
        Process inputs and calculate grades
        """
        try:
            # Validate number of students
            num_students = int(self.t_students.text())
            if num_students <= 0:
                raise ValueError("Please enter a positive number of students")
            if num_students > len(self.score_fields):
                raise ValueError(f"Maximum {len(self.score_fields)} students allowed")

            # Get the scores
            scores: list[int] = []
            for i in range(num_students):
                score_text = self.score_fields[i].text()
                if not score_text:
                    raise ValueError(f"Please enter a score for student {i + 1}")
                try:
                    score = int(score_text)
                except ValueError:
                    raise ValueError(f'Score for student {i + 1} must be an integer')
                if not 0 <= score <= 100:
                    raise ValueError(f"Score for student {i + 1} must be between 0 and 100")
                scores.append(score)

            # Calculate grades
            best_score = max(scores)
            grades = [self.calculate_grade(score, best_score) for score in scores]

            # Calculate average
            average = sum(scores) / len(scores)
            average_grade = self.calculate_grade(average, best_score)

            #Format result text
            result_text = ""
            csv_data = [["Student", "Score", "Grade"]]
            for i, (score, grade) in enumerate(zip(scores, grades), 1):
                result_text += f"Student {i} score is {score} and grade is {grade}\n"
                csv_data.append([f"Student {i}", score, grade])
            result_text += f"The average score is {average:.2f}, a grade of {average_grade}"
            csv_data.append(["Average", f"{average:.2f}", average_grade])

            self.result.setText(result_text)

            #Save to CSV
            with open("grades_output.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(csv_data)

        except ValueError as e:
            if "invalid literal" in str(e):
                QMessageBox.warning(self, "Input Error", "Please enter a number")
            else:
                QMessageBox.warning(self, "Input Error", str(e))
