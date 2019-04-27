#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import glob
import operator
import codecs
import re
import time
import chardet

KTargetFile = '*.lproj/*.strings'

KGenerateStringsFile = 'TempfileOfStoryboardNew.strings'

ColonRegex = r'["](.*?)["]'

KeyParamRegex = r'["](.*?)["](\s*)=(\s*)["](.*?)["];'

AnotationRegexPrefix = r'/(.*?)/'


def constructAnotationRegex(str):
	return AnotationRegexPrefix + '\n' + str

def getAnotationOfString(string_txt,suffix):
	anotationRegex = constructAnotationRegex(suffix)
	anotationMatch = re.search(anotationRegex,string_txt)
	anotationString = ''
	if anotationMatch:
		match = re.search(AnotationRegexPrefix,anotationMatch.group(0))
		if match:
			anotationString = match.group(0)
	return anotationString


def getTxtWithString(string):
	if string is None:
		return ''
	else:
		# print(string)
		newString_type = chardet.detect(string)
		newString_txt = string.decode(newString_type['encoding'])
		# newString_txt = string.decode('UTF-16')
		# print('文件类型 ----%s'%newString_type)
		# print(newString_txt)
		return newString_txt


def compareWithCodeFilePath(tempPath,SourcePath):
	print('比较代码部分')
# 	读取temp文件提取内容
	nameString = 'Localizable.strings'
	newStringPath = tempPath +'/'+ nameString
	originalStringPath =  SourcePath +'/'+ nameString
	print('original----%s'%originalStringPath)
	with codecs.open(newStringPath,'rb') as nspf:
	    newString = nspf.read()
	    newString_txt = getTxtWithString(newString)
	    # print("读取的内容：%s"%newString_txt)
	newString_dic = {}
	anotation_dic = {}
	for stfmatch in re.finditer(KeyParamRegex, newString_txt):
		linestr = stfmatch.group(0)
		# print(linestr)
		anotationString = getAnotationOfString(newString_txt, linestr)
		linematchs = re.findall(ColonRegex, linestr)
		if len(linematchs) == 2:
			leftvalue = linematchs[0]
			rightvalue = linematchs[1]
			newString_dic[leftvalue] = rightvalue
			anotation_dic[leftvalue] = anotationString
	# print('新字典 ----%s' % newString_dic)
	# print('不用的字典 ----%s'%anotation_dic)

	# read originalStringfile原始文件
	with codecs.open(originalStringPath, 'rb') as ospf:
		newString_origin = ospf.read()
		originalString_txt = getTxtWithString(newString_origin)

	# print("读取的源文件内容：%s" % originalString_txt)
	originalString_dic = {}
	for stfmatch in re.finditer(KeyParamRegex, originalString_txt):
		linestr = stfmatch.group(0)
		linematchs = re.findall(ColonRegex, linestr)
		if len(linematchs) == 2:
			leftvalue = linematchs[0]
			rightvalue = linematchs[1]
			originalString_dic[leftvalue] = rightvalue
	# print('originalString----%s' % originalString_dic)

	# compare and remove the useless param in original string
	for key in originalString_dic:
		if (key not in newString_dic):
			keystr = '"%s"' % key
			print(keystr)
			replacestr = '//' + keystr
			match = re.search(replacestr, originalString_txt)
			if match is None:
				originalString_txt = originalString_txt.replace(keystr, replacestr)
	# compare and add new param to original string
	executeOnce = 1
	for key in newString_dic:
		values = (key, newString_dic[key])
		# print(values)
		if (key not in originalString_dic):
			newline = ''
			if executeOnce == 1:
				timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				newline = '\n//##################################################################################\n'
				newline += '//#           ZPPAutoLocalizable            ' + timestamp + '\n'
				newline += '//##################################################################################\n'
				executeOnce = 0
			newline += '\n' + anotation_dic[key]
			newline += '\n"%s" = "%s";\n' % values
			originalString_txt += newline
		# print('生成的新文件')
		# print(originalString_txt)
	# write into origial file
	# sbfw = open(originalStringPath, "wb")
	# sbfw.write(originalString_txt)
	# sbfw.close()
	with codecs.open(originalStringPath,'wb') as sbfw:
		sbfw.write(originalString_txt.encode('UTF-8'))
#   读取source文件内容准备对比
#   对比文件添加或者删除内容
#   移除temp文件

