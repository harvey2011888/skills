#!/bin/bash
# 周报/月报自动生成器 - 演示脚本

echo "╔══════════════════════════════════════════════════════════╗"
echo "║          周报/月报自动生成器 - 功能演示                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 演示 1：生成基础周报
echo "📋 演示 1：生成基础周报"
echo "命令：python cli.py --author \"演示用户\" --team \"技术部\" --output demo_report1.md"
python cli.py --author "演示用户" --team "技术部" --output demo_report1.md
echo "✅ 报告已生成：demo_report1.md"
echo ""

# 演示 2：生成月报
echo "📋 演示 2：生成月报"
echo "命令：python cli.py --type monthly --author \"演示用户\" --output demo_report2.md"
python cli.py --type monthly --author "演示用户" --output demo_report2.md
echo "✅ 报告已生成：demo_report2.md"
echo ""

# 演示 3：使用配置文件
echo "📋 演示 3：使用配置文件生成周报"
cat > demo_config.json << EOF
{
  "report_type": "weekly",
  "author_name": "张三",
  "team_name": "后端开发组",
  "highlights": [
    "完成了用户认证模块开发",
    "优化了数据库查询，性能提升 50%"
  ],
  "challenges": [
    "跨团队协作需要加强"
  ],
  "plans": [
    "推进新功能开发",
    "准备技术分享"
  ]
}
EOF
echo "配置文件已创建：demo_config.json"
echo "命令：python cli.py --config demo_config.json --output demo_report3.md"
python cli.py --config demo_config.json --output demo_report3.md
echo "✅ 报告已生成：demo_report3.md"
echo ""

# 演示 4：运行测试
echo "📋 演示 4：运行测试套件"
echo "命令：python test_report.py"
python test_report.py
echo ""

# 显示生成的报告预览
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    生成的报告预览                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
cat demo_report3.md
echo ""

# 清理演示文件（可选）
read -p "是否清理演示文件？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f demo_report1.md demo_report2.md demo_report3.md demo_config.json
    echo "✅ 演示文件已清理"
else
    echo "ℹ️  演示文件已保留，您可以查看 demo_report*.md 了解生成效果"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    演示完成！                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "💡 提示："
echo "   - 查看快速开始指南：cat QUICKSTART.md"
echo "   - 查看完整文档：cat README_SKILL.md"
echo "   - 查看参赛帖子：cat 参赛帖子.md"
echo ""
