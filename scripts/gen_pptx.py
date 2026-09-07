#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate experiment presentation PPTX."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Colors
DARK_BLUE = RGBColor(0x1E, 0x3A, 0x8A)
MEDIUM_BLUE = RGBColor(0x3B, 0x82, 0xF6)
LIGHT_BLUE = RGBColor(0xDB, 0xEA, 0xFE)
PALE_BLUE = RGBColor(0xEF, 0xF6, 0xFF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_GRAY = RGBColor(0x1F, 0x29, 0x37)
MEDIUM_GRAY = RGBColor(0x4B, 0x55, 0x63)
LIGHT_GRAY = RGBColor(0xF8, 0xFA, 0xFC)
BORDER_GRAY = RGBColor(0xE2, 0xE8, 0xF0)
GREEN = RGBColor(0x16, 0xA3, 0x4A)
RED = RGBColor(0xDC, 0x26, 0x26)
AMBER = RGBColor(0xD9, 0x77, 0x06)

def add_gradient_bg(slide, prs):
    """Add gradient background to slide."""
    background = slide.background
    fill = background.fill
    fill.gradient()
    fill.gradient_stops[0].color.rgb = DARK_BLUE
    fill.gradient_stops[0].position = 0.0
    fill.gradient_stops[1].color.rgb = MEDIUM_BLUE
    fill.gradient_stops[1].position = 1.0

def add_solid_bg(slide, color):
    """Add solid background."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, font_size=18,
                 color=DARK_GRAY, bold=False, alignment=PP_ALIGN.LEFT,
                 font_name='微软雅黑'):
    """Add a text box with single text."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_multiline_textbox(slide, left, top, width, height, lines, font_size=14,
                           color=DARK_GRAY, bold=False, alignment=PP_ALIGN.LEFT,
                           line_spacing=1.5, font_name='微软雅黑'):
    """Add text box with multiple lines."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.bold = bold
        p.font.name = font_name
        p.alignment = alignment
        p.space_after = Pt(4)
    return txBox

def add_rounded_rect(slide, left, top, width, height, fill_color, border_color=None):
    """Add rounded rectangle."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_header_bar(slide, title_text):
    """Add header bar with title."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(0.8)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background()
    add_textbox(slide, 0.5, 0.1, 10, 0.6, title_text, font_size=24,
                 color=WHITE, bold=True)

def create_cover(prs):
    """Slide 1: Cover."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    add_gradient_bg(slide, prs)
    add_textbox(slide, 1, 2.0, 11.33, 1.2, '实验01 开源个人博客系统二次开发',
                font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, 1, 3.3, 11.33, 0.6, '基于 Ghost v6.59.0 的可注册、可写作、可评论、可搜索博客系统',
                font_size=18, color=RGBColor(0xBF, 0xDB, 0xFE), alignment=PP_ALIGN.CENTER)
    # Decorative line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.67), Inches(4.2), Inches(2), Inches(0.05))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    line.line.fill.background()
    add_textbox(slide, 1, 4.6, 11.33, 0.5, '《开源软件与新技术》课程实验 · 2026年9月',
                font_size=14, color=RGBColor(0xDB, 0xEA, 0xFE), alignment=PP_ALIGN.CENTER)
    add_textbox(slide, 1, 5.3, 11.33, 0.4, '上游项目：Ghost (MIT License) · 自定义主题：oss-blog-theme v1.0.0',
                font_size=12, color=RGBColor(0x93, 0xC5, 0xFD), alignment=PP_ALIGN.CENTER)

