import sys
from game import QuizGame


def main():
    game = QuizGame()

    while True:
        print("\n=== 나만의 TMI 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

        try:
            choice = input("선택: ").strip()
            if not choice.isdigit():
                print("! 1~5 사이의 숫자를 입력하세요.")
                continue

            num = int(choice)
            if num == 1:
                game.play()
            elif num == 2:
                game.add_quiz()
            elif num == 3:
                game.show_list()
            elif num == 4:
                game.show_best_score()
            elif num == 5:
                print("\n게임을 종료합니다. 이용해 주셔서 감사합니다!")
                sys.exit(0)
            else:
                print("! 1~5 사이의 숫자를 입력하세요.")

        except (KeyboardInterrupt, EOFError):
            print("\n\n! 프로그램이 중단되었습니다. 안전하게 종료합니다.")
            game.save_data()
            sys.exit(0)


if __name__ == "__main__":
    main()