# SelfMade_Nerf_LLFFdatasets
1.配置anaconda虚拟环境，在anaconda终端依次输入：
conda create -n Nerf-pytorch python==3.11.7
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
如果报错，请尝试将requirements.txt中的依赖项手动逐个下载；pytorch版本请酌情下载，这里博主推荐2.1.0版本，本人cuda版本为12.6；
2.在当前工作路径下（如D:/test/)，放入拍摄好的数据集（这里以一个动态环绕物体的视频为例），首先启动环境：
conda activate Nerf-pytorch
然后运行read_video.py文件，进行视频切割，逐帧提取得到图片，并自动放置在./images路径下；
3.需要在本地计算机上安装COLMAP。运行COLMAP，点击新建项目，如图所示，在database选项点击new，在工作路径D:/test下新建database.db，在images选项点击select，选择至刚才的images路径下；然后选择save。
![COLMAP1](https://github.com/user-attachments/assets/1ba59e0d-8e6c-4f10-89e7-c8024e50b5e5)
4.如下图所示，依次点选feature extract和feature matching进行特征提取和特征匹配。
<img width="434" alt="image" src="https://github.com/user-attachments/assets/44f888b6-ef52-4dbf-8ea4-8665ccec64c6" />
之后进行SfM稀疏重建：
<img width="454" alt="image" src="https://github.com/user-attachments/assets/81d8e963-4ea9-488d-9673-3a8b8900fbb3" />
重建结束后，导出模型文件至D:/data/sparse/0，上述sparse/0等相关路径均需新建：
<img width="385" alt="image" src="https://github.com/user-attachments/assets/6ff0b4b7-1441-4d96-94dc-7d2fa8075ff6" />
保存好上述二进制文件，其中包含了相机的内外参数。
5.运行
python img_4.py
和
python img_8.py
文件，对原数据集分别进行4倍和8倍的降采样，生成新的路径images_4和images_8，其中分别包含了降采样后的图片，这在nerf的训练中是需要的。
6.生成相机姿态文件。
在终端下载github的LLFF文件，将相机位姿进行格式转化：
git clone https://github.com/Fyusion/LLFF.git
unzip LLFF-master.zip
在解压缩之后的文件中找到imgs2poses.py文件，在文件的"parser.add_argument('--scenedir', "这一行中，将default=""中的内容改为"D:/test/";
另外，在LLFF/llff/poses/pose_utils.py的代码32行左右补充如下所示内容：
![image](https://github.com/user-attachments/assets/87e6177c-9cef-4976-98d4-883ffaa03b5d)
    #---------输出匹配到位姿的图片名---------
    for i in np.argsort(names):
       print(names[i],end=' ')
    #---------输出匹配到位姿的图片名---------
这样可以保证在之后的位姿文件生成过程中，看到所有匹配到相机位姿的图片，保证一一对应；否则，未能匹配的图片需要删掉，不然Nerf会报错。
然后在当前路径下运行
python imgs2poses.py
这样在test路径下将会生成npy文件。
7.将该test整个文件移动至nerf/data/llff_data/路径下：
<img width="590" alt="image" src="https://github.com/user-attachments/assets/336a3ab9-2c6c-4987-97b0-9936595c3445" />
在nerf路径下，进入nerf/configs，复制fern.txt为test.txt，并将文件第一行中的"fern_test"和第三行中的"fern"均改为"test"；
![image](https://github.com/user-attachments/assets/107e5f30-d0a4-4f3a-8fbd-9452ceb3eb41)
![image](https://github.com/user-attachments/assets/c2740330-1f6b-4b83-b40e-f7124538054c)
回到nerf路径下，进入Nerf-pytorch环境，运行python run_nerf.py --config configs/test.txt即可开始训练。

