# ZPPLanguage

## 项目主要展示python3全自动脚本，不管是代码还是xib，sb中的文字都会自动导入项目。删除和添加都不用手动维护。


## 使用方法：

1.在项目中添加需要的国际化语言，使用Localizable生成相应语言的实体文件。

2.项目中添加Run Script，填入

~~~
export PYTHONIOENCODING=UTF-8
python3 ${SRCROOT}/${TARGET_NAME}/ZPPScript/ZPPAutoLocalizable.py ${SRCROOT}/${TARGET_NAME}
~~~

3.复制粘贴该展示项目中的文件ZPPScript，只需要把文件放入项目目录，不需要导入Xcode工程

4.需要国际化时，同时按下 command + B 

## [完全国际化指南](https://juejin.im/post/5cc5095cf265da03576ecd9f)，对国际化有疑问请查看这里。
。

## 疑问解答：

* 如果没有生效？

  * 请检查你是否使用了系统的国际化宏，代码部分，只会生成使用了国际化宏的对应字符。
  如：

  ~~~
  button.titleLabel.text = NSLocalizedString(@"可能性测试", nil);
  ~~~
  * 请检查你是否有python3环境，mac系统自带python2.7环境；我使用的是python3.7。
  * 不要使用压缩包，直接clone项目，然后取项目中的ZPPScript文件。
  

## 提示：你可以在每一个.m文件需要国际化的字符里这样写：

~~~
button.titleLabel.text = NSLocalizedString(@"可能性测试", “xxxxx.m”);
~~~

之后在生成的国际化语言中，你会发现这个国际化的注释会生成。当需要翻译的文字太多时，方便查找是哪个页面的字符。
