# 詳細なアノテーション基準に基づく症例報告コーパスからの固有表現及び関係の抽出精度

これは第41回医療情報学連合大会にて発表した「詳細なアノテーション基準に基づく症例報告コーパスからの固有表現及び関係の抽出精度」のGoogle Colaboratory上で動作する推論用のデモコードです。

## 使用方法

1. 本リポジトリをダウンロードして解凍する。
2. ファイル名をUTH-17_Joint_Inferenceへ変更する。
3. 解凍したファイルをGoogle Driveのマイドライブの直下にアップロードする。
4. inference (Google Colab).ipynbを開いて実行する (必要なファイルが自動でダウンロードされるので、Google Driveの空き容量にご注意ください)。

## 参考文献
```
[1] Eberts, Markus, and Adrian Ulges. "Span-based joint entity and relation extraction with transformer pre-training." arXiv preprint arXiv:1909.07755 (2019).
[2] Zhang, Xingxing, Jianpeng Cheng, and Mirella Lapata. "Dependency parsing as head selection." arXiv preprint arXiv:1606.01280 (2016).
[3] pytorch_multi_head_selection_re, https://github.com/WindChimeRan/pytorch_multi_head_selection_re
[4] SpERT: Span-based Entity and Relation Transformer, https://github.com/lavis-nlp/spert
[5] pytorch-crf: https://pytorch-crf.readthedocs.io/en/stable/
[6] deepdep: https://github.com/tatsuokun/deepdep
```
