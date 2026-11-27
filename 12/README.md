# 第12週：從 LLM API 到 AI Agent 的完整建構指南 (From LLM API to Agent)

本筆記與實作透過與 AI 協作，從最底層的無狀態 LLM API 呼叫開始，一步步建構出具備記憶、工具呼叫 (Tool Calling) 與 ReAct 自主迴圈的 AI Agent。

## 1. 什麼是 LLM API？（無狀態的起點）
- **本質**：LLM API 是一個無狀態 (Stateless) 的 HTTP POST 請求，傳入 `messages` 陣列，回傳下一個生成的文字回應。
- **核心角色 (Roles)**：
  - `system`：設定 AI 的行為準則、人設與可用工具說明。
  - `user`：使用者的提問或指令。
  - `assistant`：模型先前的回覆。

## 2. 加上記憶：對話迴圈 (Conversation Loop)
- 因為 API 本身沒有記憶，程式端必須維護一個 `messages = []` 串列。
- 每一輪對話都將新的 `user` 訊息與模型回傳的 `assistant` 訊息 `append` 進串列，並在下一次請求時整包送出，這就是多輪對話的基礎。

## 3. 賦予雙手：工具呼叫 (Tool / Function Calling)
- 純文字模型無法查即時時間、算複雜數學或讀寫本地檔案。
- **作法**：
  1. 在程式端定義實際的 Python 函式（例如 `calculate`、`get_current_time`）。
  2. 透過 System Prompt 或 API 的 `tools` 參數，告訴模型有哪些工具、參數格式為何。
  3. 當模型判斷需要外部資訊時，不直接回答，而是輸出結構化的工具呼叫指令（如 JSON：`{"tool": "calculate", "args": {"expr": "25 * 48"}}`）。
  4. 程式端攔截該指令、執行對應的 Python 函式，並將結果 (`Observation`) 塞回 `messages` 再次詢問模型。

## 4. 成為 Agent：ReAct 迴圈 (Reasoning + Acting)
當我們把「思考 -> 呼叫工具 -> 取得結果 -> 再思考」放進一個 `while` 迴圈，直到模型輸出最終答案 (`Final Answer`) 或達到最大步數 (`max_steps`)，就完成了最核心的 **AI Agent**：

1. **Thought (思考)**：分析使用者問題，決定需要什麼資訊。
2. **Action (行動)**：選擇工具並輸出呼叫參數。
3. **Observation (觀察)**：程式執行工具並回傳真實結果。
4. **Loop / Finish**：若資訊足夠則輸出最終答案；否則回到步驟 1 繼續推理。

## 5. 實作程式：`mini_agent.py`
本資料夾內的 `mini_agent.py` 實作了一個零外部套件相依的 ReAct Agent：
- 內建 3 個真實工具：`get_time`（取得目前時間）、`calculate`（安全數學運算）、`list_files`（列出資料夾檔案）。
- 內建 `MockLLM` 模擬器，不需付費 API Key 即可直接執行並觀察完整的 `Thought -> Action -> Observation -> Final Answer` 迴圈；也保留了串接真實 OpenAI/Gemini API 的標準介面。

### 執行方式
- 直接執行：`python mini_agent.py`

## 6. AI 協作說明
本週學習筆記與 `mini_agent.py` 實作透過與 Google Gemini 對話學習並完成。
