# deep_typhoon
Analysis satellite images of typhoons by deep-learning (CNN), based on PyTorch.  

This CNN learns to map the satellite images of typhoons to their max wind speed from. The labeled train set is obtained from agora/JMA.    
    
## Improvements
This repo is forked from [melissa135/deep_typhoon](https://github.com/melissa135/deep_typhoon)
and makes several improvements (so far):
* [Upgrade to Python3 and fix indentation issues with spaces and tabs
](https://github.com/BeVWin/deep_typhoon/commit/c170dd744d6e4890bfea46aaa8d98739e6a6ff26)
* [Use multi-threads to speed up the download of image
and will retry when connections timeout.
](https://github.com/BeVWin/deep_typhoon/commit/27995fa09530f248b95e7fd35530db3f87a6ccc8)
* [Use CUDA to speed up the training
](https://github.com/BeVWin/deep_typhoon/commit/a566250e0651316726a5e65833335ea520c155a5)

## Requirements
* BeautifulSoup  
* PIL  
* Pytorch  

## Usage
Run in `main.py`:
1. Run `download_agora()`, download the satellite images of typhoons to folder `tys_raw`.  
2. Run `create_samples()`, convert raw data into the legal samples for our CNN, create two new forlder `train_set` and `test_set`.  
3. Train CNN using `train_net()`, the trained CNN will be saved as a disk file `net_relu.pth`.  
4. Run `test_net()`, analysis the test set.  

Here is what this CNN thinks of the top 20 typhoons sorted by max wind.  
```
1 ('197920', 130.27679443359375)  
2 ('200914', 127.7662582397461)  
3 ('199019', 122.92172241210938)  
4 ('200918', 122.84004211425781)  
5 ('201614', 122.66597747802734)  
6 ('201601', 122.03250885009766)  
7 ('201513', 121.75947570800781)  
8 ('200922', 121.35771942138672)  
9 ('201013', 120.0194091796875)  
10 ('201330', 118.92587280273438)  
11 ('201419', 117.6025390625)  
12 ('198305', 117.10270690917969)  
13 ('201422', 116.77259063720703)  
14 ('198522', 116.46116638183594)  
15 ('201327', 116.42304992675781)  
16 ('201216', 116.36921691894531)  
17 ('198221', 116.18096923828125)  
18 ('199230', 115.96656799316406)  
19 ('198210', 115.96611022949219)  
20 ('201328', 115.57132720947266)  
```

## Tips
* Memory should be at least 1.5G .  
* This project is written without `cuda()`, while you can use `cuda()` to transfer the CNN onto GPU and speedup the training.  
* The images and labels are crawled from agora.ax.nii.ac.jp/digital-typhoon , and the labels are refered to JMA(Japan Meteorological agency).  

## More Information
See https://mp.weixin.qq.com/s/PBm6sre7u3pEbx_aqjZLwA    
