# Agents Team Orchestrator（已停止维护）

> [!IMPORTANT]
> 本仓库已经停止维护，并于 2026-07-17 归档。历史代码和链接继续保留，不再接受安装、Issue 或 Pull Request。

这个 Skill 为旧版 Codex 的多 Agent 协作设计。当前 Codex 的 MultiAgentV2 无法为原生 Subagent 安全指定不同模型与推理强度；继续使用旧编排方式会产生模型继承、额度失控和任务生命周期不可靠的问题。

Codex 用户请改用 [codex-model-routing-team](https://github.com/zjp1997720/zhijian-skills/tree/main/skills/codex-model-routing-team)。它使用 Codex App 原生后台任务，为独立任务显式路由模型与推理强度，并设置并发、归档和失败熔断边界：

```bash
npx skills add zjp1997720/zhijian-skills --skill codex-model-routing-team
```

Claude Code 已原生支持 Agent Teams，不需要安装这个旧 Skill。新问题和贡献请提交到 [zhijian-skills Issues](https://github.com/zjp1997720/zhijian-skills/issues)。
