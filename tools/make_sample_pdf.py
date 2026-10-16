#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 PaperLens 的示例论文 PDF（纯标准库，无第三方依赖）。
输出: samples/sample-paper.pdf 与 samples/sample-paper.txt
用法: python tools/make_sample_pdf.py
"""
import os, textwrap

PAGE_W, PAGE_H = 612, 792
MARGIN, LINE_H = 72, 16

def esc(s):
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

def wrap(text, width=86):
    return textwrap.wrap(text, width) or ['']

PAGES = [
    # (font, size, text)
    [
        ('F2', 18, 'Neural Attention for Cross-Lingual Document Comprehension'),
        ('F1', 12, 'Alice Zhang, Bob Martin and Carol Lee'),
        ('F1', 12, ' '),
        ('F2', 13, 'Abstract'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'We present a neural attention framework for cross-lingual document comprehension. '
            'The model aligns word embeddings across languages with a shared transformer encoder and a '
            'token-level attention scorer. On two multilingual benchmarks, our approach improves exact-match '
            'accuracy by 4.2 points over the previous state of the art, while reducing inference latency by '
            '18 percent. We further analyze the learned attention weights and show that cross-lingual '
            'alignment emerges in the lower layers of the encoder.')],
        ('F1', 12, 'Keywords: attention, transformer, cross-lingual, embedding, benchmark'),
        ('F1', 12, ' '),
        ('F2', 13, '1. Introduction'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'Understanding documents across languages is central to multilingual information retrieval and '
            'question answering. Existing systems translate the input text before comprehension, which '
            'introduces propagation errors and extra latency. In this paper we propose a single model that '
            'reads the source language directly and reasons over a shared embedding space. Our main '
            'contribution is a token-level attention mechanism that reweights source tokens according to '
            'their relevance to the query, independent of the surface language. We evaluate the framework '
            'on two public benchmarks and report both accuracy and latency.')],
        ('F1', 11, 'Figure 1: Overview of the proposed attention-based framework, including the shared encoder and the token scorer.'),
    ],
    [
        ('F2', 13, '2. Related Work'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'Cross-lingual embeddings. Multilingual word embeddings such as MUSE and LASER project several '
            'languages into one space. However, they are static and do not adapt to the document context. '
            'Neural machine translation approaches treat the problem as a translation task and lose '
            'token-level interpretability. The transformer architecture proposed by Vaswani et al. provides '
            'the backbone for our encoder, while recent work on attention visualization motivates the '
            'interpretability analysis in Section 4.')],
        ('F1', 11, 'Table 1: Benchmark datasets used in the experiments, with language pairs and average document length.'),
        ('F1', 12, ' '),
        ('F2', 13, '2.1 Transformer basics'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'The transformer processes a sequence of tokens with self-attention layers, producing a '
            'contextual representation for every token. Each head computes queries, keys and values from '
            'the input, and the output is a weighted sum of the values. Multi-head attention allows the '
            'model to attend to different subspaces in parallel.')],
    ],
    [
        ('F2', 13, '3. Method'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'Our framework contains three components: a shared encoder, a token-level attention scorer and a '
            'prediction head. The encoder maps tokens of any supported language into a common representation '
            'space, and the scorer computes a relevance distribution over the source tokens for a given '
            'query. The final prediction is produced by the head from the attended representation.')],
        ('F1', 11, 'score(q, k) = q * k / sqrt(d)'),
        ('F1', 12, ' '),
        ('F2', 13, '3.1 Model architecture'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'The encoder is a 6-layer transformer with 8 attention heads and hidden size 512. We share all '
            'parameters across languages and train with a masked language modeling objective before '
            'fine-tuning on the downstream task. The attention scorer takes the query representation and the '
            'encoder outputs, and applies a bilinear score before softmax normalization.')],
        ('F1', 11, 'Figure 2: Training loss curves on the two benchmarks, showing convergence within 20 epochs.'),
    ],
    [
        ('F2', 13, '4. Experiments'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'We evaluate on two multilingual benchmarks: XQuAD-R and MLQA-R. We compare against three '
            'baselines: translate-then-read, static embeddings and a cross-lingual transformer without the '
            'token scorer. All models share the same parameter budget and training schedule.')],
        ('F2', 13, '4.1 Results'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'Our framework achieves an exact-match score of 61.3 on XQuAD-R and 58.9 on MLQA-R, '
            'outperforming the strongest baseline by 4.2 and 3.8 points respectively. The attention '
            'visualization shows that lower layers align tokens across languages, while upper layers focus '
            'on query-relevant content. Inference latency is 18 percent lower than the translate-then-read '
            'pipeline.')],
        ('F2', 13, '5. Conclusion'),
        ('F1', 12, ' '),
        *[('F1', 12, l) for l in wrap(
            'We presented a cross-lingual attention framework that reads the source language directly and '
            'learns token-level alignment without translation. The approach improves accuracy on two '
            'benchmarks and reduces latency. Future work includes extending the framework to more language '
            'families and document-level tasks such as summarization.')],
        ('F2', 13, 'References'),
        ('F1', 11, '[1] Vaswani et al., Attention is all you need, NeurIPS 2017.'),
        ('F1', 11, '[2] Conneau et al., Unsupervised cross-lingual representation learning at scale, ACL 2020.'),
        ('F1', 11, '[3] Artetxe and Schwenk, Massively multilingual sentence embeddings for zero-shot cross-lingual transfer, EMNLP 2019.'),
    ],
]

def content_stream(page):
    lines, y = [], PAGE_H - MARGIN - 24
    for font, size, text in page:
        if text.strip():
            lines.append('BT /%s %.1f Tf %d %d Td (%s) Tj ET' % (font, size, MARGIN, y, esc(text)))
        y -= (size + 7) if size > 12 else LINE_H
    stream = ('\n'.join(lines) + '\n').encode('latin-1')
    return b'<< /Length %d >>\nstream\n' % len(stream) + stream + b'endstream'

def build():
    n_pages = len(PAGES)
    f1 = 2 + 2 * n_pages + 1          # 字体对象位于所有页面/内容对象之后
    f2 = f1 + 1
    objs = []
    objs.append(b'<< /Type /Catalog /Pages 2 0 R >>')
    kids = ' '.join('%d 0 R' % (3 + 2 * i) for i in range(n_pages))
    objs.append(b'<< /Type /Pages /Kids [%s] /Count %d >>' % (kids.encode(), n_pages))
    for i in range(n_pages):
        objs.append(b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Contents %d 0 R '
                    b'/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> >>'
                    % (PAGE_W, PAGE_H, 4 + 2 * i, f1, f2))
        objs.append(content_stream(PAGES[i]))
    objs.append(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    objs.append(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>')

    out = b'%PDF-1.4\n'
    offsets = {}
    for i, obj in enumerate(objs, 1):
        offsets[i] = len(out)
        out += ('%d 0 obj\n' % i).encode() + obj + b'\nendobj\n'
    xref = len(out)
    n = len(objs) + 1
    out += ('xref\n0 %d\n' % n).encode()
    out += b'0000000000 65535 f \n'
    for i in range(1, n):
        out += ('%010d 00000 n \n' % offsets[i]).encode()
    out += ('trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF' % (n, xref)).encode()
    return out

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    samples = os.path.join(base, 'samples')
    os.makedirs(samples, exist_ok=True)
    pdf_path = os.path.join(samples, 'sample-paper.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(build())
    txt_path = os.path.join(samples, 'sample-paper.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        for page in PAGES:
            for _, _, text in page:
                if text.strip():
                    f.write(text + '\n')
    print('written:', pdf_path, os.path.getsize(pdf_path), 'bytes')
    print('written:', txt_path)

if __name__ == '__main__':
    main()
