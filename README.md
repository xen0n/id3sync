# id3sync

万恶舍友系列... 还是那个 TASCAM DR-2d, 不能识别 MP3 文件的 ID3v1 标签, 只能识别 ID3v2. 无奈 Mutagen 的 ID3 标签支持刻意做得不支持 ID3v1 (只要存在 ID3v2 标签就完全无视 ID3v1)... 于是自己动手, 帮他把一千多个 MP3 文件的 ID3v2 和 ID3v1 标签同步了, 顺便又调整了标题等字段的编码. 幸好 ID3v1 够简单 :-D

这是个 Python 库, 你需要的是 `id3sync.id3v1.parse_ID3v1{,file}` 和 `id3sync.tag.sync_tags` 三个函数, 用法直接看 docstring 就行了. 因为是随手的事情, 自己也暂时没有这方面需求, 所以这次就没写命令行工具了.


## 授权

* BSD 许可证


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
