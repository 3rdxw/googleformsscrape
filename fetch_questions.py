import sys
import requests
from bs4 import BeautifulSoup

def fetch_form_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting questions
    questions = soup.select('div[role="listitem"] div[role="heading"]')

    if questions:
        for idx, question in enumerate(questions, start=1):
            question_text = question.get_text(strip=True)

            # Skip specific questions
            if question_text in ["التعليقات", "الإجابة الصحيحة"]:
                continue

            print(f"Question {idx}: {question_text}")

            # Find options within the question
            options_container = question.find_next('div', {'role': 'radiogroup'})
            if options_container:
                options = options_container.find_all('span', {'dir': 'auto'})  # Find based on 'dir' attribute
                if options:
                    for option in options:
                        data_value = option.get_text(strip=True)
                        #print(f"  Option: {data_value}")
                        
                        correct_answer = find_correct_answer(question)
                        if correct_answer==data_value:
                            print(f"  Option: {data_value} |||")
                        else:
                            print(f"  Option: {data_value}")

            # Find correct answer dynamically
            correct_answer = find_correct_answer(question)
            if correct_answer:
                print()
                #print(f"  Correct Answer: {correct_answer}")

            print()
    else:
        print("No questions found.")

def find_correct_answer(question):
    # Look for the correct answer near the question
    current_tag = question
    while current_tag:
        correct_answer = current_tag.find_next('div', class_='D42QGf')
        if correct_answer:
            correct_answer_span = correct_answer.find('span', {'dir': 'auto'})
            if correct_answer_span:
                return correct_answer_span.get_text(strip=True)
        current_tag = current_tag.find_next_sibling()

    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
    else:
        url = sys.argv[1]
        fetch_form_data(url)
