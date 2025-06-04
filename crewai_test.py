from crewai import Agent, Task, Crew

# Define two agents: one writer and one reviewer
writer = Agent(
    name="Writer",
    role="資深技術寫手",
    backstory="具備豐富AI教學撰寫經驗，能將技術內容用淺顯中文傳遞給初學者。",
    goal="撰寫技術說明",
    llm="ollama/qwen3:30b-a3b",
)

reviewer = Agent(
    name="Reviewer",
    role="AI 審稿專家",
    backstory="熟悉技術文件標準，熱衷於糾正寫作錯誤與提供回饋。",
    goal="校對內容並給建議",
    llm="ollama/qwen3:30b-a3b",
)

# Define tasks for each agent
write_task = Task(
    description="寫一份 AI Workflow 入門教學",
    expected_output="一篇清楚、結構良好的 AI Workflow 入門技術教學",
    agent=writer,
)

review_task = Task(
    description="回饋審查結果",
    expected_output="一篇經過審查的 AI Workflow 入門技術教學",
    agent=reviewer,
)


def run_crew():
    crew = Crew(agents=[writer, reviewer], tasks=[write_task, review_task])
    crew.run()


if __name__ == "__main__":
    run_crew()
