# Hook Runtime 集成复盘：不要把配置可见当成运行可信

> Current status: 本文记录 F005 期间 Stop / PreCompact / SessionStart hook 集成的历史复盘。F015 已将当前默认 hook runtime 收敛为 Stop-only；`PreCompact` / `SessionStart` session recovery 不再是现役默认能力。

## 背景

AgentMentor 的可选 hook runtime 经历了多轮修复：Codex 设置页能看到 hook，但 `PreCompact` 没有恢复产物；wrapper 手动运行成功，但真实生命周期事件没有 trace；最后又出现所有 hook 在 Codex UI 中都以 `code 1` 退出。

这些问题看起来像同一个“hook 不工作”，实际跨了多层不同事实。每一层都可能单独成立，也都可能在下一层失效。

## 四层证据模型

后续写 hook、改 hook 或验证 hook 时，至少区分四层证据：

1. **配置发现层**

   Codex 是否发现了 `hooks.json` 或 `hooks/hooks.json`，设置页是否显示事件，配置是否被信任。

   这只能证明 hook 被扫描到了，不能证明命令会执行。

2. **生命周期触发层**

   平台是否在真实 `Stop`、`PreCompact`、`SessionStart` 等事件发生时派发 hook。

   对 AgentMentor 来说，证据应该来自 `.agentmentor/hook-events/events.jsonl`、真实 recovery artifact，或能对应到 session log 的 lifecycle trace。

3. **命令包装层**

   平台执行的命令是否真的进入 wrapper，例如 `hooks/run-agentmentor-hook.cmd`。

   手动运行 wrapper 成功，只证明 wrapper 自身可用；不能证明平台用同样的 shell、环境变量和工作目录调用它。

4. **业务 runner 层**

   `agentmentor_hook.py` 是否能解析 payload、调用 `closeout_check.py` 或写 recovery snapshot，并输出平台能理解的结果。

   业务 block 应该是结构化 decision，例如 `decision=block`；它不应该表现为进程崩掉或 `code 1`。

## 这次为什么最后才修好

前几轮修复分别证明了不同层：

- 保留 root-level `hooks.json` 和 nested `hooks/hooks.json`，解决的是配置发现层。
- 启用 `[features].hooks` / `[features].plugin_hooks`，解决的是平台是否允许插件 hook。
- 增加 `.agentmentor/hook-events/events.jsonl`，解决的是生命周期触发有没有可观察证据。
- 手动执行 `run-agentmentor-hook.cmd stop` 和 `agentmentor_hook.py --event stop`，证明的是 wrapper 和 Python runner 自身能跑。

但这些都没有证明 **Codex 实际执行 `commandWindows` 时使用的 shell 语义**。

最后的问题是：

```text
"%PLUGIN_ROOT%\hooks\run-agentmentor-hook.cmd" stop
```

这条命令假设会被 `cmd.exe` 执行。真实环境中 Codex 可以通过 PowerShell 执行 hook 命令。PowerShell 不会展开 `%PLUGIN_ROOT%`，并且会把后面的 `stop` / `session-start` 当成语法错误，所以命令在进入 wrapper 之前就以 `code 1` 失败。

最终修复是显式进入 `cmd.exe`：

```text
cmd /d /s /c ""%PLUGIN_ROOT%\hooks\run-agentmentor-hook.cmd" stop"
```

关键保护不是这行命令本身，而是新增了回归测试：用 PowerShell 执行每个 `commandWindows`，只通过 `PLUGIN_ROOT` 环境变量提供插件根目录。旧命令稳定失败，新命令才通过。

## 写 hook 的反模式

### 反模式一：看到 UI 就认为 hook 生效

设置页显示 hook，只说明配置被发现。它不能证明真实生命周期事件会派发，也不能证明命令能跑。

### 反模式二：手动 runner smoke 代替平台调用验证

手动执行：

```text
hooks\run-agentmentor-hook.cmd stop
```

只能证明 wrapper 在当前 shell 中能跑。真实平台可能使用不同 shell、不同 cwd、不同 env expansion、不同 payload shape。

### 反模式三：把 shell 语义当成跨平台常量

Windows 上至少要区分：

- PowerShell 的 `$env:PLUGIN_ROOT`
- cmd.exe 的 `%PLUGIN_ROOT%`
- JSON 字符串中的 quote escaping
- `.cmd` wrapper 的调用方式
- Codex 实际使用哪个 shell 启动命令

