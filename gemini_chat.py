import os
import sys
import time
import argparse
import google.auth
from google import genai
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

console = Console()

# ---------------------------------------------------------
# [경로 설정] 루키님의 요구사항에 맞춘 경로 상수 (기존 코드 비침습)
# ---------------------------------------------------------
PROJECT_ROOT = "/Users/giri/GeminiSearchPJ"
LOG_DIR = os.path.join(PROJECT_ROOT, "GeminiLog")
REVIEW_DIR = os.path.join(PROJECT_ROOT, "CodeReview")
HISTORY_FILE = os.path.join(LOG_DIR, "history.log")
# ---------------------------------------------------------

def get_client():
    credentials, project_id = google.auth.default()
    return genai.Client(credentials=credentials, vertexai=True, location="asia-northeast3")

def save_history(mode, content):
    """지정된 GemeniLog 폴더에 히스토리 기록"""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{mode}] {content}\n"
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def handle_general_query(client, query_list):
    query = " ".join(query_list)
    save_history("GENERAL", query)
    
    console.print(f"\n[bold magenta]󰚩 Gemini[/bold magenta] 응답 중...\n")
    response_text = ""
    with Live(console=console, refresh_per_second=12, vertical_overflow="visible") as live:
        try:
            stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=f"당신은 15년 차 시니어 개발자 비서입니다. 답변은 핵심 위주로 명확하게 마크다운 형식으로 작성하세요.\n\n질문: {query}"
            )
            for chunk in stream:
                if chunk.text:
                    response_text += chunk.text
                    live.update(Markdown(response_text))
        except Exception as e:
            live.update(f"[bold red]에러 발생:[/bold red] {e}")

def handle_code_review(client, file_path):
    if not os.path.exists(file_path):
        console.print(f"[bold red]에러:[/bold red] 파일을 찾을 수 없습니다: {file_path}")
        return

    target_filename = os.path.basename(file_path)
    save_history("REVIEW", target_filename)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        code_lines = f.readlines()
    
    code_with_lines = "".join([f"{i+1}: {line}" for i, line in enumerate(code_lines)])
    
    # 지정된 CodeReview 경로에 파일 생성
    save_path = os.path.join(REVIEW_DIR, f"REVIEW_{target_filename}.md")
    os.makedirs(REVIEW_DIR, exist_ok=True)

    review_prompt = f"당신은 수석 아키텍트입니다. 다음 코드를 라인별로 정밀 리뷰하고 MD 형식으로 작성하세요: \n{code_with_lines}"

    console.print(f"\n[bold cyan]󰛓 {target_filename}[/bold cyan] 정밀 분석 및 파일 생성 중...")
    
    try:
        stream = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=review_prompt
        )
        with open(save_path, "w", encoding="utf-8") as f:
            for chunk in stream:
                if chunk.text:
                    f.write(chunk.text)
                    print(">", end="", flush=True)
        
        console.print(f"\n\n[bold green]✔ 분석 완료![/bold green] 결과: [white]{save_path}[/white]")
    except Exception as e:
        console.print(f"\n[bold red]에러 발생:[/bold red] {e}")

def main():
    parser = argparse.ArgumentParser(description="Gemini 시니어 개발자 비서")
    parser.add_argument("query", nargs="*", help="질문 내용 또는 파일 경로")
    parser.add_argument("-r", "--review", action="store_true", help="코드 리뷰 모드")
    parser.add_argument("-l", "--list", action="store_true", help="히스토리 목록 보기")
    
    args = parser.parse_args()

    if args.list:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                console.print(f"\n[bold green]📜 명령어 수행 히스토리[/bold green]\n")
                console.print(f.read())
        else:
            console.print("[yellow]히스토리 기록이 없습니다.[/yellow]")
        return

    if not args.query:
        console.print("[yellow]사용법: gemini \"질문\" 또는 gemini -r 파일경로[/yellow]")
        return

    client = get_client()
    if args.review:
        handle_code_review(client, args.query[0])
    else:
        handle_general_query(client, args.query)

if __name__ == "__main__":
    main()
