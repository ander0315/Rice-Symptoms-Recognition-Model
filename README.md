# 病蟲害分類系統
## 介紹 
這個專案基於Visual-Attention-Network(VAN)架構，旨在應用於從手機拍攝的圖像中分類植物的病蟲害等徵狀問題。由於Attention架構可以有效學習全局特徵，因此選擇了基於這個架構訓練分類模型。

## 功能
- 使用Visual-Attention-Network(VAN)架構進行植物影像蟲害分類。

## 呈現結果
|                       原始圖片                       |                          推論結果                           |
| :--------------------------------------------------------------: | :---------------------------------------------------------------------: |
| <img src="results\ori_27975_1.jpg" alt="raw" width="600"> | <img src="results\demo_27975_1.png" alt="inference" width="600"> |

## 模型
### 模型架構
- 輸入層（Input Layer）
  - 接受尺寸為𝐻×𝑊×𝐶的輸入圖像，其中𝐻為高度，𝑊為寬度，𝐶為通道數。
- 初始卷積層（Initial Convolution Layer）
  - 使用卷積層將圖像的通道數轉換為所需的特徵數，並進行初步的特徵提取。
- 多頭自注意力層（Multi-Head Self-Attention Layers）
  - 多層堆疊的自注意力機制，每層包含多頭自注意力模塊：
    - 查詢、鍵、值（Query, Key, Value）計算
    - 多頭自注意力機制殘差連接（Residual Connection）
    - 層歸一化（Layer Normalization）
- 位置編碼（Positional Encoding）
  - 為每個特徵圖位置添加位置信息，以捕捉空間關係。
- 層次化結構（Hierarchical Structure）
  - 將多層注意力機制分組為不同的層次，每個層次進行特徵下采樣（例如使用池化層或卷積層），以獲取多尺度特徵。
- 融合多尺度信息（Multi-Scale Information Fusion）
  - 通過融合來自不同層次的特徵，提升模型的特徵表達能力。
- 自適應權重分配（Adaptive Weight Allocation）
  - 動態調整各注意力頭的重要性，提升模型對重要信息的關注能力。
- 完全連接層（Fully Connected Layers）
  - 將最終的特徵圖展平並輸入到一個或多個全連接層，以進行分類或回歸等任務。
- 輸出層（Output Layer）
  - 最終的輸出層，根據具體任務（如分類、分割）給出相應的輸出。

|                       Layer架構                       |                          模型架構                           |
| :--------------------------------------------------------------: | :---------------------------------------------------------------------: |
| <img src="results\LKA.png" alt="raw" width="300"> | <img src="results\structure.png" alt="inference" width="300"> |

### 訓練方式
參照[mmpretrain](https://mmpretrain.readthedocs.io/zh-cn/latest/index.html)框架進行訓練
- 訓練數據: 將水稻異常區域進行裁切後的資料集
- 損失函數: LabelSmoothLoss
- 優化器: AdamW
- 訓練批次大小: 128
- 學習率: 5e-4 * 1024 / 512

### 預訓練權重


### 模型評估
- accuracy/top1: 97.6825  
- accuracy/top3: 99.5731  
- accuracy/top5: 99.7561  
- mAP: 97.3660  
- precision: 97.9251  
- recall: 95.4201  
- f1-score: 96.5334

### 模型可視化
使用 Grad-CAM 技術進行視覺化，以產生模型對稻穗區域的注意力熱圖，並進行解釋。
|   層    |                                 圖片                                  |
| :-----: | :-------------------------------------------------------------------: |
|  backbone.blocks4.2.norm1  |   <img src="results\rIH03_27975_1.jpg" width="200">   |

### 模型穩定性


### 模型公平性


### 資料集
使用原始植物病蟲害資料集中的水稻子集，並將異常區域進行裁切的前處理。

類別共31種，如下所示(問題代號:編號):
- 'K0': 42,
- 'N0': 1,
- 'OT07': 583,
- 'OT10': 670,
- 'rDA09': 86,
- 'rDB01': 380,
- 'rDF02': 318,
- 'rDM10': 23,
- 'rDP03': 1562,
- 'rDR04': 304,
- 'rDS05': 68,
- 'rDS06': 210,
- 'rDU11': 165,
- 'rDX07': 144,
- 'rDX08': 180,
- 'rIC05': 411,
- 'rIC07': 3153,
- 'rID13': 582,
- 'rIH03': 240,
- 'rIH04': 414,
- 'rIH06': 820,
- 'rIH11': 335,
- 'rIH12': 355,
- 'rIH14': 64,
- 'rIH16': 4,
- 'rIL01': 2009,
- 'rIL02': 1026,
- 'rIL08': 123,
- 'rIL10': 11,
- 'rIL15': 38,
- 'rIO09': 228

## 自訂資料集
需依照類別名稱進行資料存放(ImageNet格式)

## 安裝
參照[mmpretrain安裝方式](https://mmpretrain.readthedocs.io/zh-cn/latest/get_started.html#id2)

## 使用
參照[mmpretrain目錄格式](https://mmpretrain.readthedocs.io/zh-cn/latest/user_guides/config.html)

## 訓練
參照[mmpretrain訓練方式](https://mmpretrain.readthedocs.io/zh-cn/latest/user_guides/train.html)

## 推論
參照[mmpretrain推論方式](https://mmpretrain.readthedocs.io/zh-cn/latest/user_guides/test.html)

## 參考文獻
[mmpretrain GitHub](https://github.com/open-mmlab/mmpretrain)

[VAN](https://arxiv.org/abs/2202.09741)
