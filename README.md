如果想用jupyter notebook 跑，就跑FogEdgeRun.ipynb.
如果想用python跑，就跑Publisher.py

进去code里 改掉URL，改成测试设备的url，建议一次只读取一个设备的数据。
URL_host_list = ["http://192.168.0.148"]
这个list里 把遥测的设备的ucl写进去，建议写一个，多个设备情况还没测试过，可能有bug

跑的时候大概率会遇到少library的情况
打开cmd，搜索栏搜cmd，进入terminal，说少了XXXX包就输入：pip install XXXXX
