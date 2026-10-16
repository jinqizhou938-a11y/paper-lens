#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成中文期刊风格样张（reportlab，STSong-Light CID 字体 + UniGB-UCS2-H CMap）。
用于验证 pdf.js CMap 修复对「缺 ToUnicode 的 CJK PDF」的解码效果。
用法: python tools/make_cn_sample.py
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

TITLE = '产业政策与债券发行定价效率'
AUTHORS = '栗宇丹  郭雅婷  罗炜'
AFFIL = '（华南师范大学经济与管理学院，广东广州 510006）'
ABSTRACT = ('摘 要：本文以 2014—2024 年 A 股上市公司为样本，考察产业政策对债券发行定价效率的影响。'
            '研究发现，重点产业政策显著降低了债券发行利差，且这一效应在市场化程度较高的地区更为明显。'
            '本文进一步从信息不对称与投资者关注两个渠道解释了上述影响，为完善产业政策与债券市场改革提供了经验证据。')
KEYWORDS = '关键词：产业政策；债券定价；发行利差；信息不对称'
SECTIONS = [
    ('一、引言', [
        '债券市场是中国企业直接融资的重要渠道，其定价效率直接关系到资源配置的质量。产业政策作为政府引导资源配置的重要手段，是否以及如何影响债券定价效率，是近年来学术界与市场关注的热点问题。本文试图从债券发行定价的视角，检验产业政策的经济后果。',
    ]),
    ('二、理论分析与研究假设', [
        '产业政策可能通过缓解信息不对称降低债券发行利差。政府背书与政策信号能够降低投资者对发行人的信息搜寻成本，从而压缩风险溢价。基于此，本文提出研究假设 H1：产业政策支持显著降低债券发行利差。',
    ]),
    ('三、研究设计', [
        '本文构建如下基准回归模型：',
        '利差 = α + β × 产业政策 + γ × 控制变量 + 固定效应 + ε',
        '图1 样本债券发行利差的年度分布',
        '表1 变量定义表',
    ]),
    ('四、实证结果', [
        '基准回归结果显示，产业政策变量的系数显著为负，说明产业政策显著降低了债券发行利差。进一步的分组检验表明，该效应在信息不对称程度较高的样本中更强。',
    ]),
    ('五、结论', [
        '本文的研究表明产业政策能够提升债券定价效率，为理解政策工具在资本市场中的作用提供了新的证据。',
    ]),
]
REFS = [
    '［1］栗宇丹，郭雅婷，罗炜．产业政策与债券发行定价效率［J］．经济研究，2025（5）：1-20．',
    '［2］林毅夫．新结构经济学［M］．北京：北京大学出版社，2019．',
    '［3］陈晓，李静．政府补贴与企业融资成本［J］．管理世界，2022（8）：45-60．',
]


def _wrap(text, n):
    out = []
    while len(text) > n:
        out.append(text[:n])
        text = text[n:]
    out.append(text)
    return out


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    samples = os.path.join(base, 'samples')
    os.makedirs(samples, exist_ok=True)
    out = os.path.join(samples, 'cn-sample-paper.pdf')
    c = canvas.Canvas(out, pagesize=A4)
    w, h = A4

    def newpage():
        c.showPage()
        return h - 60

    y = h - 110
    c.setFont('STSong-Light', 16)
    c.drawCentredString(w / 2, y, TITLE); y -= 28
    c.setFont('STSong-Light', 12)
    c.drawCentredString(w / 2, y, AUTHORS); y -= 22
    c.drawCentredString(w / 2, y, AFFIL); y -= 38
    c.setFont('STSong-Light', 11)
    for line in _wrap(ABSTRACT, 46):
        if y < 90: y = newpage()
        c.drawString(72, y, line); y -= 18
    c.drawString(72, y, KEYWORDS); y -= 30
    for title, paras in SECTIONS:
        if y < 80: y = newpage()
        c.setFont('STSong-Light', 13)
        c.drawString(72, y, title); y -= 22
        c.setFont('STSong-Light', 11)
        for p in paras:
            for line in _wrap(p, 46):
                if y < 80: y = newpage()
                c.drawString(72, y, line); y -= 17
        y -= 8
    if y < 80: y = newpage()
    c.setFont('STSong-Light', 13)
    c.drawString(72, y, '参考文献'); y -= 22
    c.setFont('STSong-Light', 10)
    for r in REFS:
        for line in _wrap(r, 60):
            if y < 80: y = newpage()
            c.drawString(72, y, line); y -= 15
    c.save()
    print('written:', out, os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main()
