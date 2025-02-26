```markdown
# SelfMade_Nerf_LLFFdatasets

## 1. 配置环境
首先，在 Anaconda 中创建虚拟环境，并安装依赖：

```bash
conda create -n Nerf-pytorch python==3.11.7
conda activate Nerf-pytorch
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

如果遇到报错，请尝试手动逐个安装 `requirements.txt` 中的依赖项。推荐使用 `pytorch` 版本 2.1.0（本人的 `CUDA` 版本为 12.6）。

## 2. 数据集准备
将拍摄好的数据集放入当前工作路径下（如 `D:/test/`）。假设是一个动态环绕物体的视频，按照以下步骤操作：

1. 激活环境：  
   ```bash
   conda activate Nerf-pytorch
   ```

2. 运行 `read_video.py` 文件，进行视频切割并逐帧提取图片，自动保存在 `./images` 目录下。

## 3. 安装 COLMAP
在本地计算机上安装并配置 COLMAP：

1. 打开 COLMAP，点击 **新建项目**。
2. 在 **Database** 选项中点击 **New**，在工作路径（例如 `D:/test`）下创建 `database.db` 文件。
3. 在 **Images** 选项中点击 **Select**，选择刚才生成的 `images` 路径。
4. 点击 **Save**。

## 4. 特征提取与匹配
在 COLMAP 中，依次点击 **Feature Extract** 和 **Feature Matching**，进行特征提取和匹配。

然后，执行 **SfM 稀疏重建**：

1. 完成重建后，将模型导出到 `D:/data/sparse/0`，该路径需要提前创建。

2. 保存上述二进制文件，包含了相机的内外参数。

## 5. 图像降采样
运行以下文件，分别对原数据集进行 4 倍和 8 倍的降采样：

```bash
python img_4.py
python img_8.py
```

这将生成 `images_4` 和 `images_8` 文件夹，分别包含降采样后的图片。

## 6. 生成相机姿态文件
1. 克隆并下载 GitHub 上的 LLFF 项目：

```bash
git clone https://github.com/Fyusion/LLFF.git
unzip LLFF-master.zip
```

2. 在解压后的 `LLFF-master` 目录中，找到 `imgs2poses.py` 文件，并在文件中的以下行更改路径：

```python
parser.add_argument('--scenedir', default="D:/test/")
```

3. 修改 `LLFF/llff/poses/pose_utils.py` 文件（大约在第 32 行），添加以下代码：

```python
#---------输出匹配到位姿的图片名---------
for i in np.argsort(names):
   print(names[i], end=' ')
#---------输出匹配到位姿的图片名---------
```

4. 运行 `imgs2poses.py`，将生成相机姿态的 `npy` 文件。

```bash
python imgs2poses.py
```

## 7. 移动数据并配置 NERF
将 `test` 文件夹移动到 `nerf/data/llff_data/` 目录下，并修改配置文件：

1. 在 `nerf/configs` 目录下，将 `fern.txt` 复制为 `test.txt`，并将文件中的以下内容进行修改：
   - 第 1 行：将 `"fern_test"` 修改为 `"test"`
   - 第 3 行：将 `"fern"` 修改为 `"test"`

2. 在 `nerf` 目录下，使用以下命令开始训练：

```bash
python run_nerf.py --config configs/test.txt
```

---

**注意**：确保在进行训练之前，所有路径和文件夹结构已正确配置。

```