def create_agenda(prs):
    """Slide 2: Agenda."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    # Left accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.1), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = MEDIUM_BLUE
    bar.line.fill.background()
    add_textbox(slide, 0.5, 0.5, 6, 0.6, '汇报目录', font_size=32, color=DARK_BLUE, bold=True)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.15), Inches(0.8), Inches(0.05))
    line.fill.solid()
    line.fill.fore_color.rgb = MEDIUM_BLUE
    line.line.fill.background()
    
    items = [
        ('01', '项目背景与目标'),
        ('02', '技术选型与系统架构'),
        ('03', '自定义主题与自主扩展'),
        ('04', '测试结果与质量保障'),
        ('05', 'Git 版本管理与开源规范'),
        ('06', '问题反思与总结'),
    ]
    for idx, (num, title) in enumerate(items):
        col = idx % 2
        row = idx // 2
        left = 0.5 + col * 6.2
        top = 1.6 + row * 1.1
        add_rounded_rect(slide, left, top, 5.8, 0.8, WHITE, BORDER_GRAY)
        add_textbox(slide, left + 0.2, top + 0.1, 0.6, 0.6, num,
                    font_size=20, color=MEDIUM_BLUE, bold=True, alignment=PP_ALIGN.CENTER)
        add_textbox(slide, left + 0.9, top + 0.2, 4.5, 0.5, title,
                    font_size=16, color=DARK_GRAY, bold=True)
    add_textbox(slide, 0.5, 6.5, 12.33, 0.5, '本次汇报约 8 分钟，包含 Live Demo 现场演示环节',
                font_size=13, color=MEDIUM_GRAY, alignment=PP_ALIGN.CENTER)

def create_background(prs):
    """Slide 3: Background and goals."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '01 项目背景与目标')
    
    # Background box
    add_rounded_rect(slide, 0.5, 1.1, 6.0, 2.2, WHITE, BORDER_GRAY)
    add_textbox(slide, 0.7, 1.2, 5.6, 0.4, '实验背景', font_size=16, color=DARK_BLUE, bold=True)
    add_multiline_textbox(slide, 0.7, 1.7, 5.6, 1.5, [
        '开源软件已成为现代软件开发的基石。',
        '本实验要求基于成熟开源项目进行二次开发，',
        '深入理解开源项目的架构、代码规范和协作流程，',
        '培养在真实开源代码基础上进行定制化开发的能力。'
    ], font_size=12, color=MEDIUM_GRAY)
    
    # Goals box
    add_rounded_rect(slide, 6.8, 1.1, 6.0, 2.2, WHITE, BORDER_GRAY)
    add_textbox(slide, 7.0, 1.2, 5.6, 0.4, '核心目标', font_size=16, color=DARK_BLUE, bold=True)
    add_multiline_textbox(slide, 7.0, 1.7, 5.6, 1.5, [
        '• 基于 Ghost 搭建可运行的个人博客系统',
        '• 实现可注册、可写作、可评论、可搜索四大功能',
        '• 开发自定义主题，至少完成一项自主扩展功能',
        '• 遵循开源规范，完成 Git 版本管理与文档交付'
    ], font_size=12, color=MEDIUM_GRAY)
    
    # Requirements
    add_rounded_rect(slide, 0.5, 3.6, 12.33, 3.3, PALE_BLUE, RGBColor(0x93, 0xC5, 0xFD))
    add_textbox(slide, 0.7, 3.7, 11.9, 0.4, '功能需求清单', font_size=16, color=DARK_BLUE, bold=True)
    
    cols = [
        ('用户管理', ['管理员账号', '会员注册/登录', '权限分级控制']),
        ('内容管理', ['文章创建/编辑', '标签分类管理', 'Markdown 支持']),
        ('互动功能', ['会员评论系统', '相关文章推荐', '搜索增强']),
        ('工程规范', ['Git 分支管理', 'PR/Code Review', '完整文档交付']),
    ]
    for i, (title, items) in enumerate(cols):
        left = 0.7 + i * 3.05
        add_textbox(slide, left, 4.3, 2.8, 0.35, title, font_size=13, color=DARK_GRAY, bold=True)
        add_multiline_textbox(slide, left, 4.7, 2.8, 1.8,
                              [f'• {item}' for item in items],
                              font_size=11, color=MEDIUM_GRAY)

