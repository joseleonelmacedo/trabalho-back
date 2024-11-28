ZENBOT - An Integrated Project for Software Testing, Back-End, Data Science, and AI

ZENBOT is an API integrated with Telegram that allows users to consult inflation data in Brazil over the years. This project combines back-end development practices with economic data analysis and software testing, ensuring the reliability and functionality of the system. The main objective is to provide quick and easy access to information, helping users better track and understand the Brazilian economy. Additionally, ZENBOT also allows users to consult data on unemployment and GDP, and compare these figures across different periods.

### 1. Features
- Query inflation data for various years in Brazil.
- User-friendly interaction through a Telegram bot.
- Integration with economic datasets (CSV) for data processing and analysis.
- Modular design, enabling future expansions like the inclusion of additional economic indicators.

### 2. Project Structure
- Back-End: Developed in Python, focusing on efficient data handling and fast responses.
- Telegram Bot: Manages user interactions and presents requested information.
- Automated Testing: Ensures system stability and accuracy.
- Data Science: Utilizes libraries like pandas for reading and analyzing economic data.

### 3. Test Coverage

Tools Used:
- pytest and pytest-cov: Used to execute tests and generate detailed coverage reports.

Current Coverage:
- 85%, mainly covering critical functionalities like calculations and dataset queries.

Test Results:
- Tested Functions:
  - Accurate inflation calculation and display.
  - User input validation (e.g., handling invalid years or empty values).

### 4. Results Analysis

- High accuracy in inflation calculations.
- Robust data manipulation functions.
- Well-structured system, making it easy to maintain and expand.

- Reliance on well-formatted CSV files.

### 5. Conclusion and Key Takeaways

Developing ZENBOT has been a rewarding experience, offering valuable insights into collaborative development and technical problem-solving. Key highlights include:

- The Value of Testing: Automated tests significantly improved system reliability, identifying issues early and preventing problems in the final product.

Key Learnings:
- Tools like pytest are essential for building stable APIs.
- Detailed data analysis ensures accurate and user-relevant results.