# AI 长期记忆：LDLWinToolBox 项目

## 项目基本信息

**项目名称：** LDL Windows ToolBox  
**项目简述：** 一个高度集成的 Windows Batch 实用工具，提供系统清理、完整性修复、组件更新和 NVMe SSD 优化功能  
**仓库地址：** https://github.com/LoveDoLove/LDLWinToolBox  
**主文件：** `LDLWinToolBox.bat`  
**许可证：** Apache License 2.0  

---

## 用户偏好与项目约定

### 编程风格与标准

1. **语言要求**
   - 主要语言：Windows Batch (`.bat`)
   - 辅助语言：PowerShell（仅当 Batch 无法满足时）
   - 目标系统：Windows 10 及 Windows 11

2. **代码规范**
   - 使用 `setlocal EnableDelayedExpansion` 启用延迟变量展开
   - 变量使用 `!VAR!` 形式在循环或条件块中引用
   - 添加清晰的注释块标记不同功能模块
   - 日志输出统一重定向到 `!LOGFILE!`

3. **菜单驱动设计**
   - 主菜单呈现数字选项（1-8）供用户选择
   - 每项功能对应一个 `:label` 跳转标签
   - 所有用户输入必须进行净化和验证

### 项目设计原则

1. **双层权限提升**
   - 脚本启动时使用 `cacls.exe` 检查管理员权限
   - 若无权限，使用 PowerShell `RunAs` 动词重新启动脚本
   - 永远不修改这一逻辑

2. **日志管理**
   - 每次运行生成时间戳日志文件：`LDLWinToolBox_yyMMddHHmmss.log`
   - 使用 PowerShell `Get-Date -Format yyMMddHHmmss` 生成时间戳
   - 控制台显示友好摘要，完整详细信息存入日志

3. **安全第一**
   - 任何破坏性操作前显示确认对话
   - 长期操作（>1 分钟）需提前警告用户并提供中断选项
   - 网络重置、WinSxS 清理等高风险操作需明确警告

4. **用户体验**
   - 清晰的进度反馈（当前处理的文件夹等）
   - 动态计算结果展示（如清理释放的空间）
   - 统一的菜单导航和确认流程

---

## 现有功能模块详解

### 功能 1：高级系统清理 (Advanced System Cleanup)

**菜单位置：** [1]  
**主要操作：**
- 停止 Windows Update 服务 (`wuauserv`) 和 BITS (`bits`)
- 清理 `%WinDir%\SoftwareDistribution\Download` 中的旧更新数据
- 清理 `%SystemRoot%\Temp` 和 `%TEMP%` 临时文件
- 删除后重建临时目录确保结构完整
- 使用 PowerShell WMI 计算清理前后的磁盘空间差异

**技术细节：**
- 使用循环逐个删除文件
- 目录删除采用 `rd` 然后 `md` 重建的方式
- 空间计算基于 `Win32_LogicalDisk` 的 FreeSpace 属性

---

### 功能 2：系统完整性修复 (System Integrity Repair)

**菜单位置：** [2]  
**主要操作：**
- 运行 `sfc /scannow` 扫描系统文件完整性
- 运行 `DISM /RestoreHealth` 从 Windows 缓存恢复损坏文件
- 提前警告用户该过程耗时 15-45 分钟
- 提供 Y/N 确认机制

**注意事项：**
- 该过程可以安全中断（关闭窗口）
- 必须有管理员权限
- 日志记录详细的修复结果

---

### 功能 3：Windows 组件存储清理 (WinSxS Cleanup)

**菜单位置：** [3]  
**主要操作：**
- 执行 `DISM /StartComponentCleanup` 清理旧的 Windows Update 安装文件
- 移除 WinSxS 中的过时组件缓存
- 重要警告：用户不应中断此过程，否则可能损坏未来的 Windows 更新

**安全考虑：**
- 需要额外的确认对话
- 必须明确说明中断的后果
- 提供详细的日志输出用于故障排查

---

### 功能 4：更新所有已安装应用 (Update Apps with Winget)

**菜单位置：** [4]  
**主要操作：**
- 使用 Windows Package Manager (`winget`) 自动更新所有已安装软件
- 采用静默标志：`--accept-package-agreements`、`--accept-source-agreements`
- 将输出重定向到日志文件以保持控制台清洁

**适用条件：**
- 需要 Windows Package Manager 已安装
- 需要网络连接
- 某些软件可能需要手动更新或系统重启

---

### 功能 5：完整网络重置 (Complete Network Reset)

**菜单位置：** [5]  
**主要操作：**
- 执行 `netsh winsock reset` 重置 Winsock 目录
- 执行 `netsh int ip reset` 重置 TCP/IP 栈
- 清空 DNS 缓存
- 需要系统重启以完全生效

**用户警告：**
- 该操作会断开当前网络连接
- 系统重启后网络接口恢复到默认状态
- 需要用户确认后执行

