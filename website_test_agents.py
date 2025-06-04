from crewai import Agent, Crew
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

LOGIN_URL = "https://example.com/login"  # TODO: replace with real login url
BASE_URL = "https://example.com/"        # TODO: replace with target url
USERNAME = "your_username"               # TODO: replace with your username
PASSWORD = "your_password"               # TODO: replace with your password


def login(session: requests.Session) -> requests.Session:
    payload = {"username": USERNAME, "password": PASSWORD}
    response = session.post(LOGIN_URL, data=payload)
    response.raise_for_status()
    return session


def find_broken_links(session: requests.Session, url: str) -> list[str]:
    page = session.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "html.parser")
    broken = []
    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link["href"])
        resp = session.get(full_url)
        if resp.status_code == 404:
            broken.append(full_url)
    return broken


login_agent = Agent(
    name="Login Bot",
    role="自動化登入程式",
    backstory="負責登入網站並維護會話。",
    goal="成功登入網站並維持登入狀態",
    llm="ollama/qwen3:30b-a3b",
)

link_checker_agent = Agent(
    name="Link Checker",
    role="Broken link 探測器",
    backstory="專門檢查網站連結是否可用。",
    goal="偵測並回報所有失效連結",
    llm="ollama/qwen3:30b-a3b",
)


def login_task():
    session = requests.Session()
    return login(session)


def link_check_task(session: requests.Session):
    return find_broken_links(session, BASE_URL)


def run_crew():
    crew = Crew(
        agents=[login_agent, link_checker_agent],
        tasks=[
            {
                "agents": [login_agent],
                "instructions": "登入目標網站並提供 Session 物件。",
                "expected_output": "已登入網站並建立 session",
            },
            {
                "agents": [link_checker_agent],
                "instructions": "利用登入後的 Session 檢查網站 broken links。",
                "expected_output": "列出所有失效連結",
            },
        ],
    )
    crew.run()


if __name__ == "__main__":
    run_crew()