def create_architecture(prs):
    """Slide 4: Tech stack and architecture."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '02 技术选型与系统架构')
    
    add_textbox(slide, 0.5, 1.0, 6, 0.4, '技术栈选型', font_size=16, color=DARK_BLUE, bold=True)
    
    # Table
    rows_data = [
        ['层级', '技术', '版本'],
        ['运行时', 'Node.js LTS', 'v22.23.1'],
        ['博客核心', 'Ghost', 'v6.59.0'],
        ['数据库', 'SQLite3', '内置'],
        ['主题引擎', 'Handlebars', 'v4.x'],
        ['前端样式', 'CSS3 + JS', '原生'],
    ]
    table_shape = slide.shapes.add_table(len(rows_data), 3, Inches(0.5), Inches(1.5), Inches(5.5), Inches(2.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.5)
    table.columns[1].width = Inches(2.0)
    table.columns[2].width = Inches(2.0)
    for r, row in enumerate(rows_data):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.name = '微软雅黑'
                p.alignment = PP_ALIGN.CENTER
                if r == 0:
                    p.font.bold = True
                    p.font.color.rgb = WHITE
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = DARK_BLUE
                else:
                    p.font.color.rgb = DARK_GRAY
    
    # Selection reasons
    add_textbox(slide, 6.5, 1.0, 6, 0.4, '选型理由', font_size=16, color=DARK_BLUE, bold=True)
    add_rounded_rect(slide, 6.5, 1.5, 6.3, 2.8, WHITE, BORDER_GRAY)
    add_multiline_textbox(slide, 6.7, 1.65, 5.9, 2.5, [
        '• Ghost：专业博客平台，MIT 开源协议，架构清晰，主题系统成熟，API 完善',
        '• SQLite：零配置文件数据库，适合个人博客，便于备份迁移',
        '• Handlebars：语义化模板引擎，Ghost 原生支持，学习成本低',
        '• Node 22：Ghost 官方要求的 LTS 版本，兼容性有保障'
    ], font_size=11, color=MEDIUM_GRAY)
    
    # Architecture diagram
    add_textbox(slide, 0.5, 4.6, 6, 0.4, '系统架构', font_size=16, color=DARK_BLUE, bold=True)
    arch_items = [
        (0.5, '浏览器客户端\n前台 + 管理后台', LIGHT_BLUE, MEDIUM_BLUE),
        (3.5, 'Ghost 核心服务\nExpress + Handlebars\nREST Admin/Content API', RGBColor(0xBF, 0xDB, 0xFE), MEDIUM_BLUE),
        (6.8, '自定义主题层\noss-blog-theme', LIGHT_BLUE, MEDIUM_BLUE),
        (9.8, 'SQLite\n数据持久化', RGBColor(0xFE, 0xF2, 0xF2), RGBColor(0xF8, 0x71, 0x71)),
    ]
    for left, text, fill, border in arch_items:
        add_rounded_rect(slide, left, 5.1, 2.8, 1.5, fill, border)
        add_textbox(slide, left, 5.3, 2.8, 1.1, text, font_size=11,
                    color=DARK_BLUE, bold=True, alignment=PP_ALIGN.CENTER)

def create_baseline(prs):
    """Slide 5: Upstream baseline and modification boundary."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '03 上游基线与修改边界')
    
    # Two top boxes
    add_rounded_rect(slide, 0.5, 1.1, 6.0, 1.6, WHITE, BORDER_GRAY)
    add_textbox(slide, 0.7, 1.2, 5.6, 0.35, '上游基线', font_size=15, color=DARK_BLUE, bold=True)
    add_multiline_textbox(slide, 0.7, 1.6, 5.6, 1.0, [
        '• Ghost Core：v6.59.0，未修改核心代码',
        '• 基础主题：Source v1.7.2（Ghost 官方主题）',
        '• 许可证：MIT License，允许二次开发与商用'
    ], font_size=11, color=MEDIUM_GRAY)
    
    add_rounded_rect(slide, 6.8, 1.1, 6.0, 1.6, WHITE, BORDER_GRAY)
    add_textbox(slide, 7.0, 1.2, 5.6, 0.35, '修改边界原则', font_size=15, color=DARK_BLUE, bold=True)
    add_multiline_textbox(slide, 7.0, 1.6, 5.6, 1.0, [
        '• 不修改 Ghost 核心代码，通过主题和 API 扩展',
        '• 新增文件使用 oss- 前缀，与上游文件明确区分',
        '• 修改上游文件时保留原始结构，仅增量修改'
    ], font_size=11, color=MEDIUM_GRAY)
    
    # Diff table
    add_textbox(slide, 0.5, 2.9, 6, 0.4, '文件级差异统计', font_size=16, color=DARK_BLUE, bold=True)
    diff_data = [
        ['文件/目录', '类型', '行数', '说明'],
        ['assets/css/oss-custom.css', '新增', '373', '自定义样式，含响应式/无障碍'],
        ['assets/js/oss-search.js', '新增', '401', '搜索增强，纯前端实现'],
        ['navigation.hbs', '修改', '+25', '中文化、类名前缀、无障碍'],
        ['post-card.hbs', '修改', '+18', '阅读时间、中文日期、标签图标'],
        ['post.hbs', '修改', '+45', '重写相关文章推荐区域'],
        ['default.hbs', '修改', '+8', '添加自定义 CSS/JS 引用'],
    ]
    table_shape = slide.shapes.add_table(len(diff_data), 4, Inches(0.5), Inches(3.4), Inches(12.33), Inches(3.5))
    table = table_shape.table
    table.columns[0].width = Inches(3.5)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(1.2)
    table.columns[3].width = Inches(6.43)
    for r, row in enumerate(diff_data):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.name = '微软雅黑'
                if r == 0:
                    p.font.bold = True
                    p.font.color.rgb = WHITE
                    p.alignment = PP_ALIGN.CENTER
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = DARK_BLUE
                else:
                    p.font.color.rgb = DARK_GRAY
                    if c in [1, 2]:
                        p.alignment = PP_ALIGN.CENTER

