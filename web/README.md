# Interactive Game AI Lab · 交互式游戏 AI 实验室

[`gameai-lab.html`](gameai-lab.html) is a self-contained, single-file web page with
**three live, interactive debug viewports** — the same algorithms as the Python
samples, ported to the browser so you can watch and play with them:

一个自包含的单文件网页，内含**三个可交互的调试视图**——与 Python 示例相同的算法，
移植到浏览器中，可实时观看与操作：

1. **Pac-Man ghost AI** — the four ghost personalities (Blinky / Pinky / Inky /
   Clyde), scatter/chase modes, and each ghost's live target tile.
   吃豆人四幽灵性格、追逐 / 散开模式，以及每个幽灵的实时目标格。
2. **FPS suppress & flank** — an anchor pins the player while a flanker takes a
   concealed path to a new angle (line-of-sight, cover, suppression).
   FPS 火力压制与包抄：锚点压制、包抄手沿规避视线的路径迂回。
3. **Unbeatable minimax** — a playable tic-tac-toe board that searches the whole
   game tree and never loses. Try to beat it.
   可对弈的“不可战胜”井字棋，搜索整棵博弈树，永不落败。

## Viewing · 查看方式

- **Locally:** open `gameai-lab.html` in any modern browser — no server, no build,
  no dependencies. 直接用浏览器打开即可，无需服务器或依赖。
- It is theme-aware (light / dark), responsive, and respects reduced-motion.
  支持浅色 / 深色主题、响应式布局，并尊重“减少动态效果”偏好。

The page is standard HTML/CSS/JS with everything inlined, so it also works as an
Artifact on claude.ai.
页面为纯内联 HTML/CSS/JS，同样可作为 claude.ai 上的 Artifact 运行。
