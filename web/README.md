# Interactive Game AI Lab · 交互式游戏 AI 实验室

[`gameai-lab.html`](gameai-lab.html) is a self-contained, single-file web page with
**seven live, PLAYABLE debug viewports** — the same algorithms as the Python
samples, ported to the browser so you can control them and watch the AI react:

一个自包含的单文件网页，内含**七个可交互、可操作的调试视图**——与 Python 示例相同的
算法，移植到浏览器中，你可以亲自操控、并看 AI 如何反应：

1. **Pac-Man** — **you** drive (arrow keys / WASD / D-pad) while the four ghost
   personalities (Blinky / Pinky / Inky / Clyde) hunt you. 亲自操控吃豆人，躲避四幽灵。
2. **Boids flocking** — lead the swarm with your cursor. 用光标带领蜂群。
3. **A\* pathfinding** — click to move the goal, or draw your own walls and watch it
   re-route. 点击移动目标，或自己画墙看它重新寻路。
4. **FPS suppress & flank** — click a floor tile to reposition the defender; the
   squad re-plans its flank. 点击地块重新部署防守者，小队随之重新规划包抄。
5. **Minimax** — a playable board; unbeatable on *Perfect*, beatable on *Casual*.
   可对弈的井字棋；“完美”不可战胜，“休闲”可被击败。
6. **Q-learning** — click to place the goal/pit and watch the agent relearn live.
   点击放置目标 / 陷阱，实时观看智能体重新学习。
7. **Open-world streaming / LOD AI** — drive through the world, adjust the full-sim
   radius and LLM "hero" NPCs, and watch the frame budget (the GTA-scale question).
   驾车穿行，调节全模拟半径与 LLM 主角 NPC，观察帧预算（GTA 级难题）。

## Viewing · 查看方式

- **Locally:** open `gameai-lab.html` in any modern browser — no server, no build,
  no dependencies. 直接用浏览器打开即可，无需服务器或依赖。
- It is theme-aware (light / dark), responsive, and respects reduced-motion.
  支持浅色 / 深色主题、响应式布局，并尊重“减少动态效果”偏好。

The page is standard HTML/CSS/JS with everything inlined, so it also works as an
Artifact on claude.ai.
页面为纯内联 HTML/CSS/JS，同样可作为 claude.ai 上的 Artifact 运行。
