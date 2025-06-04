from crewai import Crew,Agent

agent1 = Agent(
    name="Writer",
    role="資深技術寫手",   # ← 必填！
    backstory="具備豐富AI教學撰寫經驗，能將技術內容用淺顯中文傳遞給初學者。", # ← 必填！
    goal="撰寫技術說明",
    llm="ollama/qwen3:30b-a3b"
)

agent2 = Agent(
    name="Reviewer",
    role="AI 審稿專家",
    backstory="熟悉技術文件標準，熱衷於糾正寫作錯誤與提供回饋。",
    goal="校對內容並給建議",
    llm="ollama/qwen3:30b-a3b"
)


crew = Crew(
    agents=[agent1, agent2],
    tasks=[
        {
        "agents": [agent1],
        "instructions": "寫一份 AI Workflow 入門教學",
        "expected_output": "一篇清楚、結構良好的 AI Workflow 入門技術教學"
        },
        {
        "agents": [agent2],
        "instructions": "回饋審查結果",
        "expected_output": "一篇經過審查的 AI Workflow 入門技術教學",
         "description": "寫一份 AI Workflow 入門教學",
         "expected_output": "一篇清楚、結構良好的 AI Workflow 入門技術教學"
         },
        {"from": [agent2],
         "to": agent1, 
         "description": "回饋審查結果",
         "expected_output": "一篇經過審查的 AI Workflow 入門技術教學"
        }
    ]
)
crew.run()