def create_theme(prs):
    """Slide 6: Custom theme development."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '04 自定义主题开发')
    
    cards = [
        (0.5, '导航栏定制', MEDIUM_BLUE, [
            '导航项全面中文化',
            'oss- 类名前缀区分',
            'aria-label 无障碍增强',
            '毛玻璃背景效果',
            '滚动时阴影变化'
        ]),
        (4.7, '文章卡片定制', GREEN, [
            '显示预计阅读时间',
            '中文日期格式',
            '# 标签图标展示',
            '悬停上浮动画效果',
            '卡片阴影层次感'
        ]),
        (8.9, '样式系统增强', AMBER, [
            'oss-custom.css 373行',
            '完整响应式断点',
            '高对比度模式支持',
            '减少动画偏好支持',
            '搜索弹窗专属样式'
        ]),
    ]
    for left, title, color, items in cards:
        add_rounded_rect(slide, left, 1.1, 3.9, 2.5, WHITE, BORDER_GRAY)
        # Header
        hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                      Inches(left), Inches(1.1), Inches(3.9), Inches(0.5))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = color
        hdr.line.fill.background()
        add_textbox(slide, left, 1.15, 3.9, 0.4, title, font_size=14,
                    color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
        add_multiline_textbox(slide, left + 0.2, 1.75, 3.5, 1.7,
                              [f'• {item}' for item in items],
                              font_size=11, color=MEDIUM_GRAY)
    
    # File structure
    add_textbox(slide, 0.5, 3.9, 6, 0.4, '主题文件结构', font_size=16, color=DARK_BLUE, bold=True)
    add_rounded_rect(slide, 0.5, 4.4, 12.33, 2.6, RGBColor(0x0F, 0x17, 0x2A))
    structure_lines = [
        'oss-blog-theme/',
        '├── package.json              # 主题配置 v1.0.0',
        '├── default.hbs               # 修改：添加自定义资源引用',
        '├── post.hbs                  # 修改：相关文章推荐区域',
        '├── partials/',
        '│   ├── components/navigation.hbs   # 修改：中文化+无障碍',
        '│   └── post-card.hbs               # 修改：阅读时间+日期',
        '└── assets/',
        '    ├── css/oss-custom.css          # 新增：373行自定义样式',
        '    └── js/oss-search.js            # 新增：401行搜索增强',
    ]
    add_multiline_textbox(slide, 0.7, 4.5, 11.9, 2.4, structure_lines,
                          font_size=10, color=RGBColor(0x94, 0xA3, 0xB8), font_name='Consolas')

def create_feature1(prs):
    """Slide 7: Related posts recommendation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '05 自主扩展一：相关文章推荐')
    
    add_rounded_rect(slide, 0.5, 1.1, 6.0, 1.5, PALE_BLUE, RGBColor(0x93, 0xC5, 0xFD))
    add_textbox(slide, 0.7, 1.2, 5.6, 0.35, '功能设计', font_size=15, color=DARK_BLUE, bold=True)
    add_multiline_textbox(slide, 0.7, 1.6, 5.6, 0.9, [
        '在文章详情页底部展示与当前文章主题相关的推荐文章，',
        '提升用户阅读深度和站内停留时间。基于标签相似度算法，最多展示4篇。'
    ], font_size=11, color=MEDIUM_GRAY)
    
    add_rounded_rect(slide, 6.8, 1.1, 6.0, 1.5, RGBColor(0xF0, 0xFD, 0xF4), RGBColor(0x86, 0xEF, 0xAC))
    add_textbox(slide, 7.0, 1.2, 5.6, 0.35, '技术实现', font_size=15, color=RGBColor(0x16, 0x65, 0x34), bold=True)
    add_multiline_textbox(slide, 7.0, 1.6, 5.6, 0.9, [
        '使用 Ghost 原生 {{#get}} 助手查询，按 primary_tag 过滤同标签文章，',
        '排除当前文章，按发布时间降序排列。无需后端代码修改，纯主题层实现。'
    ], font_size=11, color=MEDIUM_GRAY)
    
    add_textbox(slide, 0.5, 2.8, 6, 0.4, '核心代码逻辑', font_size=16, color=DARK_BLUE, bold=True)
    add_rounded_rect(slide, 0.5, 3.3, 12.33, 2.2, RGBColor(0x0F, 0x17, 0x2A))
    code_lines = [
        '{{!-- 相关文章推荐：基于主标签相似度 --}}',
        '{{#get "posts" filter="primary_tag:{{primary_tag.slug}}+id:-{{id}}"',
        '     limit="4" order="published_at desc" include="tags"}}',
        '  {{#if posts}}',
        '    {{#foreach posts}}  {{!-- 渲染文章卡片 --}}  {{/foreach}}',
        '  {{else}}',
        '    {{!-- 回退：展示最新文章并提示 --}}',
        '  {{/if}}',
        '{{/get}}',
    ]
    add_multiline_textbox(slide, 0.7, 3.4, 11.9, 2.0, code_lines,
                          font_size=10, color=RGBColor(0x94, 0xA3, 0xB8), font_name='Consolas')
    
    add_rounded_rect(slide, 0.5, 5.7, 6.0, 1.2, RGBColor(0xFE, 0xF9, 0xC7), RGBColor(0xFA, 0xCC, 0x15))
    add_multiline_textbox(slide, 0.7, 5.8, 5.6, 1.0, [
        '设计亮点：优雅降级机制',
        '无同标签文章时自动回退到最新文章，并显示"暂无同标签文章"提示'
    ], font_size=11, color=RGBColor(0x71, 0x3F, 0x12))
    
    add_rounded_rect(slide, 6.8, 5.7, 6.0, 1.2, RGBColor(0xFC, 0xE7, 0xF3), RGBColor(0xF4, 0x72, 0xB6))
    add_multiline_textbox(slide, 7.0, 5.8, 5.6, 1.0, [
        '测试验证：TC-019 测试用例',
        '有标签文章显示相关推荐，无标签文章显示回退内容，推荐数量不超过4篇'
    ], font_size=11, color=RGBColor(0x83, 0x18, 0x43))

