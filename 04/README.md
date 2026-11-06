# Week 4: Git Flow 與 GitHub Flow 工作流程實作筆記

## 1. Git Flow 架構
* **main**: 正式穩定上線分支。
* **develop**: 日常開發整合分支。
* **feature/***: 新功能分支，由 develop 切出，完成後合併回 develop。
* **release/*** & **hotfix/***: 版本發布準備與緊急線上修補分支。

## 2. GitHub Flow 實作流程
1. 從 main 建立功能分支：git checkout -b feature/update-ui`n2. 提交變更：git add . && git commit -m "Add feature"
3. 推送至遠端：git push -u origin feature/update-ui`n4. 發起 Pull Request (PR)，通過 Code Review 與自動化測試後 Merge 回 main。
