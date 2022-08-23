# WeMo Insight ワットメータ

## 概要

Belkin WeMo Insgiht を使って消費電力を計測し，Fluentd に送信するスクリプトです．

## 準備

`config.yml` と `device.yml` を書き換えて，Fluetd サーバやデバイス名の
変換に関する設定を行います．

## 使い方

```
python3 app/belklin_wemo_logger.py
```
