import json
import os
from quiz import Quiz

# 데이터 저장 파일명 정의
STATE_FILE = "state.json"


class QuizGame:
    """게임 전체 흐름과 데이터(퀴즈 목록, 최고 점수)를 관리하는 클래스입니다."""

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def get_default_quizzes(self):
        """기본 TMI 상식 퀴즈 5개 생성"""
        return [
            Quiz("바나나는 사실 나무가 아니라 풀이다?", ["O (풀이다)", "X (나무다)", "외계식물이다", "버섯류다"], 1),
            Quiz("딸기는 과일이 아니라 채소(채과류)로 분류된다?", ["O (채소다)", "X (과일이다)", "견과류다", "곡류다"], 1),
            Quiz("달팽이는 이빨이 있다?", ["없다", "약 10개", "약 1,000개", "1만 개 이상"], 4),
            Quiz("북극곰의 피부 색깔은 무슨 색일까?", ["하얀색", "검은색", "분홍색", "투명한색"], 2),
            Quiz("사과 씨앗에는 미량의 독소(청산가리 성분)가 존재한다?", ["O (있다)", "X (없다)", "설탕 성분이다", "비타민이다"], 1)
        ]

    def load_data(self):
        """state.json 파일에서 데이터를 불러옵니다."""
        if not os.path.exists(STATE_FILE):
            self.quizzes = self.get_default_quizzes()
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.quizzes = [Quiz(q["question"], q["choices"], q["answer"]) for q in data.get("quizzes", [])]
            if not self.quizzes:
                self.quizzes = self.get_default_quizzes()
            self.best_score = data.get("best_score", 0)

        except Exception:
            print("\n! 파일이 손상되어 기본 데이터로 초기화합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0

    def save_data(self):
        """state.json 파일에 저장합니다."""
        quiz_data = [{"question": q.question, "choices": q.choices, "answer": q.answer} for q in self.quizzes]
        data = {"quizzes": quiz_data, "best_score": self.best_score}
        
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n! 저장 중 오류 발생: {e}")

    def play(self):
        """퀴즈 풀기 기능 실행"""
        if not self.quizzes:
            print("\n! 풀 수 있는 퀴즈가 없습니다.")
            return

        print(f"\n퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0
        for idx, quiz in enumerate(self.quizzes, 1):
            quiz.display_quiz(idx)
            ans = input("정답 입력 (1-4): ").strip()
            if ans.isdigit() and quiz.is_correct(int(ans)):
                print("✔ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. (정답: {quiz.answer}번)")

        print(f"\n결과: {len(self.quizzes)}문제 중 {score}문제 정답!")
        if score > self.best_score:
            print(f"🎉 새로운 최고 점수 달성! ({self.best_score}점 ➔ {score}점)")
            self.best_score = score
            self.save_data()

    def add_quiz(self):
        """퀴즈 추가 기능 실행 (취소/뒤로가기 기능 포함)"""
        print("\n--- 새로운 퀴즈 추가 ---")
        print("(※ 작성 중 언제든지 'q'를 입력하면 메뉴로 돌아갑니다.)\n")

        # 1. 문제 입력
        question = input("문제를 입력하세요: ").strip()
        if question.lower() == 'q':
            print("↩ 퀴즈 추가를 취소하고 메뉴로 돌아갑니다.")
            return
        if not question:
            print("! 문제는 비어있을 수 없습니다.")
            return

        # 2. 선택지 4개 입력
        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if choice.lower() == 'q':
                print("↩ 퀴즈 추가를 취소하고 메뉴로 돌아갑니다.")
                return
            if not choice:
                print("! 선택지는 비어있을 수 없습니다.")
                return
            choices.append(choice)

        # 3. 정답 번호 입력
        answer_input = input("정답 번호 (1-4): ").strip()
        if answer_input.lower() == 'q':
            print("↩ 퀴즈 추가를 취소하고 메뉴로 돌아갑니다.")
            return
        if not answer_input.isdigit() or not (1 <= int(answer_input) <= 4):
            print("! 1~4 사이의 숫자를 입력해야 합니다.")
            return

        # 4. 저장 처리
        self.quizzes.append(Quiz(question, choices, int(answer_input)))
        self.save_data()
        print("✔ 퀴즈가 성공적으로 저장되었습니다!")
        
    def show_list(self):
        """퀴즈 목록 보기"""
        print(f"\n--- 등록된 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")

    def show_best_score(self):
        """최고 점수 확인"""
        print(f"\n🏆 현재 최고 점수: {self.best_score}점")