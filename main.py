import sys
from quiz import Quiz

def get_default_quizzes():
    """기본 '쓸데없는 기초 상식' 퀴즈 5개 생성"""
    return [
        Quiz("바나나는 사실 나무가 아니라 '이것'에 속합니다. 무엇일까요?", ["풀(풀줄기)", "나무", "버섯", "덩굴식물"], 1),
        Quiz("다음 중 사과나무 과(Family)에 속하며 장미와 친척인 과일은?", ["바나나", "사과", "수박", "파인애플"], 2),
        Quiz("달팽이의 이빨 개수는 대략 몇 개일까요?", ["0개", "10개", "100개", "1만 개 이상"], 4),
        Quiz("플라밍고(홍학)의 깃털이 핑크색인 진짜 이유는 무엇일까요?", ["타고난 유전자", "새우/플랑크톤 섭취", "햇빛에 타서", "스트레스 때문에"], 2),
        Quiz("세계에서 가장 긴 이름을 가진 나라의 수도(방콕)의 풀네임은 몇 자 정도 될까요?", ["10자 미만", "30자 정도", "60자 정도", "100자 이상"], 4)
    ]

def display_menu():
    """메뉴 목록 출력"""
    print("\n==============================")
    print(" 💡 쓸데없는 기초 상식 퀴즈 게임 ")
    print("==============================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("==============================")

def get_valid_input(prompt, min_val, max_val):
    """
    사용자의 입력을 안전하게 받아 검증하는 예외 처리 함수입니다.
    - 공백 제거 후 숫자 변환 확인
    - 지정된 범위(min_val ~ max_val) 내부의 숫자인지 확인
    - Ctrl+C, EOF(입력 종료) 발생 시 안전하게 처리
    """
    while True:
        try:
            user_input = input(prompt).strip() # 입력값 앞뒤 공백 제거
            
            # 빈 입력(Enter만 침) 처리
            if not user_input:
                print("! 아무것도 입력하지 않았습니다. 다시 입력해 주세요.")
                continue
                
            # 숫자로 변환 시도
            num = int(user_input)
            
            # 범위 검사
            if min_val <= num <= max_val:
                return num
            else:
                print(f"! 잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력해 주세요.")
                
        except ValueError:
            # 숫자가 아닌 문자(예: abc) 입력 시
            print(f"! 잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력해 주세요.")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 누르거나 입력 스트림이 끊겼을 때
            print("\n\n! 강제 종료 신호가 감지되었습니다. 프로그램을 안전하게 종료합니다.")
            sys.exit(0)

def main():
    quiz_list = get_default_quizzes()
    
    while True:
        display_menu()
        # 1~5 사이의 안전한 메뉴 번호 받기
        choice = get_valid_input("선택: ", 1, 5)
        
        if choice == 1:
            print("\n[안내] '퀴즈 풀기' 기능은 곧 구현될 예정입니다.")
        elif choice == 2:
            print("\n[안내] '퀴즈 추가' 기능은 곧 구현될 예정입니다.")
        elif choice == 3:
            print("\n[안내] '퀴즈 목록' 기능은 곧 구현될 예정입니다.")
        elif choice == 4:
            print("\n[안내] '점수 확인' 기능은 곧 구현될 예정입니다.")
        elif choice == 5:
            print("\n게임을 종료합니다. 이용해 주셔서 감사합니다!")
            break

if __name__ == "__main__":
    main()

def add_quiz_flow(quiz_list):
    """새로운 퀴즈를 직접 등록하는 기능입니다."""
    print("\n--- 새로운 퀴즈 추가 ---")
    question = input("문제를 입력하세요: ").strip()
    
    # 빈 입력 방지 예외 처리
    if not question:
        print("! 문제는 비어 있을 수 없습니다.")
        return

    choices = []
    # 선택지 4개 받아오기
    for i in range(1, 5):
        choice = input(f"선택지 {i}: ").strip()
        if not choice:
            print("! 선택지는 비어 있을 수 없습니다.")
            return
        choices.append(choice)

    # 정답 번호 입력받기 (1~4 범위 검수)
    answer_input = input("정답 번호 (1-4): ").strip()
    if not answer_input.isdigit() or not (1 <= int(answer_input) <= 4):
        print("! 잘못된 입력입니다. 1~4 사이의 숫자를 입력하세요.")
        return

    # Quiz 객체로 만들어서 목록에 추가
    new_quiz = Quiz(question, choices, int(answer_input))
    quiz_list.append(new_quiz)
    print("✔ 퀴즈가 성공적으로 추가되었습니다!")


def show_quiz_list(quiz_list):
    """등록되어 있는 전체 퀴즈 목록을 보여줍니다."""
    print(f"\n--- 등록된 퀴즈 목록 (총 {len(quiz_list)}개) ---")
    if not quiz_list:
        print("등록된 퀴즈가 없습니다.")
        return

    for idx, quiz in enumerate(quiz_list, 1):
        print(f"[{idx}] {quiz.question}")