def compareWithFilePath(newStringPath,originalStringPath):
    print('比较文件生成新文件')
    # 新文件都是生成在不同目录的string文件
    print('新文件 ----' +newStringPath)
    # 需要对比的老文件
    print('老文件 ----' +originalStringPath)
    # 读取新文件，把所有的内容变成字典
    with codecs.open(newStringPath,'rb') as nspf:
	    newString = nspf.read()
	    newString_txt = getTxtWithString(newString)
	    # print("读取的内容：%s"%newString_txt)
    newString_dic = {}
    anotation_dic = {}
    for stfmatch in re.finditer(KeyParamRegex, newString_txt):
        linestr = stfmatch.group(0)
        # print(linestr)
        anotationString = getAnotationOfString(newString_txt, linestr)
        linematchs = re.findall(ColonRegex, linestr)
        if len(linematchs) == 2:
            leftvalue = linematchs[0]
            rightvalue = linematchs[1]
            newString_dic[leftvalue] = rightvalue
            anotation_dic[leftvalue] = anotationString
        # print('新字典 ----%s' % newString_dic)
        # print('不用的字典 ----%s'%anotation_dic)

    #read originalStringfile原始文件
    with codecs.open(originalStringPath,'rb') as ospf:
	    newString_origin = ospf.read()
	    originalString_txt = getTxtWithString(newString_origin)

    # print("读取的源文件内容：%s" % originalString_txt)
    originalString_dic = {}
    for stfmatch in re.finditer(KeyParamRegex, originalString_txt):
        linestr = stfmatch.group(0)
        linematchs = re.findall(ColonRegex, linestr)
        if len(linematchs) == 2:
            leftvalue = linematchs[0]
            rightvalue = linematchs[1]
            originalString_dic[leftvalue] = rightvalue
    # print('originalString----%s' % originalString_dic)

    # compare and remove the useless param in original string
    for key in originalString_dic:
        if (key not in newString_dic):
            keystr = '"%s"' % key
            print(keystr)
            replacestr = '//' + keystr
            match = re.search(replacestr, originalString_txt)
            if match is None:
                originalString_txt = originalString_txt.replace(keystr, replacestr)
    # compare and add new param to original string
    executeOnce = 1
    for key in newString_dic:
        values = (key, newString_dic[key])
        # print(values)
        if (key not in originalString_dic):
            newline = ''
            if executeOnce == 1:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                newline = '\n//##################################################################################\n'
                newline += '//#           ZPPAutoLocalizable            ' + timestamp + '\n'
                newline += '//##################################################################################\n'
                executeOnce = 0
            newline += '\n' + anotation_dic[key]
            newline += '\n"%s" = "%s";\n' % values
            originalString_txt += newline
            # print('生成的新文件')
            # print(originalString_txt)
    # write into origial file
    # sbfw = open(originalStringPath, "wb")
    # sbfw.write(originalString_txt)
    # sbfw.close()
    with codecs.open(originalStringPath, 'wb') as sbfw:
	    sbfw.write(originalString_txt.encode('UTF-8'))

# 生成文件名
def extractFileName(file_path):
	seg = file_path.split('/')
	lastindex = len(seg) - 1
	return seg[lastindex]
# 生成路径前缀
def extractFilePrefix(file_path):
	seg = file_path.split('/')
	lastindex = len(seg) - 1
	prefix =  seg[lastindex].split('.')[0]
	return prefix

# shell 执行命令
def generateShellForUI(sourcePath,tempPath):
    cmdString = 'ibtool '+ sourcePath + ' --generate-strings-file ' + tempPath
    if os.system(cmdString) == 0:
        return 1


def generateCodeFiles(projectPath):
    print("代码国际化")
# 	生成temp文件
    tempPath = 'tempLocalizableStringsFilePath'
    cmdCD = 'cd ' + projectPath
    cmdMKDIR = 'mkdir ' + tempPath

    tempFilePath = projectPath + '/' + tempPath
    if os.path.exists(tempFilePath):
	    cmdString = cmdCD + '&&' + 'find . -name \*.m | xargs genstrings -o ' + tempPath
    else:
	    cmdString = cmdCD + '&&' + cmdMKDIR + '&&' + 'find . -name \*.m | xargs genstrings -o ' + tempPath

    if os.system(cmdString) == 0:
	    return tempFilePath
    else:
	    return 1


# 生成代码文件
def generateCodeLocalizableFile(sourcePaths,projectPath):
	tempPath = generateCodeFiles(projectPath)
	if tempPath == 1:
		return
	nameString = 'Localizable.strings'
	tempPathFile = tempPath + '/' + nameString
	for sourcePath in sourcePaths:
		compareWithCodeFilePath(tempPath,sourcePath)
	os.remove(tempPathFile)



