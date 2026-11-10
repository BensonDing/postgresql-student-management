# 中文安装、录屏与提交指南

本项目文件已经准备好，但你仍需在自己的 Windows 11 电脑连接数据库、录制真实演示视频，并公开上传 GitHub。英文稿中的画面结果是成功运行时应出现的结果，必须以你本地实际运行结果为准。

## 一、先安装和运行，不要一边安装一边录

1. 解压整个 ZIP。进入包含 `README.md`、`requirements.txt`、`database`、`src` 的项目文件夹。
2. 安装 64 位 Python 3.12，勾选 Python Launcher。安装 PostgreSQL 时选择 Server、pgAdmin 4、Command Line Tools。记住你设置的 `postgres` 密码和端口。官方入口：[Python](https://www.python.org/downloads/windows/)、[PostgreSQL](https://www.postgresql.org/download/windows/)。
3. 打开 pgAdmin，连接本地 PostgreSQL。没有服务器时，右键 Servers → Register → Server；名称任意，Connection 页填写 `127.0.0.1`、安装时的端口（通常 5432）、维护数据库 `postgres`、用户 `postgres` 和你自己的密码。
4. 在已有的 `postgres` 数据库右键 → Query Tool。启用 Auto-commit。Ctrl+O 打开 `database/create_database.sql`，F5 执行，创建 `student_management`。此命令要单独执行，不能包在 BEGIN 事务里。已有同名数据库就跳过。
5. 右键 Databases → Refresh。对 **student_management** 右键 → Query Tool。确认这次窗口连接的是 **student_management**。
6. Ctrl+O 打开 `database/init.sql`，F5 执行完整文件。它一次创建表并插入三条指定数据。只初始化一次；不要再执行 `schema.sql`、`seed.sql`。后两个文件只是另一种初始化方式。
7. 打开 `database/verify.sql` 并按 F5。应有 John Doe、Jane Smith、Jim Beam 三条记录。若 init 执行报错，在该窗口执行 `ROLLBACK;`，根据 README 排错后再操作；不要随意删除其他数据库。
8. 在文件资源管理器打开项目文件夹，空白处右键 → 在终端中打开。PowerShell 逐行执行：

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   Copy-Item .env.example .env
   notepad .env
   ```

9. 将 `.env` 的 `CHANGE_ME` 换成你自己的 PostgreSQL 密码。其他字段必须和 pgAdmin 的主机、端口、数据库和用户名一致。保存并关闭。**不要录到或上传 `.env`。** 若密码含英文单引号，可改用适当的双引号格式；`$` 不会被程序当作变量替换。
10. 运行：

    ```powershell
    .\.venv\Scripts\python.exe .\src\main.py
    ```

11. 输入 `1`，应显示三位初始学生。再输入 `0` 退出。
12. 可运行真实集成测试：

    ```powershell
    .\.venv\Scripts\python.exe .\tests\integration_test.py
    ```

    成功应显示 `Ran 15 tests` 和 `OK`。测试会新建独立临时数据库，完成后删除；不修改作业库中的学生表。需要当前用户有 CREATEDB 权限，默认本地 `postgres` 用户通常有。Windows 和你安装的 pgAdmin 仍需由你亲自验证。

## 二、把录屏需要的三个窗口提前摆好

- **PowerShell**：处于项目根目录，准备好运行命令。
- **pgAdmin**：两个 Query Tool 标签都连接 `student_management`。A 标签打开 `schema.sql` 仅展示结构，**录屏时不要执行它**；B 标签打开 `verify.sql`，用于不断重新查询。保持 Auto-commit 开启。
- **代码编辑器**：打开 `src/main.py` 和 `README.md`，方便最后展示连接和 SQL 代码。不要打开 `.env`。

pgAdmin 左侧应能展开：Servers → 你的服务器 → Databases → student_management → Schemas → public → Tables → students。找不到表时，右键 Tables → Refresh。

确保五列都能看见，终端字号够大。把英文稿放在另一台设备/另一块屏幕上，或打印出来，避免录到你反复找稿子的过程。

## 三、设置跨窗口录屏

建议使用 [OBS Studio 官方下载](https://obsproject.com/download)。它能录整块显示器，适合在 PowerShell、pgAdmin、代码编辑器之间切换。

1. 安装后打开 OBS。首次自动配置向导可选择以录制为主。无需配置直播。
2. 在 **Sources / 来源** 点 `+` → **Display Capture / 显示器采集** → 选择你演示的显示器。使用整屏采集才能拍到切换窗口。
3. 在 **Audio Mixer / 音频混音器** 检查 `Mic/Aux`。讲话时音量条应移动。若没有麦克风来源，在 Sources 点 `+` → **Audio Input Capture / 音频输入采集** → 选择麦克风。避免同时采集同一麦克风两次造成重音。
4. Settings → Output → Recording 检查保存目录。录制格式可用 MKV；录完后用 **File → Remux Recordings** 转为 MP4，方便上传。若你的 OBS 界面语言不同，按对应英文名称找。
5. 先录 10 秒测试：切一次窗口、说一句话，再停止。播放确认画面和人声都清楚。
6. 关闭通知和无关窗口。录屏前输入密码并关闭配置文件。正式视频无需露脸，除非课程其他通知另有要求。

## 四、按稿子演示：目标约 4 分 30 秒，绝不能超过 5 分钟

英文逐字稿在 [demonstration_script.md](demonstration_script.md)。只朗读每节 **Say** 的英文；其余都是操作提示。

| 时间 | 你要做什么 | 应看到什么 |
| --- | --- | --- |
| 0:00–0:20 | Start Recording；PowerShell 运行程序，介绍项目 | 选项 1、2、3、4、0 |
| 0:20–1:05 | 切 pgAdmin，展示学生表位置和 A 标签里的 schema | 五个字段、IDENTITY、主键、NOT NULL、UNIQUE |
| 1:05–1:25 | B 标签 F5 查询 | 三条指定初始数据 |
| 1:25–1:45 | 切 PowerShell，输入 `1` | 三条记录和 Total students: 3 |
| 1:45–2:30 | 输入 `2`，按提示新增 Alex；立即切 pgAdmin 按 F5 | 由三条变四条 |
| 2:30–3:10 | 输入 `3`，用 Alex 的实际 ID 修改邮箱；切 pgAdmin F5 | 仍四条，只有 Alex 邮箱变化 |
| 3:10–3:45 | 输入 `4`，删除同一个 ID；切 pgAdmin F5 | 回到最初三条 |
| 3:45–4:20 | 切编辑器展示 get_connection、addStudent 的 SQL 和错误处理 | Psycopg、参数占位符、with 事务管理 |
| 4:20–4:30 | 展示 README，结尾；停止录制 | 完成所有要求且不超过五分钟 |

新增时逐项输入，每项按 Enter：

```text
Alex
Chen
alex.chen@example.com
2024-01-15
```

**记下程序返回的 student_id。** 全新初始化后通常是 4，但失败插入或反复排练可能让 ID 变成其他数字。修改和删除必须输入程序真实显示的数字，不能照抄 `NEW_ID`，也不能默认永远是 4。

修改时新邮箱填写：

```text
alex.chen.updated@example.com
```

三个数据库验证画面必须都有：**新增后四条、修改后新邮箱、删除后剩原始三条**。必须在 pgAdmin **重新按 F5 查询**；停留在旧结果上不会自动更新。

英文稿先练一次并计时。如果说得较慢，可加快窗口切换、在讲解时同时输入；不要省略 CRUD 或 pgAdmin 验证。时间只是排练目标，最终以视频真实时长为准。

## 五、重录时怎样恢复

如果上一遍已经完成新增再删除，表里应仍是最初三条；下次新增 ID 更大也没有问题。若练习数据还在，可用程序删除对应的 Alex 记录，保留最初三位学生。

若你确定 `student_management` 只是此次作业的练习库，并且愿意删除当前表里**全部数据**，可手动运行 `database/reset_demo.sql`。它会清空学生表、重置 ID 并恢复指定三条数据。运行前务必确认数据库名称，别在其他库执行。该脚本不会由应用或测试自动运行。

## 六、视频上传

1. 停止录制后，完整播放一遍。核对麦克风声音、文字清晰度、四个函数和三次 pgAdmin 验证。
2. 确认成片 **≤ 5:00**；建议控制在约 4:30，给片头片尾留余量。
3. 上传到支持链接观看的平台。YouTube 可选 **Unlisted / 不公开列出**，不要选 **Private / 私密**。这里的视频可以 Unlisted；作业要求 **GitHub 仓库必须 Public**，两者不要混淆。
4. 用浏览器隐私窗口、不登录账号打开链接，确认别人无需申请权限即可观看。
5. 编辑项目根目录 `README.md` 顶部 **Demonstration video URL**，将 `NOT YET RECORDED...` 整句换成你真实的视频链接。

## 七、创建公开 GitHub 仓库并上传

当前未替你发布 GitHub 仓库。可以用 GitHub Desktop 上传，避免网页拖拽时漏掉以点开头的配置文件。

1. 从 [GitHub Desktop 官方网站](https://desktop.github.com/) 安装并登录你自己的 GitHub 账号。
2. 先在项目文件夹里将 README 的视频链接填好。
3. GitHub Desktop → **File → Add local repository** → 选择项目根目录。如果提示不是 Git repository，使用提示中的 **create a repository here**，让路径指向这个已解压的项目目录，不要另建一个空项目。
4. 检查更改列表：应包含 README、requirements、SQL、Python、docs、tests、`.gitignore`、`.env.example`。**不能包含 `.env`、`.venv`、密码、录屏文件或数据库文件。** `.env.example` 中只能保留 CHANGE_ME。
5. 填写提交说明，例如 `Implement PostgreSQL student CRUD application`，点击 **Commit to main**（初始分支名可能因设置不同而不同）。
6. 点击 **Publish repository**。名称可填 `postgresql-student-management`。**取消勾选 Keep this code private**，然后发布到你自己的账号。如果同名仓库已存在，请用新名字，不要覆盖旧仓库。
7. 点击 **View on GitHub**，检查仓库显示 **Public**。README、database、src 应直接在仓库根目录；README 的视频链接应可点击。
8. 用隐私窗口打开仓库和视频，确认助教不登录也能访问。

若使用 GitHub 网页上传：先创建新 **Public** 仓库，再上传项目内容，不要只上传整个 ZIP；还要确保 `.gitignore` 和 `.env.example` 都被包含，`.env` 与 `.venv` 均未上传。Windows 可以打开文件资源管理器的 **View → Show → File name extensions**，避免误把 `.env` 保存成 `.env.txt`。

## 八、最后提交到 Brightspace

1. 对照 [demonstration_checklist.md](demonstration_checklist.md) 逐项检查。
2. 提交的是 **公开 GitHub 仓库 URL**，不是本地文件路径，也不是仅视频链接。
3. README 中必须有真实可访问的视频链接，视频总时长不能超过 5 分钟。
4. Brightspace 如有备注栏，可按实际情况补充说明；无需编造测试或运行情况。
5. 截图没有给出明确截止日期，请以课程页面为准。TA 指示写明迟交扣 **10%**。

官方操作参考：[OBS Quick Start](https://obsproject.com/kb/quick-start-guide)、[GitHub Desktop 发布项目](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop)。