def create_feature2(prs):
    """Slide 8: Search enhancement."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '06 自主扩展二：搜索增强')
    
    cards = [
        (0.5, '快捷键唤起', [
            'Ctrl/Cmd + K 快捷键',
            '模态弹窗展示',
            'ESC 键关闭',
            '点击遮罩关闭',
            '自动聚焦输入框'
        ]),
        (4.7, '智能搜索体验', [
            '关键词 mark 高亮',
            '300ms 防抖请求',
            '加载动画反馈',
            '上下箭头键盘导航',
            'Enter 跳转首条结果'
        ]),
        (8.9, '无结果智能建议', [
            '显示热门标签列表',
            '点击标签自动搜索',
            '友好的空状态提示',
            '搜索历史记录',
            '结果数量统计'
        ]),
    ]
    for left, title, items in cards:
        add_rounded_rect(slide, left, 1.1, 3.9, 2.2, WHITE, BORDER_GRAY)
        add_textbox(slide, left + 0.15, 1.2, 3.6, 0.35, title, font_size=14, color=DARK_BLUE, bold=True)
        add_multiline_textbox(slide, left + 0.15, 1.65, 3.6, 1.5,
                              [f'• {item}' for item in items],
                              font_size=11, color=MEDIUM_GRAY)
    
    add_textbox(slide, 0.5, 3.6, 6, 0.4, '技术架构', font_size=15, color=DARK_BLUE, bold=True)
    add_rounded_rect(slide, 0.5, 4.1, 5.8, 1.5, RGBColor(0x0F, 0x17, 0x2A))
    add_multiline_textbox(slide, 0.7, 4.2, 5.4, 1.3, [
        '用户输入 → 300ms防抖 → Ghost Content API',
        '     ↓',
        '  解析JSON → 关键词高亮 → 渲染结果列表',
        '     ↓',
        '  无结果 → 获取热门标签 → 显示建议',
    ], font_size=10, color=RGBColor(0x94, 0xA3, 0xB8), font_name='Consolas')
    
    add_textbox(slide, 6.8, 3.6, 6, 0.4, '安全设计', font_size=15, color=DARK_BLUE, bold=True)
    add_rounded_rect(slide, 6.8, 4.1, 6.0, 1.5, RGBColor(0xF0, 0xFD, 0xF4), RGBColor(0x86, 0xEF, 0xAC))
    add_multiline_textbox(slide, 7.0, 4.2, 5.6, 1.3, [
        '• 仅使用 Content API（只读 Key）',
        '• 不暴露 Admin API Key',
        '• XSS 防护：文本转义后渲染',
        '• 请求失败优雅降级',
    ], font_size=11, color=RGBColor(0x16, 0x65, 0x34))
    
    add_rounded_rect(slide, 0.5, 5.9, 12.33, 1.0, PALE_BLUE, RGBColor(0x93, 0xC5, 0xFD))
    add_multiline_textbox(slide, 0.7, 6.0, 11.9, 0.8, [
        '实现规模：oss-search.js 共 401 行纯前端 JavaScript，零依赖，兼容现代浏览器。',
        '通过 TC-007（搜索命中）、TC-008（无结果提示）、TC-015（键盘可访问）三项测试用例验证。'
    ], font_size=12, color=DARK_BLUE)

def create_testing(prs):
    """Slide 9: Testing results."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '07 测试结果与质量保障')
    
    # Stats cards
    stats = [
        (0.5, '20/20', '测试全部通过', RGBColor(0xDC, 0xFC, 0xE7), GREEN),
        (3.6, '4类', '测试覆盖维度', LIGHT_BLUE, MEDIUM_BLUE),
        (6.7, '0', '严重缺陷', RGBColor(0xFE, 0xF2, 0xF2), RED),
        (9.8, '9篇', '演示文章数据', RGBColor(0xFE, 0xF9, 0xC7), AMBER),
    ]
    for left, num, label, fill, border in stats:
        add_rounded_rect(slide, left, 1.1, 2.8, 1.3, fill, border)
        add_textbox(slide, left, 1.2, 2.8, 0.7, num, font_size=32,
                    color=border, bold=True, alignment=PP_ALIGN.CENTER)
        add_textbox(slide, left, 1.9, 2.8, 0.4, label, font_size=12,
                    color=border, bold=True, alignment=PP_ALIGN.CENTER)
    
    # Test categories table
    add_textbox(slide, 0.5, 2.7, 6, 0.4, '测试用例分类与结果', font_size=16, color=DARK_BLUE, bold=True)
    test_data = [
        ['测试类别', '数量', '覆盖内容', '通过', '失败'],
        ['功能测试', '8', '登录、文章CRUD、标签、评论、搜索', '8', '0'],
        ['权限测试', '4', '匿名访问、匿名禁后台、会员禁后台', '4', '0'],
        ['界面测试', '4', '桌面布局、移动端响应式、键盘可访问', '4', '0'],
        ['恢复测试', '2', '重启数据保留、内容导出与恢复', '2', '0'],
        ['自主扩展', '2', '相关文章推荐、搜索增强功能', '2', '0'],
    ]
    table_shape = slide.shapes.add_table(len(test_data), 5, Inches(0.5), Inches(3.2), Inches(12.33), Inches(3.0))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(1.0)
    table.columns[2].width = Inches(6.0)
    table.columns[3].width = Inches(1.0)
    table.columns[4].width = Inches(1.0)
    for r, row in enumerate(test_data):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.name = '微软雅黑'
                p.alignment = PP_ALIGN.CENTER
                if r == 0:
                    p.font.bold = True
                    p.font.color.rgb = WHITE
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = DARK_BLUE
                else:
                    p.font.color.rgb = DARK_GRAY
                    if c == 3:
                        p.font.color.rgb = GREEN
                        p.font.bold = True
    
    add_textbox(slide, 0.5, 6.5, 12.33, 0.4,
                '测试文档：tests/acceptance.md · 数据备份：SQLite 1.5MB + JSON 109KB · 备份恢复说明：docs/backup-restore.md',
                font_size=11, color=MEDIUM_GRAY, alignment=PP_ALIGN.CENTER)

