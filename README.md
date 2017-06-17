Cryptography
=========

本项目包含密码学的Jupyter Notebook

### 目录
1. [导论与流密码 Introduction and Stream Ciphers](https://github.com/reata/Cryptography/blob/master/Introduction%20and%20Stream%20Ciphers.ipynb)
2. [分组密码 Block Ciphers](https://github.com/reata/Cryptography/blob/master/Block%20Ciphers.ipynb)
3. [信息完整性 Message Integrity](https://github.com/reata/Cryptography/blob/master/Message%20Integrity.ipynb)
4. [认证加密 Authenticated Encryption](https://github.com/reata/Cryptography/blob/master/Authenticated%20Encryption.ipynb)
5. [密钥交换基础 Basic Key Exchange](https://github.com/reata/Cryptography/blob/master/Basic%20Key%20Exchange.ipynb)
6. [公钥加密 Public-Key Encryption](https://github.com/reata/Cryptography/blob/master/Public-Key%20Encryption.ipynb)

### 编程练习

#### 第一周 一次性密码本
使用流密码时，密钥在每次使用后需要更换，即所有密钥只能用于一条信息的加密，称为一次性密码本。多次使用同一密钥，会造成不安全。

第一周的编程练习，给定了11组使用相同密钥加密的密文，需要根据这些密文进行破解。

一个提示：空格space（0x21)和任何字母（0x41~0x5A, 0x61~0x7A）进行异或运算，会改变该字母的大小写。所以一条密文中的特定字符如果是空格，则该字符与其它密文对应字符的异或结果很大可能是字母（与标点异或则不是字母）。根据这条规律，可以进行破译。详情见week1_many_time_pad.py。

#### 第二周 分组密码
直接将一次性密码本用于加密，每次需要生成和明文同长的随机密钥，计算量极大且密钥的传输也是一个问题。实际中通常采用的是分组密码，也即将明文切割为多个模块，对每个模块使用AES或3DES加密，模块之间然后按照一定逻辑进行组合。

常见的分组加密标准包括CBC和CTR两种模式。第二周的编程练习，给定了CBC和CTR加密的密文各两组，需要构造解密函数进行解密。详情见week2_block_cipher.py。

#### 第三周 信息完整性
信息保密性之外，加密系统的另一个特征是信息完整性。如何保证信息在传递过程中没有发生错误，接受者收到的信息和发送者发送的信息相同，这里就需要应用讯息鉴别码（MAC）生成标签，文件的MD5值就属于信息完整性的应用。

通常计算信息的标签需要整个文件。在本周的编程练习中，我们讨论的具体情境是在线视频的播放。

假设某网站提供在线视频，而浏览器在播放之前需要核对信息是否准确，下载整个文件则耗时过长。如何在边下边播的过程中，保证所下载的文件是正确的？

解决方案是将文件分块，比如分为若干个大小为1KB的组，每一个组到包含本组的数据信息以及之后一个组的SHA256值，最后一个组仅仅包含数据本身。

这样，第0组包括：1)第0组的数据。2)第1组的SHA256值h1。将第0组全部信息进行SHA256，得到h0。

浏览器在下载了第0组的信息时，只需要核对其SHA256值，是否和h0相等，如果相等，则播放第0组视频。同时第0组还包含了第一组的h1,从而可以继续核对。

第三周的编程练习，需要程序在给定文件时，计算其h0值。详情见week3_file_authentication.py。

#### 第四周 认证加密
直接对明文使用加密系统进行加密，所得到的密文可以应对选择明文攻击，但无法应对选择密文攻击，因此我们需要首先对明文添加讯息鉴别码保证信息完整性，然后在加密提供保密性。同时兼顾完整性和保密性的加密系统被称为认证加密。

TLS标准中，信息接收方需要首先核对补齐的padding是否正确，其次在检查密文的标签是否正确。一旦发现不正确即返回错误信息。注意：如果返回的信息包含了具体的错误原因，可能导致严重的padding oracle攻击。

本周的编程练习，给定一个会返回具体错误信息的网站，而密文可以从URL中提取。攻击者需要利用padding oracle的漏洞，攻击并破译给定的密文。

详情见week4_padding_oracle.py。（由于墙的原因，即使挂了代理，给指定网站发送请求依然连接超时，没有办法完成练习，本章的代码来自Github用户mgraczyk，仅做了简单的格式修改使代码符合PEP8规范。

#### 第五周 离散对数
这一章主要介绍密钥交换和数论的相关知识，数论当中对合数进行因子分解以及计算离散对数这两大难题，分别造就了基于迪菲-赫尔曼协议以及基于陷门函数的两种公钥加密系统。

没有公钥加密系统首先建立会话交换密钥，之前所学的对称加密系统就全无意义。本周的编程练习，介绍了一种免于穷举的离散对数计算方法，可以达到O(sqrt(N))的复杂度。

设有素数p，从集合[0, p-1]上随机抽取两个整数g和h。对于1 <= x <= 2<sup>40</sup>，有h = g<sup>x</sup>。给定p, g, h，需要计算x。采用穷举的办法，需要尝试所有2<sup>40</sup>种可能。采用以下算法，则可以降低到2<sup>20</sup>。

令B = 2<sup>20</sup>，x0和x1是[0, B-1]上的整数，有x = x0 * B + x1。这样h = g<sup>x</sup> = g<sup>x0 * B + x1</sup> = g<sup>B * x0</sup> * g<sup>x1</sup> in Z<sub>p</sub>。移项可得 h / g<sup>x1</sup> = g<sup>B * x0</sup> in Z<sub>p</sub>。

这样，对于2<sup>20</sup>种x1，可以计算出所有对应的h / g<sup>x1</sup>，建立一张哈希表。然后对于所有x0，计算g<sup>B * x0</sup>，查询结果是否在表中。详情见week5_discrete_log.py。

### 参考资料
1. [Coursera斯坦福大学密码学公开课](https://www.coursera.org/learn/crypto)

