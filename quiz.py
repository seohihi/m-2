class Quiz:
    """퀴즈 1개의 문제, 선택지, 정답을 관리하는 클래스입니다."""[cite: 1]

    def __init__(self, question, choices, answer):
        # self.question: 문제 텍스트를 저장합니다.
        self.question = question
        # self.choices: 4개의 보기 목록을 저장합니다.
        self.choices = choices
        # self.answer: 정답 번호(1~4 중 하나)를 저장합니다.
        self.answer = answer

    def display_quiz(self, quiz_num):
        """화면에 퀴즈 문제와 4개 선택지를 출력합니다."""
        print(f"\n[문제 {quiz_num}] {self.question}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"  {idx}. {choice}")

    def is_correct(self, user_answer):
        """입력한 정답 번호가 맞는지 확인합니다."""
        return user_answer == self.answer
    