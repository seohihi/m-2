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
        """병아리 퀴즈 5개 생성"""
        return [
            Quiz("달걀에서 병아리가 부화하는 데 걸리는 기간은 약 며칠일까요?", ["14일", "21일", "30일", "45일"], 2),
            Quiz("병아리가 부화할 때 달걀껍데기를 깨고 나오기 위해 주둥이 끝에 생기는 특별한 돌기의 이름은 무엇일까요?", ["난치", "부리톱", "깃봉", "부리돌기"], 1),
            Quiz("병아리가 갓 태어난 직후 며칠 동안 음식을 먹지 않고도 견딜 수 있는 이유는 무엇 때문일까요?", ["몸속에 노란 난황(노른자)을 흡수했기 때문", "체내 지방 축적량이 높기 때문", "껍데기의 칼슘을 미리 섭취했기 때문", "수분을 몸속에 다량 저장했기 때문"], 1),
            Quiz("갓 부화한 병아리가 처음 본 움직이는 대상을 어미로 인식하고 평생 기억하여 졸졸 따라다니는 행동 특성을 무엇이라고 할까요?", ["세대 전승", "음향 순응", "각인", "파블로프 효과"], 3),
            Quiz("병아리가 모이를 먹은 후 잠시 보관하고 부드럽게 삭히는 신체 기관의 이름은 무엇일까요?", ["모래주머니", "모이주머니", "쓸개", "맹장"], 2)
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