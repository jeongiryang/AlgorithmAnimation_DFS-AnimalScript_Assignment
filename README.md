# DFS AnimalScript Generator Assignment

## 목차

- [1. 과제 개요](#1-과제-개요)
- [2. 과제 요구사항](#2-과제-요구사항)
- [3. 과제 안내 이미지](#3-과제-안내-이미지)
- [4. 구현 개요](#4-구현-개요)
- [5. 레포 구조](#5-레포-구조)
- [6. 입력 파일](#6-입력-파일)
- [7. DFS 수행 결과](#7-dfs-수행-결과)
- [8. 실행 방법](#8-실행-방법)
- [9. AnimalScript 생성 프로그램 설명](#9-animalscript-생성-프로그램-설명)
- [10. AnimalScript 생성 결과](#10-animalscript-생성-결과)
- [11. Animal 실행 결과](#11-animal-실행-결과)

## 1. 과제 개요

본 과제는 주어진 무방향 그래프를 깊이우선탐색(DFS)으로 탐색하는 과정을 AnimalScript 애니메이션으로 표현하는 과제이다. 그래프의 노드는 `A, B, C, D, E, F, G` 총 7개로 고정하며, 간선은 입력 파일에서 읽어 구성한다.

DFS는 시작 노드 `A`에서 출발한다. 인접 노드는 알파벳순으로 방문하며, 각 단계에서 노드 상태와 DFS 트리 간선을 시각적으로 표시한다. 초기 노드는 흰색, 방문 완료 노드는 회색, 현재 방문 노드는 분홍색, 방문 후보 노드는 푸른색으로 표현한다. DFS 방문에 사용된 간선은 굵은 검은색 선으로 강조한다.

script 생성 프로그램은 입력 파일을 읽어 DFS를 수행하고 `g1`, `g2`에 대한 AnimalScript를 자동 생성한다. 생성 결과는 `output/g1.asu`, `output/g2.asu`로 저장된다.

## 2. 과제 요구사항

과제 요구사항은 다음과 같다.

- 노드는 `A, B, C, D, E, F, G` 총 7개이다.
- 간선은 입력 파일로 제공한다.
- 입력 파일 첫 줄은 간선 개수이다.
- 두 번째 줄부터는 두 노드 이름이 한 줄에 표시된다.
- DFS 시작 노드는 `A`이다.
- 인접 노드는 알파벳순으로 방문한다.
- 그래프는 무방향 그래프로 처리한다.

1단계는 그래프 표시 단계이다.

- 노드는 흰색으로 표시한다.
- 간선은 가는 선으로 표시한다.

2단계는 `A`부터 방문하는 DFS 애니메이션 단계이다.

- 이미 방문한 노드는 회색으로 표시한다.
- 방금 방문한 노드는 분홍색으로 표시한다.
- 방문 후보 노드는 푸른색으로 표시한다.
- 방문에 사용된 간선은 굵은 선으로 표시한다.

제출물은 다음과 같다.

- script 생성 프로그램
- animal script
- animal 실행 결과 캡처
- `g1.txt`, `g2.txt` 각각의 실행 결과 캡처
- hwp 또는 word 형식 파일 하나
- zip 사용 금지

채점 기준은 다음과 같다.

- 애니메이션 작동 여부 50%
- 보기 좋게 그렸는가 20%
- 스크립트 생성 프로그램 사용 여부 30%

## 3. 과제 안내 이미지

아래 이미지는 과제 안내 자료이다. Animal 실행 결과 캡처가 아니라 과제 요구사항을 정리하기 위한 참고 이미지이다.

<table>
  <tr>
    <td align="center">
      <img src="screenshots/assignment_01_overview.png" width="420"><br>
      <sub>과제 개요</sub>
    </td>
    <td align="center">
      <img src="screenshots/assignment_02_input_example.png" width="420"><br>
      <sub>입력 파일 예시</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/assignment_03_animation_process.png" width="420"><br>
      <sub>애니메이션 과정</sub>
    </td>
    <td align="center">
      <img src="screenshots/assignment_04_initial_graph.png" width="420"><br>
      <sub>애니메이션 예시 1단계</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/assignment_05_dfs_step.png" width="420"><br>
      <sub>애니메이션 예시 2단계</sub>
    </td>
    <td align="center">
      <img src="screenshots/assignment_06_submission_details.png" width="420"><br>
      <sub>세부사항 및 제출물</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/assignment_07_grading_criteria.png" width="420"><br>
      <sub>채점기준</sub>
    </td>
  </tr>
</table>

## 4. 구현 개요

구현은 Python 표준 라이브러리만 사용한다. 외부 라이브러리나 웹 시각화 도구를 사용하지 않는다. 입력 파일을 검증한 뒤 무방향 그래프의 인접 리스트를 구성하고, 시작 노드 `A`부터 DFS를 수행한다.

인접 노드는 알파벳순으로 정렬한다. DFS 수행 과정에서 방문 순서와 DFS tree edge를 계산한다. 이후 계산된 이벤트 목록을 바탕으로 AnimalScript `.asu` 파일을 자동 생성한다.

생성된 AnimalScript는 단계별 `nextStep` 구조를 사용한다. 각 단계는 현재 단계 설명, 방문 순서, DFS 스택, 방문 후보 노드, DFS 트리 간선 정보를 갱신한다. 노드 상태는 흰색, 회색, 분홍색, 푸른색으로 구분하고, DFS 트리 간선은 굵은 검은색 선으로 표현한다. 화면 UI 라벨은 한글로 구성한다.

## 5. 레포 구조

파일 구성은 다음과 같다.

```text
README.md
input/
  g1.txt
  g2.txt
src/
  dfs_animal_generator.py
output/
  .gitkeep
  g1.asu
  g2.asu
screenshots/
  .gitkeep
  assignment_01_overview.png
  assignment_02_input_example.png
  assignment_03_animation_process.png
  assignment_04_initial_graph.png
  assignment_05_dfs_step.png
  assignment_06_submission_details.png
  assignment_07_grading_criteria.png
  result_g1_01_initial.png
  result_g1_02_start_candidate.png
  result_g1_03_middle_step.png
  result_g1_04_final.png
  result_g2_01_initial.png
  result_g2_02_start_candidate.png
  result_g2_03_middle_step.png
  result_g2_04_final.png
```

## 6. 입력 파일

`input/g1.txt`의 내용은 다음과 같다.

```text
7
AB
AD
BC
CD
BE
EF
FG
```

`g1.txt`는 간선 7개를 가진 무방향 그래프를 의미한다. 첫 줄 `7`은 이후에 입력되는 간선 줄 수와 일치한다.

`input/g2.txt`의 내용은 다음과 같다.

```text
10
AB
AC
AD
BC
CD
BE
CF
DG
EF
FG
```

`g2.txt`는 간선 10개를 가진 무방향 그래프를 의미한다. 첫 줄 `10`은 이후에 입력되는 간선 줄 수와 일치한다.

두 입력 파일 모두 노드 `A`부터 `G`까지만 사용한다. 각 간선은 `AB`, `AC`와 같이 두 노드 문자로 표현한다.

## 7. DFS 수행 결과

DFS 수행 결과는 다음과 같다.

| 입력 파일 | DFS 방문 순서 | DFS tree edges |
| --- | --- | --- |
| `g1.txt` | `A -> B -> C -> D -> E -> F -> G` | `AB, BC, CD, BE, EF, FG` |
| `g2.txt` | `A -> B -> C -> D -> G -> F -> E` | `AB, BC, CD, DG, GF, FE` |

그래프는 무방향 그래프이다. 따라서 `g2`의 `GF`, `FE`는 각각 입력 간선 `FG`, `EF`를 DFS 진행 방향 기준으로 표시한 것이다.

## 8. 실행 방법

AnimalScript 생성 명령은 다음과 같다.

```bash
python src/dfs_animal_generator.py input/g1.txt output/g1.asu
python src/dfs_animal_generator.py input/g2.txt output/g2.asu
```

Animal 실행 방법은 다음과 같다.

1. Animal을 실행한다.
2. `File` 메뉴에서 생성된 `.asu` 파일을 연다.
3. `output/g1.asu`, `output/g2.asu`를 각각 실행한다.
4. 단계별 DFS 애니메이션 결과를 확인한다.

## 9. AnimalScript 생성 프로그램 설명

`src/dfs_animal_generator.py`는 본 과제의 script 생성 프로그램이다. 입력 그래프 파일을 읽고 DFS를 수행한 뒤 AnimalScript 파일을 생성한다.

### 입력 검증

생성 프로그램은 입력 파일 존재 여부를 확인하고, 첫 줄의 간선 개수가 실제 간선 줄 수와 일치하는지 검사한다. 간선 형식은 두 문자로 제한한다. 노드는 `A`부터 `G`까지만 허용한다. 자기 자신으로 가는 간선은 거부한다. 중복 간선은 안전하게 무시한다.

### 그래프 구성

입력 간선은 무방향 간선으로 처리한다. 각 간선 `AB`는 `A`의 인접 노드에 `B`를 추가하고, `B`의 인접 노드에 `A`를 추가하는 방식으로 반영한다. 모든 인접 리스트는 알파벳순으로 정렬한다.

### DFS 탐색

DFS는 시작 노드 `A`에서 시작한다. 인접 노드는 정렬된 순서대로 검사한다. 아직 방문하지 않은 인접 노드를 발견하면 후보 노드로 표시하고, 해당 간선을 DFS tree edge로 기록한 뒤 재귀적으로 방문한다.

### 애니메이션 상태 구성

DFS 진행 중 각 이벤트를 단계 정보로 저장한다. 저장되는 정보는 현재 단계 설명, 방문 순서, DFS 스택, 방문 후보 노드, DFS 트리 간선 목록이다. 노드 상태는 초기, 방문 완료, 현재 방문, 방문 후보로 구분한다.

### AnimalScript 출력

프로그램은 계산된 이벤트 목록을 이용해 `.asu` 파일을 생성한다. 각 이벤트는 `nextStep`으로 분리한다. 화면에는 제목, 그래프 영역, DFS 진행 과정 패널, 방문 순서, DFS 스택, 방문 후보 노드, DFS 트리 간선, 범례를 배치한다.

## 10. AnimalScript 생성 결과

생성 결과 파일은 다음과 같다.

- `output/g1.asu`
- `output/g2.asu`

두 파일은 모두 `src/dfs_animal_generator.py` 실행으로 생성한다. 파일은 `%Animal 2` 형식과 `stepMode true` 설정을 사용한다. 각 DFS 단계는 `nextStep`으로 분리되어 Animal에서 단계별 애니메이션으로 확인할 수 있다.

화면 구성 요소는 다음과 같다.

- 제목
- 그래프 영역
- DFS 진행 과정
- 방문 순서
- DFS 스택
- 방문 후보 노드
- DFS 트리 간선
- 범례

생성 결과는 `output/g1.asu`와 `output/g2.asu`로 저장된다.

## 11. Animal 실행 결과

다음 이미지는 Animal에서 생성된 `.asu` 파일을 실행한 결과이다.

### g1 실행 결과

<table>
  <tr>
    <td align="center">
      <img src="screenshots/result_g1_01_initial.png" width="440"><br>
      <sub>g1 초기 그래프</sub>
    </td>
    <td align="center">
      <img src="screenshots/result_g1_02_start_candidate.png" width="440"><br>
      <sub>g1 시작 노드와 후보 노드 표시</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/result_g1_03_middle_step.png" width="440"><br>
      <sub>g1 중간 DFS 진행 단계</sub>
    </td>
    <td align="center">
      <img src="screenshots/result_g1_04_final.png" width="440"><br>
      <sub>g1 DFS 완료</sub>
    </td>
  </tr>
</table>

### g2 실행 결과

<table>
  <tr>
    <td align="center">
      <img src="screenshots/result_g2_01_initial.png" width="440"><br>
      <sub>g2 초기 그래프</sub>
    </td>
    <td align="center">
      <img src="screenshots/result_g2_02_start_candidate.png" width="440"><br>
      <sub>g2 시작 노드와 후보 노드 표시</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/result_g2_03_middle_step.png" width="440"><br>
      <sub>g2 중간 DFS 진행 단계</sub>
    </td>
    <td align="center">
      <img src="screenshots/result_g2_04_final.png" width="440"><br>
      <sub>g2 DFS 완료</sub>
    </td>
  </tr>
</table>
