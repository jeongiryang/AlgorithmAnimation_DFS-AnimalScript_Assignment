# DFS AnimalScript Generator Assignment

## 과제 개요

이 레포는 고정된 7개 노드 `A, B, C, D, E, F, G`로 구성된 무방향 그래프를 입력 파일에서 읽고, `A`부터 깊이 우선 탐색(DFS)을 수행한 뒤 DFS 방문 과정을 AnimalScript(`.asu`) 파일로 자동 생성하는 과제용 레포입니다.

직접 손으로 작성한 AnimalScript만 제출하는 구조가 아니라, 입력 파일을 읽어 AnimalScript를 생성하는 Python 프로그램을 포함합니다.

## 레포 목적

- `input/g1.txt`, `input/g2.txt` 그래프 입력 파일을 유지합니다.
- `src/dfs_animal_generator.py`가 입력 그래프를 검증하고 DFS를 수행합니다.
- 생성 프로그램이 `output/g1.asu`, `output/g2.asu` AnimalScript 파일을 만듭니다.
- 사용자는 생성된 `.asu` 파일을 Animal에서 실행한 뒤 캡처 이미지를 추가하고 최종 보고서를 정리합니다.

## 레포 구조

```text
README.md
input/
  g1.txt
  g2.txt
src/
  dfs_animal_generator.py
output/
  .gitkeep
screenshots/
  .gitkeep
report/
  .gitkeep
```

## 입력 파일 형식

입력 파일 첫 줄에는 간선 개수를 적습니다.

두 번째 줄부터는 무방향 간선을 한 줄에 하나씩 적습니다. 간선은 `AB`, `AC`처럼 노드 문자 2개로 작성합니다.

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

조건:

- 허용 노드는 `A`부터 `G`까지입니다.
- 자기 자신으로 가는 간선은 허용하지 않습니다.
- 중복 간선은 안전하게 무시합니다.
- 인접 노드는 알파벳순으로 방문합니다.
- DFS 시작 노드는 항상 `A`입니다.

## 실행 방법

```bash
python src/dfs_animal_generator.py input/g1.txt output/g1.asu
python src/dfs_animal_generator.py input/g2.txt output/g2.asu
```

## g1/g2 예상 DFS 방문 순서

- `g1`: `A -> B -> C -> D -> E -> F -> G`
- `g2`: `A -> B -> C -> D -> G -> F -> E`

## AnimalScript 생성 방법

생성기는 입력 파일을 읽고 다음 작업을 수행합니다.

1. 첫 줄의 간선 개수와 실제 간선 줄 수를 검증합니다.
2. 간선 형식, 허용 노드, 자기 간선을 검증합니다.
3. 무방향 인접 리스트를 만듭니다.
4. 인접 노드를 알파벳순으로 정렬해 `A`부터 DFS를 수행합니다.
5. DFS 방문 순서와 DFS tree edge를 콘솔에 출력합니다.
6. 각 DFS 단계가 `nextStep`으로 나뉜 AnimalScript 파일을 생성합니다.

생성된 애니메이션은 제목, 그래프 영역, 현재 단계 설명, 방문 순서, DFS stack, 후보 노드, 색상 범례, DFS tree edge 강조를 포함합니다.

## Animal에서 .asu 실행 후 캡처하는 방법

1. Animal을 실행합니다.
2. `File` 메뉴에서 생성된 `.asu` 파일을 엽니다.
3. `output/g1.asu`, `output/g2.asu`를 각각 실행해 DFS 애니메이션이 단계별로 보이는지 확인합니다.
4. 필요한 실행 화면을 캡처합니다.
5. 캡처 이미지는 추후 `screenshots/` 폴더에 정리합니다.

## 최종 제출물 정리 방법

최종 제출 시에는 생성 프로그램, 입력 파일, 생성된 AnimalScript, Animal 실행 캡처를 보고서에 정리합니다.

zip 파일 제출은 금지이며, 최종 제출은 Word 또는 HWP 문서 하나로 정리해야 합니다.

현재 `screenshots/` 폴더는 사용자가 추후 Animal 실행 캡처를 넣기 위한 자리입니다. 현재 `report/` 폴더는 사용자가 추후 Word/HWP 보고서 내용을 정리하기 위한 자리입니다.
