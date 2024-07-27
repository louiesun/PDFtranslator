***Still under heavy development!!!***

## 目标

尝试正确处理包含公式等非PlainText的pdf文件的翻译。

## 要考虑的点

1. 需要正确识别公式并标记。
2. 要尽可能保证一段文本在同一段内，以充分发挥翻译软件的解析上下文能力。

## 如何鉴定专门的数学函数

直接选择参考 $\KaTeX$ [Support Table](https://katex.org/docs/support_table)

```plaintext
arccos
arcctg
arcsin
arctan
……
```

但是我觉得一个脑袋正常的翻译引擎能识别出来。

反而，我觉得可能这类更需要特殊关注（与常用变量高度重合？）

```plaintext
cnt
res
val
ans
```

## 如何鉴定字母代号

正如上述，我们需要识别字母（数字显然不用翻译）。

以`A`为例（另一个是`I`但这玩意主要于句首做主语）。

`This is a banana. `

`We define a to store it. `

这里可以利用公式的不同字体等。比如，事实上，论文一般这样排版。

This is a banana. We fine $a$ to store it. 

先跑起来再说。

## Build

```bash
pip install pymupdf
python main.py [PDFfilename]
```
