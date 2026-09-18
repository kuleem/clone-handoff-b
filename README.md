# Clone Handoff — Local B

给 VS Code/Codex 使用的 successor-B 本地执行器。

它会：
1. 从 Supabase 读取 `clone-handoff-001`
2. 作为独立 successor B 尝试原子 claim
3. 执行任务
4. 把结果写回 Supabase

不会模拟 B；只有实际连接并成功 claim 才会报告成功。

## 配置

复制 `.env.example` 为 `.env`，填写 `SUPABASE_URL` 和 `SUPABASE_SERVICE_ROLE_KEY`。

```bash
python -m pip install -r requirements.txt
python src/claim_and_run.py
```

不要把 `.env` 提交到 GitHub。
