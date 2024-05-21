# 오픈소스SW입문 기말프로젝트
## team G

### 🚀 python 슈팅 게임
---
- 이 자료는 이수안 컴퓨터 연구소에서 개발한 파이게임을 가지고 3가지 목차를 가지고 개선해나가고 있습니다.
  - 분할 컴파일
  - 기능 추가
  - Clean code 개선

### 📚 STACKS
---
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">

### 📁 작업 순서 및 git 규칙
---
- 이슈 생성
    - 이슈 제목: [♻ Clean code / ✨ Add feature / 🚨 Fix Bug / 🌈 Modify style] 이슈 제목
        ex. ✨ Add feature - 설정 탭 추가
    - 작업 내용 모두 완료했다면 close (close 해도 내역 확인 가능)

- 브랜치 생성
    - 브랜치 생성 명령어:
        - `git branch 브랜치명` (예: `pygame/이름-작업내역#이슈번호`)
        - 이슈번호 → 이슈 생성 시 제목 옆에 # 기호와 함께 뜸            
        - ex. `git branch "pygame/soobin-AddSettingTab#1"`

- **본인 브랜치 내에서 작업**
    - 브랜치 이동/변경 명령어:
        - `git switch 본인이 생성한 브랜치 이름`
        - ex. `git switch pygame/soobin-AddSettingTab#1`

- VSCode 내 변경 내역을 모두 **+** 하기 (모든 변경 내역을 commit으로 올리겠다)
    - VSCode 왼쪽 상단에 청진기 모양 아이콘(동그라미 3개 - 아래 사진 참고)을 누르면 본인이 작업한 내역이 뜸. 각 작업 내역마다 + 버튼을 눌러도 되고 제일 상단에 + 버튼으로 한 번에 올릴 수도 있음.
        
        
- 작업 내역 commit
    - `git commit -m “작업내역”`
    - 작업 내역 최대한 상세하게
    - ex. `git commit -m “Add SettingTab page, Add SettingIcon, Add SoundControl”`

- 직전에 commit한 내역 깃허브로 전송
    - `git push`

- PR 올리기    
    - 분류/작업내역#이슈번호
    - ex. `Refactor/DivisionCompile#1`
    - **develop**(main 아님) ← 본인의 작업 브랜치
                
- 다른 팀원이 PR 리뷰 후 승인 (comment 남기기)
    - 리뷰 방법 → 해당 브랜치로 이동 후 파일 실행
    - 올려진 PR의 작업내역이 모두 정상 작동 한다면 comment 남기기
        
        ex. 정상 작동합니다. 수고하셨습니다!
        
        ex. 어떠한 부분 수정 부탁드립니다.
        
- merge! (**반드시 PR을 올렸던 사람이 merge**)


### ✨ 변경된 작업 내역 적용하기 (merge된 내역 받아오기)
---
1. `git remote update`  
   변경된 사항 가져오기 (팀원이 만든 새로운 브랜치)

2. `git switch develop`  
   develop 브랜치로 변경

3. `git pull origin develop`  
   develop 브랜치에 merge된 업데이트 내역 가져오기

4. `git switch "본인이 작업할 브랜치명"`  
   내가 작업할 브랜치로 돌아오기

5. `git rebase develop`  
   develop 브랜치에 업데이트된 내역 내 작업 브랜치로 불러오기

6. 작업하기!
