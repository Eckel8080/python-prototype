# Windows 环境下命令执行编码规范

本规范旨在解决在 Windows 系统环境（如 PowerShell 或 CMD）下执行命令并捕获输出时，因默认 GBK 编码与 UTF-8 解码不匹配导致中文报错或提示信息出现乱码的问题。

## 1. 乱码原因分析

在 Windows 操作系统中，系统默认的区域设置（Locale）通常决定了控制台的默认活动代码页（Active Code Page）：
- 对于中文简体的 Windows 系统，默认代码页通常是 **GBK（代码页 936）**。
- 大多数现代开发工具、编译器以及 AI 代理系统（包括本系统）默认使用 **UTF-8（代码页 65001）** 编码来读取和解析命令行的标准输出（stdout）和标准错误（stderr）。

当命令行工具（如 `git`、`ipconfig`、`ping` 或各种编译器）输出中文时，它们会按照当前控制台的代码页（GBK）对中文字符进行编码。而接收这些输出的程序则尝试以 UTF-8 格式进行解码。由于 GBK 和 UTF-8 的多字节编码格式不兼容，解码过程就会失败，从而在日志或返回结果中呈现为乱码。

## 2. 解决方案

为了确保命令输出中的中文信息能够被正确解析，在执行可能产生中文输出的命令前，必须显式地将控制台的输出编码设置为 UTF-8。

### 2.1 CMD 环境下的解决方案

在 CMD 终端中，可以使用 `chcp` 命令（Change Code Page）将活动代码页临时切换为 65001（即 UTF-8）：

```cmd
chcp 65001 > nul && <your_command>
```
*注：`> nul` 用于屏蔽 `chcp` 命令自身的输出（例如“Active code page: 65001”），使主命令的输出更加干净。*

### 2.2 PowerShell 环境下的解决方案

在 PowerShell 中，有几种方式可以确保输出编码为 UTF-8：

#### 方法一：设置控制台输出编码（推荐）
通过设置 `[Console]::OutputEncoding`，可以强制控制台的输出采用 UTF-8 编码。这对于捕获外部可执行文件（如 `git`）的输出非常有效：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; <your_command>
```

#### 方法二：设置环境变量和管道编码
在某些情况下，PowerShell 在通过管道传递文本时会使用 `$OutputEncoding` 变量指定的编码。建议与控制台编码一同设置：

```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; <your_command>
```

#### 方法三：混用 chcp 命令
在 PowerShell 中也可以直接调用 `chcp 65001`，但为了使其在当前会话的 .NET 环境中完全生效，建议结合 `[Console]::OutputEncoding` 使用。

## 3. AI 代理执行命令规范要求

当 AI 代理在 Windows 环境下自动执行命令时，应遵循以下规范：

1. **组合执行**：对于所有可能包含本地化中文输出的系统命令或第三方 CLI 工具，不要单独执行。应当将编码设置命令与目标命令组合在同一个命令行中执行。
   - **PowerShell 推荐格式**：
     ```powershell
     [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; <目标命令>
     ```
   - **CMD 推荐格式**：
     ```cmd
     chcp 65001 > nul && <目标命令>
     ```
2. **工具链配置**：如果配置了特定的开发环境（如 Python、Node.js 编译环境），可通过设置系统环境变量来辅助控制编码：
   - 设置 `PYTHONIOENCODING=utf-8` 以确保 Python 脚本输出 UTF-8。
   - 设置环境变量 `LANG=zh_CN.UTF-8` 或 `LC_ALL=zh_CN.UTF-8`。
3. **日志捕获与审核**：在捕获的输出中如果依然发现类似 `` 的替换字符，说明编码未成功转换，应停止后续自动处理并检查命令链中的编码设置是否正确应用。