def create_git(prs):
    """Slide 10: Git and open source."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '08 Git 版本管理与开源规范')
    
    add_textbox(slide, 0.5, 1.0, 6, 0.4, '提交历史（7非合并 + 1合并）', font_size=15, color=DARK_BLUE, bold=True)
    add_rounded_rect(slide, 0.5, 1.5, 5.8, 3.5, RGBColor(0x0F, 0x17, 0x2A))
    git_log = [
        '* baf69cd (HEAD -> main, origin/main)',
        '|   docs: 补充实验报告、截图、PPT、启动入口',
        '*   882cd7b (tag: v1.0-lab)',
        '|\\   merge: 合并自主扩展功能到main',
        '| * e77a7cf docs: PR与Code Review记录',
        '| * e55126a docs: README/NOTICE/备份恢复',
        '| * 86e693c test: 20项验收测试用例',
        '| * a94c800 feat(enhancement): 自主扩展功能',
        '| * 8103140 feat(theme): 自定义主题',
        '|/',
        '* 900732e chore: 初始化项目骨架与基线',
        '',
        '分支策略：main + feature/*',
        '提交规范：Conventional Commits',
        '版本标签：v1.0-lab (annotated)',
    ]
    add_multiline_textbox(slide, 0.65, 1.6, 5.5, 3.3, git_log,
                          font_size=9, color=RGBColor(0x94, 0xA3, 0xB8), font_name='Consolas')
    
    # PR records
    add_textbox(slide, 6.8, 1.0, 6, 0.4, 'Pull Request 与 Code Review', font_size=15, color=DARK_BLUE, bold=True)
    
    add_rounded_rect(slide, 6.8, 1.5, 6.0, 1.6, WHITE, BORDER_GRAY)
    add_textbox(slide, 7.0, 1.6, 5.6, 0.35, 'PR #1: 自定义主题开发', font_size=13, color=DARK_BLUE, bold=True)
    add_multiline_textbox(slide, 7.0, 2.0, 5.6, 1.0, [
        '• 分支：feature/theme-customization → main',
        '• 审查清单：代码规范、无障碍、响应式、安全性',
        '• 审查意见：3条建议，全部回复并处理',
        '• 结论：Approved，合并到 main'
    ], font_size=10, color=MEDIUM_GRAY)
    
    add_rounded_rect(slide, 6.8, 3.3, 6.0, 1.7, WHITE, BORDER_GRAY)
    add_textbox(slide, 7.0, 3.4, 5.6, 0.35, 'PR #2: 自主扩展功能', font_size=13, color=DARK_BLUE, bold=True)
    add_multiline_textbox(slide, 7.0, 3.8, 5.6, 1.1, [
        '• 分支：feature/blog-enhancement → main',
        '• 审查重点：API Key 安全、XSS防护、错误处理',
        '• 审查意见：2条建议（防抖优化、空状态处理）',
        '• 结论：Approved，合并到 main'
    ], font_size=10, color=MEDIUM_GRAY)
    
    add_rounded_rect(slide, 0.5, 5.3, 12.33, 1.5, PALE_BLUE, RGBColor(0x93, 0xC5, 0xFD))
    add_multiline_textbox(slide, 0.7, 5.4, 11.9, 1.3, [
        '开源合规：MIT License 保留 · NOTICE.md 声明第三方资源 · .gitignore 排除敏感文件',
        '（API Key、数据库、node_modules）· 上游修改边界清晰（oss- 前缀区分）',
        '完整文档：README / 实验报告 / 差异清单 / Git证据对照表 / PR-Review记录'
    ], font_size=11, color=DARK_BLUE)

def create_reflection(prs):
    """Slide 11: Reflection and improvement."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, LIGHT_GRAY)
    add_header_bar(slide, '09 问题反思与改进方向')
    
    add_textbox(slide, 0.5, 1.0, 6, 0.4, '遇到的主要问题', font_size=15, color=RED, bold=True)
    
    problems = [
        (1.5, 'Node.js 版本不兼容',
         '系统默认 Node v24 与 Ghost v6.59.0 不兼容（要求 ^22.23.1）。解决方案：下载 Node v22 便携版到项目目录，创建包装脚本切换运行环境。'),
        (2.7, '原生模块编译失败',
         'better-sqlite3/re2 模块需要 VS C++ 构建工具。解决方案：设置 npm 预编译二进制镜像，直接下载预编译版本，绕过本地编译。'),
        (3.9, 'gscan 主题校验工具',
         '因网络环境无法安装运行 gscan。处理方式：记录为已知限制，主题基于官方 Source 开发，兼容性有上游保障，后续可在网络正常时补做。'),
    ]
    for top, title, desc in problems:
        add_rounded_rect(slide, 0.5, top, 6.0, 1.1, RGBColor(0xFE, 0xF2, 0xF2), RGBColor(0xFC, 0xA5, 0xA5))
        add_textbox(slide, 0.7, top + 0.08, 5.6, 0.3, title, font_size=12, color=RGBColor(0x7F, 0x1D, 0x1D), bold=True)
        add_textbox(slide, 0.7, top + 0.4, 5.6, 0.65, desc, font_size=10, color=MEDIUM_GRAY)
    
    add_textbox(slide, 6.8, 1.0, 6, 0.4, '收获与改进方向', font_size=15, color=GREEN, bold=True)
    
    items = [
        (1.5, '主要收获', RGBColor(0xF0, 0xFD, 0xF4), RGBColor(0x86, 0xEF, 0xAC), RGBColor(0x14, 0x53, 0x2D),
         '深入理解了 Ghost 架构和主题系统；掌握了 Handlebars 模板引擎；学会了在成熟开源项目基础上进行二次开发的方法论；实践了 Git 分支管理和 Code Review 流程。'),
        (2.8, '短期改进', RGBColor(0xFE, 0xF9, 0xC7), RGBColor(0xFA, 0xCC, 0x15), RGBColor(0x71, 0x3F, 0x12),
         '补做 gscan 主题校验；增加更多自动化测试；优化搜索结果排序算法；添加文章阅读量统计；完善 SEO 元数据配置。'),
        (4.1, '长期规划', PALE_BLUE, RGBColor(0x93, 0xC5, 0xFD), DARK_BLUE,
         '将自定义主题发布为开源项目；贡献代码回上游 Ghost；探索 Ghost 的 Members 订阅功能；集成第三方评论系统；搭建 CI/CD 自动化部署流程。'),
    ]
    for top, title, fill, border, color, desc in items:
        add_rounded_rect(slide, 6.8, top, 6.0, 1.2, fill, border)
        add_textbox(slide, 7.0, top + 0.08, 5.6, 0.3, title, font_size=12, color=color, bold=True)
        add_textbox(slide, 7.0, top + 0.4, 5.6, 0.75, desc, font_size=10, color=MEDIUM_GRAY)
    
    add_textbox(slide, 0.5, 6.5, 12.33, 0.5,
                '"开源不仅仅是使用代码，更是参与社区、贡献价值、共同成长。"',
                font_size=14, color=MEDIUM_GRAY, alignment=PP_ALIGN.CENTER)

