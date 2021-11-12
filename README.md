# 詳細なアノテーション基準に基づく症例報告コーパスからの固有表現及び関係の抽出精度

これは第41回医療情報学連合大会にて発表した「詳細なアノテーション基準に基づく症例報告コーパスからの固有表現及び関係の抽出精度」のGoogle Colaboratory上で動作する推論用のデモコードです。

## 使用方法

1. 本リポジトリをダウンロードして解凍する。
2. ファイル名をJoint_Inferenceへ変更する。
3. 解凍したファイルをGoogle Driveのマイドライブの直下にアップロードする。
4. inference.ipynbを開いて実行する (必要なファイルが自動でダウンロードされるので、Google Driveの空き容量にご注意ください)。

## モデルについて

本モデルは[症例報告コーパス](https://ai-health.m.u-tokyo.ac.jp/home/research/corpus)に掲載される[iCorpus_202108](https://ai-health.m.u-tokyo.ac.jp/labweb/wp-content/uploads/icorpus_202108.zip)に含まれる、182症例2,172文を用いて学習を行ったものです。

モデルの詳細は詳細抄録を、コーパスの詳細は[7]をご確認ください。


## 引用

本コードを参照する場合は以下の論文を引用してください。
```
柴田 大作, 河添 悦昌, 篠原 恵美子, 嶋本 公徳. 詳細なアノテーション基準に基づく症例報告コーパスからの固有表現及び関係の抽出精度. 第41回医療情報学連合大会, pp. XXX-YYY, 2021.
```

## 参考文献
```
[1] Eberts, Markus, and Adrian Ulges. "Span-based joint entity and relation extraction with transformer pre-training." arXiv preprint arXiv:1909.07755 (2019).
[2] Zhang, Xingxing, Jianpeng Cheng, and Mirella Lapata. "Dependency parsing as head selection." arXiv preprint arXiv:1606.01280 (2016).
[3] pytorch_multi_head_selection_re, https://github.com/WindChimeRan/pytorch_multi_head_selection_re
[4] SpERT: Span-based Entity and Relation Transformer, https://github.com/lavis-nlp/spert
[5] pytorch-crf: https://pytorch-crf.readthedocs.io/en/stable/
[6] deepdep: https://github.com/tatsuokun/deepdep
[7] 篠原 恵美子, 河添 悦昌, 柴田 大作, 嶋本 公徳, 関 倫久. 医療テキストに対する網羅的な所見アノテーションのためのアノテーション基準の構築. 第25回日本医療情報学春季学術大会.
```
