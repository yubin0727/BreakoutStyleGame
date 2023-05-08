# Breakout-style Game
블록깨기 - 파이썬의 pygame을 이용하여 블록깨기 제작  

## 개발 환경  
  파이썬  
  
## 개발 계획  
  3주차~6주차 -> 플레이하면서 오류 발견하고 수정  
  
  |  주차  |  계획  |
  | :-----: | :-----: |
  | 1주차 | 파이썬 및 pygame 모듈 사용법 익히기 |
  | 2주차 | 블록깨기 시작 화면 및 공, 게임바 생성 |
  | 3주차 | 블록 생성 / 공이 블록과 충돌했을 때 블록 사라지도록 하기 |
  | 4주차 | 일정 시간이 지나면 블록이 새로 생성되고 아래로 내려오도록 하기 / 공 이동 속도 및 블록 생성 속도 조절되도록 수정 |
  | 5주차 | 게임 종료 조건, 종료 후 점수 표시 |
  | 6주차 | 난이도 설정 기능 추가 |  
  
## 핵심 기능
   |  class  |  설명  |
   | :-----: | :-----: |
   | class Ball() | 공의 움직임을 위한 class |
   | class makeR() | block, paddle 생성을 위한 class |
   | class button() | 시작 메뉴 버튼을 위한 class |

   |  def  |  설명  |
   | :-----: | :-----: |
   | def makeBlock() | 게임 진행 중 새로운 블록 생성을 위한 함수 |
   | def DisplayScore(text_color, text_pos) | 게임 진행 중 화면에 점수와 레벨 표시 |
   | def updateLevel() | 게임 중 레벨 업데이트 / 레벨에 따라 공 속도, 블록 생성 속도 조절 |
   | def quitButton() |     |
   | def initialize(n) | 게임 난이도에 따라 처음 공 속도, 블록 생성 속도, paddle 크기 설정 |
   | def Game() | 게임 진행 |
   
* __StartGame()__ - 게임 시작 화면
   * 게임 이름 표시  
   * 시작, 설정, 종료 버튼  
   * Settings -> Menu()로 이동  
   * initialize -> 게임 시작 전 난이도에 따라 변수들 값 설정
* __Menu()__ - 설정 화면
   * 난이도, 색, 사이즈 조절
* __main()__ - 게임 진행
   * Game()
   * makeBlock() -> 일정 시간(blocktime)이 지날 때마다 블록이 생성됨
   * DisplayScore()
* __FinishGame()__ - 최종 점수 표시
  
* __bool(done, se, go)__ 을 이용하여 StartGame(), Menu(), main(), FinishGame() 사이를 이동