---

### 功能 6：清空事件查看器日志 (Clear Event Viewer Logs)

**菜单位置：** [6]  
**主要操作：**
- 使用 `wevtutil.exe` 枚举所有已注册的事件日志提供程序
- 逐个清空系统日志、安全日志、应用程序日志等
- 恢复日志到清洁状态

**技术实现：**
- 遍历 `wevtutil el` 返回的所有日志通道
- 对每个通道执行 `wevtutil cl <logname>` 命令
- 每次清空操作记录到日志文件

---

### 功能 7：手动 SSD TRIM (Manual SSD TRIM)

**菜单位置：** [7]  
**硬件优化：**
- 针对 NVMe 驱动器的垃圾回收
- 使用现代 PowerShell `Get-Volume` 发现驱动器
- 执行 `defrag /L` 向 SSD 控制器发送 TRIM 提示

**适配硬件：**
- 特别优化了 Kingston KC3000 等 NVMe 驱动器
- Phison 控制器识别 TRIM 信号后执行内部垃圾回收
- 输入净化（去除冒号、空格）防止命令执行错误

**用户交互：**
- 提示用户输入驱动器号（仅字母，如 `C`）
- 验证输入的驱动器存在后再执行 TRIM
- 完成后显示优化结果

---

## 已定义的规则和约定

### 规则来源

这些规则来自项目的 `ANALYSIS.md` 和 `PROMPT_GUIDE.md` 文件，是对该项目长期最佳实践的总结。

### 核心规则列表

1. **维持 Batch 标准** → 任何新功能必须使用原生 `.bat` 命令
2. **保留自动管理员权限** → 不修改现有的 UAC 双层提升逻辑
3. **保持历史完整** → 仅追加文档，不删除已有内容
4. **安全第一方法论** → 破坏性命令必须精确限制范围
5. **清洁详细度控制** → 控制台显示摘要，详细日志入文件
6. **长期进程处理** → 1 分钟以上的操作需提前警告和确认

---

## 技能包库

### 目录结构

```
.agents/
└── skills/
    ├── karpathy-guidelines/
    │   └── SKILL.md          # Karpathy 编码准则
    └── [其他从开源克隆的技能包]
```

### 已安装技能包

| 技能名称 | 来源 | 功能说明 |
|---------|------|---------|
| `karpathy-guidelines` | GitHub 开源 | LLM 编码常见错误的行为准则。用于审查和优化代码，避免过度复杂化，进行精准修改 |

### 技能包安装流程

1. 从 GitHub 或 Skills.sh 搜索合适的开源技能包
2. Clone 或下载到 `.agents/skills/<skill-name>/`
3. 验证包含 `SKILL.md` 主入口文件
4. 在此表中更新记录
5. 在需要时调用相关技能

---

## 任务追踪与进度管理

### 任务文件位置

- **待办事项**：`memory/tasks.md`
- **完成记录**：`memory/YYYY-MM-DD.md`（按日期归档）

### 任务状态

- ⏳ **待开始**：未开始的任务
- 🔄 **进行中**：当前正在进行的工作
- ✅ **已完成**：完成的任务及其成果

### 每日工作日志

每天的工作应记录在 `memory/YYYY-MM-DD.md` 中，包括：
- 完成的任务或调查
- 做出的关键决策
- 发现的问题或改进机会
- 技术笔记和代码片段

---

## 持久约定与决策历史

### 设计决策

| 决策 | 理由 | 日期 |
|------|------|------|
| 使用 Batch 而非 PowerShell | Windows 兼容性更强，脚本更轻量 | 初始化 |
| 双层权限提升机制 | 确保脚本无论如何启动都能获得所需权限 | 初始化 |
| 分离控制台和日志输出 | 改善用户体验，同时保留完整审计日志 | 初始化 |

### 已知限制

1. 某些 Windows API 功能可能在 Batch 中难以实现，需要 PowerShell 辅助
2. WinSxS 清理可能导致某些 Windows 更新失败，需谨慎使用
3. Network Reset 会暂时断开网络连接

### 未来计划

- [ ] 添加 Bitlocker 禁用功能 (Plan 阶段)
- [ ] 集成 Kill Browser AI 功能（基于 PowerShell gist）
- [ ] 增强日志分析和生成报告功能
- [ ] 添加系统回滚点自动创建

---

## 更新历史

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-05-25 | v1.0 | 初始化长期记忆系统，记录项目背景、设计原则、现有功能和规则 |

---

## 快速查询索引

- 📋 **查看任务进度**：`memory/tasks.md`
- 📅 **查看今日工作**：`memory/2026-05-25.md`
- 🔧 **查看技能包**：`.agents/skills/`
- 📖 **查看完整分析**：`ANALYSIS.md`
- 💡 **查看用户指南**：`PROMPT_GUIDE.md`
- 🎯 **查看 Agent 规范**：`AGENTS.md`