只要 hook 命令依赖某个 shell 的变量展开，就必须用同一个 shell 语义做回归测试。

### 反模式四：把业务 block 和运行失败混在一起

Stop hook 因缺少 closeout block 而拦截完成声明，是业务结果；它应该输出结构化 block decision。

`hook exited with code 1` 是运行层失败，说明命令、wrapper、解释器、路径、权限或 shell 语义有问题。不要把它解释成“closeout 正常拦截”。

## 推荐验收清单

每次新增或修改 hook，至少完成这些检查：

1. **配置一致性**

   root-level `hooks.json`、nested `hooks/hooks.json`、skill 内示例配置必须一致。

2. **命令不依赖 cwd**

   不要在 `hooks.json` 中直接写 `python ./skills/...`。优先进入 wrapper，由 wrapper 根据自身路径反推插件根目录。

3. **Windows 命令用真实 shell 验证**

   对 Codex `commandWindows`，用 PowerShell 执行配置里的原始命令字符串：

   ```powershell
   $env:PLUGIN_ROOT = "C:\path\to\plugin"
   powershell -NoProfile -Command '<commandWindows value>'
   ```

   如果命令依赖 `%PLUGIN_ROOT%`，应显式包一层：

   ```text
   cmd /d /s /c ""%PLUGIN_ROOT%\hooks\run-agentmentor-hook.cmd" <event>"
   ```

4. **业务 allow/block 分开验证**

   对 Stop hook 分别验证：

   - 无完成声明时输出 allow。
   - 有完成声明但无 closeout block 时输出 block decision。
   - 有合法 closeout block 时输出 allow。
   - Codex 平台下业务 block 不应变成进程 `code 1`。

5. **真实安装链路验证**

   不只验证仓库源码。还要验证：

   - personal plugin source，例如 `C:\Users\HUAWEI\plugins\agentmentor`
   - Codex plugin cache，例如 `C:\Users\HUAWEI\.codex\plugins\cache\personal\agentmentor\...`
   - 本机 skills 安装目录，例如 `C:\Users\HUAWEI\.codex\skills\using-agentmentor`

6. **生命周期证据**

   修改后看 `.agentmentor/hook-events/events.jsonl` 或 recovery artifact。没有运行痕迹时，不要声称生命周期 hook 已经可依赖。

7. **回归测试锁住真实失败条件**

   这次新增的关键测试不是“字符串里包含 `%PLUGIN_ROOT%`”，而是“把配置里的 `commandWindows` 原样交给 PowerShell 执行，返回码必须为 0”。

## 最小测试矩阵

```text
Config discovery:
- root hooks.json equals hooks/hooks.json
- skill example config equals plugin config

Wrapper smoke:
- hooks/run-agentmentor-hook.cmd stop exits 0
- hooks/run-agentmentor-hook.cmd pre-compact exits 0
- hooks/run-agentmentor-hook.cmd session-start exits 0

PowerShell commandWindows smoke:
- SessionStart commandWindows exits 0
- PreCompact commandWindows exits 0
- Stop commandWindows exits 0

Runner behavior:
- Stop no completion claim -> allow
- Stop completion claim without closeout -> block decision, process exit 0 for Codex
- Stop valid closeout -> allow
- PreCompact writes same-session recovery snapshot
- SessionStart compact reads only same-session recovery snapshot

Lifecycle proof:
- real hook execution writes .agentmentor/hook-events/events.jsonl
- real PreCompact either writes recovery snapshot or diagnostics reports the lifecycle gap
```

## 判断一个 hook 修复是否真的完成

不要问“这段配置看起来对不对”。要问：

- 平台能发现它吗？
- 真实生命周期会触发它吗？
- 平台使用的 shell 能执行这条命令吗？
- wrapper 能找到 runner 吗？
- runner 能处理真实 payload 吗？
- 输出是否符合平台协议？
- 失败时是 fail open、结构化 block，还是进程崩溃？
- 验证覆盖的是源码、安装源，还是实际 cache？

只有这些问题都被证据回答，hook runtime 才算真正可依赖。

## 最终原则

Hook 集成不是“写一段配置调用脚本”，而是跨平台生命周期契约。它的验收单位不是配置文件存在，也不是 runner 手动成功，而是：

```text
真实平台事件 -> 真实命令入口 -> 真实 wrapper -> 真实 runner -> 可解释输出 -> 可观察证据
```

每次修改 hook，都要沿着这条链路验证。否则很容易修好上一层，又在下一层继续踩坑。