def create_summary(prs):
    """Slide 12: Summary and thanks."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_gradient_bg(slide, prs)
    
    add_textbox(slide, 1, 1.0, 11.33, 1.0, '总结与致谢', font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.67), Inches(2.0), Inches(2), Inches(0.05))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    line.line.fill.background()
    
    add_rounded_rect(slide, 1, 2.4, 11.33, 2.0, RGBColor(0xFF, 0xFF, 0xFF), None)
    # Make it semi-transparent by using a light fill
    add_multiline_textbox(slide, 1.3, 2.6, 10.7, 1.7, [
        '本实验基于 Ghost v6.59.0 开源博客平台，完成了一个功能完整的个人博客系统。',
        '实现了可注册、可写作、可评论、可搜索四大核心功能，开发了自定义主题 oss-blog-theme，',
        '并完成了相关文章推荐和搜索增强两项自主扩展功能。',
        '20项验收测试全部通过，遵循开源规范完成 Git 版本管理与完整文档交付。'
    ], font_size=13, color=RGBColor(0x1E, 0x3A, 0x8A), alignment=PP_ALIGN.CENTER)
    
    add_textbox(slide, 1, 4.7, 11.33, 0.5, '交付物清单', font_size=18, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    
    add_multiline_textbox(slide, 1.5, 5.3, 4.8, 1.5, [
        '• 可运行博客系统（Ghost + 自定义主题）',
        '• 主题压缩包 oss-blog-theme.zip',
        '• 一键启动入口（HTML + BAT）',
        '• 20项验收测试报告',
    ], font_size=11, color=RGBColor(0xBF, 0xDB, 0xFE))
    
    add_multiline_textbox(slide, 7.0, 5.3, 4.8, 1.5, [
        '• 完整实验报告（Word + Markdown）',
        '• 上游基线差异清单',
        '• Git 证据对照表',
        '• PR/Code Review 记录 + 运行截图',
    ], font_size=11, color=RGBColor(0xBF, 0xDB, 0xFE))
    
    add_textbox(slide, 1, 6.8, 11.33, 0.5, '感谢各位老师的聆听与指导！',
                font_size=18, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

def main():
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    create_cover(prs)
    create_agenda(prs)
    create_background(prs)
    create_architecture(prs)
    create_baseline(prs)
    create_theme(prs)
    create_feature1(prs)
    create_feature2(prs)
    create_testing(prs)
    create_git(prs)
    create_reflection(prs)
    create_summary(prs)
    
    output_path = r'D:\Desktop\开源软件作业\oss-blog\docs\实验01-展示PPT.pptx'
    prs.save(output_path)
    print(f"PPT saved to: {output_path}")
    print(f"Total slides: {len(prs.slides)}")

if __name__ == '__main__':
    main()