# 生成文件
def generateLocalizableFiles(filePath ,sourceFilePath):
	# print ('------->  sourceFilePath: ' + sourceFilePath + '  filePath: ' + filePath)
	sourceFile_list = glob.glob(sourceFilePath)
	print('获得xib或者sb的具体文件')
	print(sourceFile_list)
	if len(sourceFile_list) == 0:
		print ('error ，no result of list!')
		return
	targetFilePath = filePath + '/' + KTargetFile
	targetFile_list = glob.glob(targetFilePath)
	tempFile_Path = filePath + '/' + KGenerateStringsFile
	# print('tempfile')
	# print(tempFile_Path)
	if len(targetFile_list) == 0:
		print ('error framework , no .lproj dic was found')
		return
	for sourcePath in sourceFile_list:
		sourceprefix = extractFilePrefix(sourcePath)
		sourcename = extractFileName(sourcePath)
		print ('init with %s'%sourcename)
		if generateShellForUI(sourcePath,tempFile_Path) == 1:
			print ('- - genstrings %s successfully'%sourcename)
			for targetPath in targetFile_list:
				print('targetPath')
				print(targetPath)
				targetprefix = extractFilePrefix(targetPath)
				targetname = extractFileName(targetPath)
				# 判断相同的目录，多个xib或者sb的话，是否执行
				print('sourcePrefix %s  targetPrefix %s'%(sourceprefix,targetprefix))
				if operator.eq(sourceprefix,targetprefix):
					print ('- - dealing with %s'%targetPath)
					compareWithFilePath(tempFile_Path,targetPath)
			print ('finish with %s'%sourcename)
			# os.remove(tempFile_Path)
		else:
			print ('- - genstrings %s error'%sourcename)




#根据项目根目录遍历所有的xib和storyboard的文件路径
def getAllUIPathFor(dir):
	sourceFilePaths = []
	#三个参数：1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
	for parent,dirnames,filenames in os.walk(dir):
		for filename in filenames: #输出文件信息
			# print(filename)
			if (('.xib' in filename) | ('.storyboard' in filename)):
				filePath = os.path.join(parent)
				if filePath not in sourceFilePaths:
					sourceFilePaths.append(filePath)
	# print('sourceFilePaths --- %s'%sourceFilePaths)
	return sourceFilePaths
# 根据查找所有含有Localizable的文件路径
def getAllCodePathFor(dir):
	sourceFilePaths = []
	# 三个参数：1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
	for parent, dirnames, filenames in os.walk(dir):
		for filename in filenames:  # 输出文件信息
			# print(filename)
			if operator.eq('Localizable.strings',filename):
				# print('codeFilePath ---%s'%parent)
				filePath = os.path.join(parent)
				if filePath not in sourceFilePaths:
					sourceFilePaths.append(filePath)
	# print('sourceFilePaths --- %s' % sourceFilePaths)
	return sourceFilePaths

def main():
	# 脚本执行接受外部参数
	# print(sys.argv)
	if len(sys.argv) == 1:
		# 如果在终端运行，注意要修改自己需要国际化的项目文件夹的路径！
		filePath = '/Users/figaro/Desktop/language/language'
	else:
		filePath = sys.argv[1]


# 	查找所有。h 和。m文件找到中间的中文字符。生成一个标准。strings文件
	sourceFilePaths = getAllUIPathFor(filePath)
# 	查找所有。xib 和 。sb文件，找到所有需要文件,生成新文件
	# *.storyboard 国际化
	for sourceFilePath in sourceFilePaths:
		baseStrIdx = 0
		try:
			# 该方法返回查找对象的索引位置，如果没有找到对象则抛出异常
			baseStrIdx = sourceFilePath.index('Base.lproj')
		except Exception as e:
			pass
		else:
			sourceFilePathName = sourceFilePath + '/*.storyboard'
			upperFilePath = sourceFilePath[0:(baseStrIdx-1)]
			# print('在upper查找sb文件 --- '+upperFilePath)
			generateLocalizableFiles(upperFilePath, sourceFilePathName)
	# *.xib 国际化
	for sourceFilePath in sourceFilePaths:
		baseStrIdx = 0
		try:
			baseStrIdx = sourceFilePath.index('Base.lproj')
		except Exception as e:
			pass
		else:
			sourceFilePathName = sourceFilePath + '/*.xib'
			upperFilePath = sourceFilePath[0:(baseStrIdx-1)]
			# print('在upper查找xib文件 --- '+upperFilePath)
			generateLocalizableFiles(upperFilePath, sourceFilePathName)
# 	代码部分生成新文件
	sourceCodeFilePaths = getAllCodePathFor(filePath)
	generateCodeLocalizableFile(sourceCodeFilePaths,filePath)



if __name__ == '__main__':
	main()

